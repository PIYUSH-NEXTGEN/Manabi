from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    MonitoredWebsite,
    AccessibilityScan,
    AccessibilityIssue,
    utcnow,
)

router = APIRouter(prefix="/api/accessibility", tags=["accessibility"])


def _website_out(w: MonitoredWebsite) -> schemas.MonitoredWebsiteOut:
    return schemas.MonitoredWebsiteOut.model_validate(w)


@router.get("/websites", response_model=list[schemas.MonitoredWebsiteOut])
def list_websites(db: DB, user: CurrentUser, is_active: bool | None = Query(default=None)):
    query = select(MonitoredWebsite).where(MonitoredWebsite.user_id == user.id)
    if is_active is not None:
        query = query.where(MonitoredWebsite.is_active == is_active)
    query = query.order_by(MonitoredWebsite.created_at.desc())
    rows = db.scalars(query).all()
    return [_website_out(r) for r in rows]


@router.post("/websites", response_model=schemas.MonitoredWebsiteOut, status_code=201)
def create_website(body: schemas.MonitoredWebsiteCreate, user: CurrentUser, db: DB):
    website = MonitoredWebsite(
        user_id=user.id,
        name=body.name.strip(),
        url=str(body.url).strip(),
        scan_interval_minutes=body.scan_interval_minutes,
        wcag_level=body.wcag_level,
        is_active=body.is_active,
    )
    db.add(website)
    db.commit()
    db.refresh(website)
    return _website_out(website)


@router.get("/websites/{website_id}", response_model=schemas.MonitoredWebsiteOut)
def get_website(website_id: int, user: CurrentUser, db: DB):
    website = db.scalar(
        select(MonitoredWebsite).where(MonitoredWebsite.id == website_id, MonitoredWebsite.user_id == user.id)
    )
    if website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    return _website_out(website)


@router.patch("/websites/{website_id}", response_model=schemas.MonitoredWebsiteOut)
def update_website(website_id: int, body: schemas.MonitoredWebsiteUpdate, user: CurrentUser, db: DB):
    website = db.scalar(
        select(MonitoredWebsite).where(MonitoredWebsite.id == website_id, MonitoredWebsite.user_id == user.id)
    )
    if website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(website, field, str(value).strip() if field == "url" and isinstance(value, str) else value)
    db.commit()
    db.refresh(website)
    return _website_out(website)


@router.delete("/websites/{website_id}", status_code=204)
def delete_website(website_id: int, user: CurrentUser, db: DB):
    website = db.scalar(
        select(MonitoredWebsite).where(MonitoredWebsite.id == website_id, MonitoredWebsite.user_id == user.id)
    )
    if website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    db.delete(website)
    db.commit()
    return None


@router.post("/websites/{website_id}/scans", response_model=schemas.AccessibilityScanOut, status_code=201)
def create_scan(website_id: int, body: schemas.AccessibilityScanCreate, user: CurrentUser, db: DB):
    website = db.scalar(
        select(MonitoredWebsite).where(MonitoredWebsite.id == website_id, MonitoredWebsite.user_id == user.id)
    )
    if website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    scan = AccessibilityScan(
        website_id=website_id,
        status="pending",
        wcag_level=body.wcag_level,
        pages_scanned=0,
        issues_found=0,
        summary_json={},
        started_at=utcnow(),
    )
    db.add(scan)
    website.last_scan_at = utcnow()
    db.commit()
    db.refresh(scan)
    return schemas.AccessibilityScanOut.model_validate(scan)


@router.get("/websites/{website_id}/scans", response_model=list[schemas.AccessibilityScanOut])
def list_scans(website_id: int, user: CurrentUser, db: DB, limit: int = Query(default=50, ge=1, le=200)):
    website = db.scalar(
        select(MonitoredWebsite).where(MonitoredWebsite.id == website_id, MonitoredWebsite.user_id == user.id)
    )
    if website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    rows = db.scalars(
        select(AccessibilityScan)
        .where(AccessibilityScan.website_id == website_id)
        .order_by(AccessibilityScan.started_at.desc())
        .limit(limit)
    ).all()
    return [schemas.AccessibilityScanOut.model_validate(r) for r in rows]


@router.get("/scans/{scan_id}", response_model=schemas.AccessibilityScanOut)
def get_scan(scan_id: int, user: CurrentUser, db: DB):
    scan = db.scalar(
        select(AccessibilityScan)
        .join(MonitoredWebsite)
        .where(AccessibilityScan.id == scan_id, MonitoredWebsite.user_id == user.id)
    )
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return schemas.AccessibilityScanOut.model_validate(scan)


