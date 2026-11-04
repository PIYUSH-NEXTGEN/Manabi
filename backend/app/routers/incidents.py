from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    Incident,
    IncidentEvent,
    IncidentAssignment,
    IncidentTimelineEntry,
    utcnow,
)

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


def _incident_out(inc: Incident) -> schemas.IncidentOut:
    return schemas.IncidentOut.model_validate(inc)


@router.get("", response_model=list[schemas.IncidentOut])
def list_incidents(db: DB, user: CurrentUser, status: str | None = Query(default=None), severity: str | None = Query(default=None)):
    query = select(Incident)
    if status:
        query = query.where(Incident.status == status)
    if severity:
        query = query.where(Incident.severity == severity)
    query = query.order_by(Incident.started_at.desc())
    rows = db.scalars(query).all()
    return [_incident_out(r) for r in rows]


@router.post("", response_model=schemas.IncidentOut, status_code=201)
def create_incident(body: schemas.IncidentCreate, user: CurrentUser, db: DB):
    inc = Incident(
        title=body.title.strip(),
        description=body.description.strip(),
        severity=body.severity,
        reporter_user_id=user.id,
        assignee_user_id=body.assignee_user_id,
        status="open",
        tags_json=body.tags,
        started_at=utcnow(),
    )
    db.add(inc)
    db.commit()
    db.refresh(inc)
    entry = IncidentTimelineEntry(
        incident_id=inc.id,
        title="Incident created",
        description=f"Incident created by {user.username}",
        entry_type="status_change",
        occurred_at=utcnow(),
        created_by_user_id=user.id,
    )
    db.add(entry)
    db.commit()
    return _incident_out(inc)


@router.get("/{incident_id}", response_model=schemas.IncidentOut)
def get_incident(incident_id: int, db: DB, user: CurrentUser):
    inc = db.scalar(
        select(Incident).options(
            selectinload(Incident.events),
            selectinload(Incident.assignments),
            selectinload(Incident.timeline_entries),
        ).where(Incident.id == incident_id)
    )
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return _incident_out(inc)


@router.patch("/{incident_id}", response_model=schemas.IncidentOut)
def update_incident(incident_id: int, body: schemas.IncidentUpdate, user: CurrentUser, db: DB):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    old_status = inc.status
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(inc, field, value)
    if body.status is not None and body.status != old_status:
        entry = IncidentTimelineEntry(
            incident_id=inc.id,
            title=f"Status changed to {body.status}",
            description=f"Status changed from {old_status} to {body.status} by {user.username}",
            entry_type="status_change",
            occurred_at=utcnow(),
            created_by_user_id=user.id,
        )
        db.add(entry)
        if body.status == "resolved" and inc.resolved_at is None:
            inc.resolved_at = utcnow()
        if body.status == "closed" and inc.closed_at is None:
            inc.closed_at = utcnow()
    db.commit()
    db.refresh(inc)
    return _incident_out(inc)


@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, user: CurrentUser, db: DB):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(inc)
    db.commit()
    return None


@router.post("/{incident_id}/events", response_model=schemas.IncidentEventOut, status_code=201)
def create_event(incident_id: int, body: schemas.IncidentEventCreate, user: CurrentUser, db: DB):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    event = IncidentEvent(
        incident_id=incident_id,
        source=body.source,
        source_id=body.source_id,
        event_type=body.event_type,
        payload_json=body.payload,
        occurred_at=body.occurred_at,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return schemas.IncidentEventOut.model_validate(event)


@router.get("/{incident_id}/events", response_model=list[schemas.IncidentEventOut])
def list_events(incident_id: int, db: DB, user: CurrentUser):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    rows = db.scalars(
        select(IncidentEvent).where(IncidentEvent.incident_id == incident_id).order_by(IncidentEvent.occurred_at.asc())
    ).all()
    return [schemas.IncidentEventOut.model_validate(r) for r in rows]


@router.post("/{incident_id}/assignments", response_model=schemas.IncidentAssignmentOut, status_code=201)
def create_assignment(incident_id: int, body: schemas.IncidentAssignmentCreate, user: CurrentUser, db: DB):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    assignment = IncidentAssignment(
        incident_id=incident_id,
        user_id=body.user_id,
        role=body.role,
        assigned_at=utcnow(),
    )
    db.add(assignment)
    if body.role == "incident_commander":
        inc.assignee_user_id = body.user_id
    db.commit()
    db.refresh(assignment)
    return schemas.IncidentAssignmentOut.model_validate(assignment)


@router.get("/{incident_id}/assignments", response_model=list[schemas.IncidentAssignmentOut])
def list_assignments(incident_id: int, db: DB, user: CurrentUser):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    rows = db.scalars(
        select(IncidentAssignment).where(IncidentAssignment.incident_id == incident_id).order_by(IncidentAssignment.assigned_at.desc())
    ).all()
    return [schemas.IncidentAssignmentOut.model_validate(r) for r in rows]


@router.post("/{incident_id}/timeline", response_model=schemas.IncidentTimelineEntryOut, status_code=201)
def create_timeline_entry(incident_id: int, body: schemas.IncidentTimelineEntryCreate, user: CurrentUser, db: DB):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    entry = IncidentTimelineEntry(
        incident_id=incident_id,
        title=body.title.strip(),
        description=body.description,
        entry_type=body.entry_type,
        occurred_at=body.occurred_at,
        created_by_user_id=body.created_by_user_id or user.id,
        metadata_json=body.metadata,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return schemas.IncidentTimelineEntryOut.model_validate(entry)


@router.get("/{incident_id}/timeline", response_model=list[schemas.IncidentTimelineEntryOut])
def list_timeline(incident_id: int, db: DB, user: CurrentUser):
    inc = db.scalar(select(Incident).where(Incident.id == incident_id))
    if inc is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    rows = db.scalars(
        select(IncidentTimelineEntry)
        .where(IncidentTimelineEntry.incident_id == incident_id)
        .order_by(IncidentTimelineEntry.occurred_at.asc())
    ).all()
    return [schemas.IncidentTimelineEntryOut.model_validate(r) for r in rows]


@router.get("/stats/summary")
def incident_stats(db: DB):
    total = db.scalar(select(func.count(Incident.id))) or 0
    open_count = db.scalar(select(func.count(Incident.id)).where(Incident.status == "open")) or 0
    investigating = db.scalar(select(func.count(Incident.id)).where(Incident.status == "investigating")) or 0
    resolved = db.scalar(select(func.count(Incident.id)).where(Incident.status == "resolved")) or 0
    critical = db.scalar(select(func.count(Incident.id)).where(Incident.severity == "critical")) or 0
    return {
        "total_incidents": int(total),
        "open": int(open_count),
        "investigating": int(investigating),
        "resolved": int(resolved),
        "critical": int(critical),
    }
