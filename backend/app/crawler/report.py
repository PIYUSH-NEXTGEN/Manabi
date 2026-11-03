"""Per-run counters, structured log lines, and the Actions markdown summary (§10)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

COUNTERS = (
    "discovered",
    "fetched",
    "unchanged",
    "new",
    "updated",
    "skipped_robots",
    "skipped_compliance",
    "skipped_out_of_scope",
    "skipped_not_a_problem",
    "failed",
    "needs_review",
    "published",
    "deferred",
)


@dataclass
class CrawlReport:
    source_key: str
    counts: dict[str, int] = field(default_factory=lambda: {key: 0 for key in COUNTERS})
    coverage: dict[int, dict] = field(default_factory=dict)
    llm_calls: int = 0
    errors: list[str] = field(default_factory=list)

    def add(self, counter: str, amount: int = 1) -> None:
        self.counts[counter] = self.counts.get(counter, 0) + amount

    def cover(self, year: int | None, status: str, source_id: str | None = None) -> None:
        bucket = self.coverage.setdefault(year or 0, {"found": 0, "ingested": 0, "skipped": {}})
        if status == "found":
            bucket["found"] += 1
        elif status == "ingested":
            bucket["ingested"] += 1
        else:
            bucket["skipped"].setdefault(status, []).append(source_id or "?")

    def fail(self, url: str, reason: str) -> None:
        self.add("failed")
        self.errors.append(f"{url}: {reason}")
        self.log("failed", url=url, reason=reason)

    def log(self, decision: str, **fields) -> None:
        print(json.dumps({"source": self.source_key, "decision": decision, **fields}, ensure_ascii=False))

    def status(self) -> str:
        return "failed" if self.errors and not any(self.counts[k] for k in ("new", "updated", "unchanged", "published")) else "success"

    def to_markdown(self) -> str:
        lines = [f"## Crawl report — `{self.source_key}`", ""]
        lines.append(f"- LLM calls: {self.llm_calls}")
        for key in COUNTERS:
            lines.append(f"- {key}: {self.counts[key]}")
        if self.coverage:
            lines += ["", "### Coverage per year", ""]
            for year in sorted(self.coverage):
                bucket = self.coverage[year]
                label = str(year) if year else "unknown"
                skipped = sum(len(ids) for ids in bucket["skipped"].values())
                lines.append(
                    f"- {label}: found {bucket['found']}, ingested {bucket['ingested']}, skipped {skipped}"
                )
                for reason, ids in sorted(bucket["skipped"].items()):
                    lines.append(f"  - {reason}: {', '.join(ids[:40])}" + (" …" if len(ids) > 40 else ""))
        if self.errors:
            lines += ["", "### Errors"] + [f"- `{error}`" for error in self.errors[:50]]
        return "\n".join(lines) + "\n"