@router.patch("/scans/{scan_id}", response_model=schemas.AccessibilityScanOut)
def update_scan(scan_id: int, body: schemas.AccessibilityScanBase, user: CurrentUser, db: DB):
    scan = db.scalar(
        select(AccessibilityScan)
        .join(MonitoredWebsite)
        .where(AccessibilityScan.id == scan_id, MonitoredWebsite.user_id == user.id)
    )
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(scan, field, value)
    db.commit()
    db.refresh(scan)
    return schemas.AccessibilityScanOut.model_validate(scan)


@router.post("/scans/{scan_id}/issues", response_model=schemas.AccessibilityIssueOut, status_code=201)
def create_issue(scan_id: int, body: schemas.AccessibilityIssueCreate, user: CurrentUser, db: DB):
    scan = db.scalar(
        select(AccessibilityScan)
        .join(MonitoredWebsite)
        .where(AccessibilityScan.id == scan_id, MonitoredWebsite.user_id == user.id)
    )
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    issue = AccessibilityIssue(
        scan_id=scan_id,
        page_url=str(body.page_url).strip(),
        component_selector=body.component_selector,
        rule_id=body.rule_id.strip(),
        rule_name=body.rule_name.strip(),
        wcag_level=body.wcag_level,
        severity=body.severity,
        description=body.description.strip(),
        remediation=body.remediation,
        element_html=body.element_html,
        is_resolved=False,
    )
    scan.issues_found = (scan.issues_found or 0) + 1
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return schemas.AccessibilityIssueOut.model_validate(issue)


@router.get("/scans/{scan_id}/issues", response_model=list[schemas.AccessibilityIssueOut])
def list_issues(scan_id: int, user: CurrentUser, db: DB, severity: str | None = Query(default=None), is_resolved: bool | None = Query(default=None)):
    scan = db.scalar(
        select(AccessibilityScan)
        .join(MonitoredWebsite)
        .where(AccessibilityScan.id == scan_id, MonitoredWebsite.user_id == user.id)
    )
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    query = select(AccessibilityIssue).where(AccessibilityIssue.scan_id == scan_id)
    if severity:
        query = query.where(AccessibilityIssue.severity == severity)
    if is_resolved is not None:
        query = query.where(AccessibilityIssue.is_resolved == is_resolved)
    query = query.order_by(AccessibilityIssue.detected_at.desc())
    rows = db.scalars(query).all()
    return [schemas.AccessibilityIssueOut.model_validate(r) for r in rows]


@router.patch("/issues/{issue_id}", response_model=schemas.AccessibilityIssueOut)
def update_issue(issue_id: int, body: schemas.AccessibilityIssueBase, user: CurrentUser, db: DB):
    issue = db.scalar(
        select(AccessibilityIssue)
        .join(AccessibilityScan)
        .join(MonitoredWebsite)
        .where(AccessibilityIssue.id == issue_id, MonitoredWebsite.user_id == user.id)
    )
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(issue, field, str(value).strip() if isinstance(value, str) else value)
    db.commit()
    db.refresh(issue)
    return schemas.AccessibilityIssueOut.model_validate(issue)


@router.get("/stats/summary")
def accessibility_stats(db: DB, user: CurrentUser):
    total_websites = db.scalar(
        select(func.count(MonitoredWebsite.id)).where(MonitoredWebsite.user_id == user.id)
    ) or 0
    total_scans = db.scalar(
        select(func.count(AccessibilityScan.id)).join(MonitoredWebsite).where(MonitoredWebsite.user_id == user.id)
    ) or 0
    total_issues = db.scalar(
        select(func.count(AccessibilityIssue.id))
        .join(AccessibilityScan)
        .join(MonitoredWebsite)
        .where(MonitoredWebsite.user_id == user.id)
    ) or 0
    unresolved_issues = db.scalar(
        select(func.count(AccessibilityIssue.id))
        .join(AccessibilityScan)
        .join(MonitoredWebsite)
        .where(MonitoredWebsite.user_id == user.id, AccessibilityIssue.is_resolved == False)
    ) or 0
    return {
        "total_websites": int(total_websites),
        "total_scans": int(total_scans),
        "total_issues": int(total_issues),
        "unresolved_issues": int(unresolved_issues),
    }
