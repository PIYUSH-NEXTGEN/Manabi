"""Crawler CLI and orchestration: compliance → discover → extract → publish (§7, §10)."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import date
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.crawler import config as crawler_config
from app.crawler.compliance import ComplianceError, RobotsCache, assert_compliant
from app.crawler.dedupe import content_hash
from app.crawler.discovery import CrawlContext, DiscoveredItem, RobotsDisallowed, discover
from app.crawler.extract import Budget, BudgetExhausted, ExtractionError, NoClearProblem, extract_draft
from app.crawler.fetcher import FetchError, HostThrottle, safe_fetch
from app.crawler.publish import source_display_name, upsert_problem
from app.crawler.registry import Source, load_source
from app.crawler.report import CrawlReport
from app.db import normalized_database_url, session_scope
from app.models import (
    CrawlItem,
    CrawlRun,
    Problem,
    STATUS_PUBLISHED,
    utcnow,
)

MISSING_RUNS_BEFORE_CLOSED = 3


def _existing(db: Session, source: Source, item: DiscoveredItem) -> Problem | None:
    if not item.source_id:
        return None
    return db.scalar(
        select(Problem).where(
            Problem.source_name == source_display_name(source, item.year),
            Problem.source_id == item.source_id,
        )
    )


def _record_crawl_item(
    db: Session,
    source: Source,
    item: DiscoveredItem,
    *,
    action: str,
    problem_id: int | None,
    digest: str,
) -> None:
    key = f"{item.url}#{item.source_id}" if item.source_id else item.url
    row = db.scalar(select(CrawlItem).where(CrawlItem.url == key))
    if row is None:
        row = CrawlItem(source_key=source.key, url=key, updated_at=utcnow())
        db.add(row)
    row.source_key = source.key
    row.problem_id = problem_id
    row.last_status = action
    row.content_hash = digest
    row.updated_at = utcnow()


def _flag_missing(db: Session, source: Source, seen_ids: set[str]) -> None:
    """Never delete: after repeated absences, mark the statement closed (§6.5)."""
    problems = db.scalars(
        select(Problem).where(
            Problem.crawl_source_key == source.key,
            Problem.status == STATUS_PUBLISHED,
        )
    ).all()
    for problem in problems:
        if problem.source_id and problem.source_id in seen_ids:
            continue
        row = db.scalar(
            select(CrawlItem).where(
                CrawlItem.source_key == source.key,
                CrawlItem.problem_id == problem.id,
            )
        )
        previous = 0
        if row and (row.last_status or "").startswith("missing:"):
            try:
                previous = int((row.last_status or "").split(":", 1)[1])
            except ValueError:
                previous = 0
        misses = previous + 1
        if row is not None:
            row.last_status = f"missing:{misses}"
            row.updated_at = utcnow()
        if misses >= MISSING_RUNS_BEFORE_CLOSED and problem.source_status != "closed":
            problem.source_status = "closed"


async def run_source(
    key: str,
    *,
    db: Session,
    dry_run: bool = False,
    limit: int | None = None,
    triggered_by: str = "manual",
    today: date | None = None,
    client=None,
    resolve=None,
    sleep=None,
    call=None,
) -> CrawlReport:
    report = CrawlReport(source_key=key)
    if not crawler_config.enabled():
        report.log("skipped_compliance", reason="CRAWLER_ENABLED is false")
        report.add("skipped_compliance")
        return report
    try:
        user_agent = crawler_config.user_agent()
    except RuntimeError as exc:
        report.fail(key, str(exc))
        return report

    try:
        source = load_source(key)
    except (FileNotFoundError, ValueError) as exc:
        report.fail(key, str(exc))
        return report

    try:
        assert_compliant(source, today=today)
    except ComplianceError as exc:
        report.log("skipped_compliance", reason=str(exc))
        report.add("skipped_compliance")
        report.errors.append(str(exc))
        return report

    limits = crawler_config.limits()
    budget = Budget(max_llm_calls=limits.max_llm_calls)
    throttle = HostThrottle(source.politeness.min_delay_seconds, sleep=sleep or asyncio.sleep)

    async def fetch_robots(url: str) -> tuple[int, str]:
        result = await safe_fetch(
            url,
            client=client,
            resolve=resolve,
            throttle=throttle,
            user_agent=user_agent,
            max_bytes=200_000,
            allow_statuses={404},
            sleep=sleep or asyncio.sleep,
        )
        return result.status, result.text

    robots = RobotsCache(fetch_robots, user_agent)
    ctx = CrawlContext(
        source=source,
        robots=robots,
        throttle=throttle,
        user_agent=user_agent,
        max_bytes=source.politeness.max_bytes,
        resolve=resolve,
        client=client,
        sleep=sleep,
    )

    run_row = None
    if not dry_run:
        run_row = CrawlRun(source_key=key, triggered_by=triggered_by, counts={})
        db.add(run_row)
        db.flush()

    try:
        items = await discover(source, ctx)
    except RobotsDisallowed as exc:
        report.log("skipped_robots", reason=str(exc))
        report.add("skipped_robots")
        report.errors.append(str(exc))
        items = []
    except FetchError as exc:
        report.fail(key, str(exc))
        items = []

    report.counts["fetched"] += ctx.requests
    report.counts["discovered"] = len(items)
    cap = min(source.politeness.max_pages_per_run, limit or source.politeness.max_pages_per_run)
    seen_ids: set[str] = set()

    for index, item in enumerate(items[:cap]):
        report.cover(item.year, "found", item.source_id)
        if not item.source_id:
            report.cover(item.year, "missing_id", "?")
            report.fail(item.url, "missing deterministic source id")
            continue
        seen_ids.add(item.source_id)
        if (item.category or "").strip().lower() == "hardware":
            report.add("skipped_out_of_scope")
            report.cover(item.year, "out_of_scope_hardware", item.source_id)
            report.log("skipped_out_of_scope", url=item.url, source_id=item.source_id)
            continue
        try:
            await robots.check(item.url)
        except Exception as exc:  # pragma: no cover - check itself is defensive
            report.log("skipped_robots", url=item.url, reason=str(exc))
            report.add("skipped_robots")
            continue

        source_text = item.description or item.title or ""
        if not source_text.strip():
            report.cover(item.year, "no_text", item.source_id)
            report.fail(item.url, "no text to extract")
            continue

        digest = content_hash(source_text)
        existing = _existing(db, source, item)
        if existing is not None and existing.content_hash == digest:
            outcome = upsert_problem(db, source=source, item=item, extraction=None, digest=digest, dry_run=dry_run)  # type: ignore[arg-type]
            report.add("unchanged")
            report.cover(item.year, "ingested", item.source_id)
            if not dry_run:
                _record_crawl_item(db, source, item, action="unchanged", problem_id=outcome.problem_id, digest=digest)
            report.log("unchanged", url=item.url, source_id=item.source_id)
            continue

        try:
            budget.spend()
            extraction = await asyncio.to_thread(
                extract_draft, source=source, item=item, text=source_text, call=call
            )
        except BudgetExhausted:
            report.add("deferred")
            report.cover(item.year, "deferred", item.source_id)
            report.log("deferred", url=item.url, reason="LLM budget exhausted")
            for remaining in items[index + 1 : cap]:
                report.cover(remaining.year, "found", remaining.source_id)
                report.cover(remaining.year, "deferred", remaining.source_id)
            break
        except NoClearProblem:
            report.add("skipped_not_a_problem")
            report.cover(item.year, "not_a_problem", item.source_id)
            report.log("skipped_not_a_problem", url=item.url, source_id=item.source_id)
            continue
        except (ExtractionError, RuntimeError) as exc:
            report.cover(item.year, "failed_extraction", item.source_id)
            report.fail(item.url, str(exc))
            continue

        outcome = upsert_problem(
            db,
            source=source,
            item=item,
            extraction=extraction,
            digest=digest,
            dry_run=dry_run,
        )
        report.add(outcome.action)
        report.cover(item.year, "ingested", item.source_id)
        if outcome.status == STATUS_PUBLISHED:
            report.add("published")
        else:
            report.add("needs_review")
        if not dry_run:
            _record_crawl_item(
                db,
                source,
                item,
                action=outcome.action,
                problem_id=outcome.problem_id,
                digest=digest,
            )
        report.log(
            "published" if outcome.status == STATUS_PUBLISHED else "needs_review",
            url=item.url,
            source_id=item.source_id,
            action=outcome.action,
            confidence=extraction.confidence,
            note=outcome.note,
        )

    for item in items[cap:]:
        report.cover(item.year, "found", item.source_id)
        report.cover(item.year, "deferred", item.source_id)

    report.llm_calls = budget.used

    if not dry_run:
        _flag_missing(db, source, seen_ids)
        if run_row is not None:
            run_row.finished_at = utcnow()
            run_row.status = report.status()
            run_row.counts = dict(report.counts)
            run_row.llm_calls = report.llm_calls
            run_row.error_summary = "\n".join(report.errors[:20]) or None
        db.commit()
    return report


def _guard_env(env: str) -> str | None:
    database_url = normalized_database_url(get_settings().DATABASE_URL)
    if (env == "prod" or crawler_config.require_postgres()) and database_url.startswith("sqlite"):
        return "Refusing to crawl against SQLite in prod; set a Postgres DATABASE_URL"
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the MANABI crawler for one source")
    parser.add_argument("--source", required=True, help="registry key, e.g. sih-2026")
    parser.add_argument("--dry-run", action="store_true", help="fetch/extract but write nothing")
    parser.add_argument("--limit", type=int, default=None, help="cap pages this run")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev")
    args = parser.parse_args(argv)

    if not crawler_config.enabled():
        print("CRAWLER_ENABLED is false — refusing to crawl (kill switch).")
        return 0
    problem = _guard_env(args.env)
    if problem:
        print(problem, file=sys.stderr)
        return 2

    with session_scope() as db:
        report = asyncio.run(
            run_source(
                args.source,
                db=db,
                dry_run=args.dry_run,
                limit=args.limit,
                triggered_by="manual",
            )
        )
    markdown = report.to_markdown()
    print(markdown)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        Path(summary_path).write_text(markdown, encoding="utf-8")
    return 0 if report.status() == "success" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
