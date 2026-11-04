from datetime import date

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    AnalyticsEvent,
    ConsentRecord,
    DataRetentionPolicy,
    FunnelDefinition,
    RetentionCohort,
    CONSENT_GRANTED,
    CONSENT_DENIED,
    CONSENT_UNKNOWN,
    utcnow,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.post("/events", response_model=schemas.AnalyticsEventOut, status_code=201)
def ingest_event(body: schemas.AnalyticsEventCreate, db: DB):
    consent = db.scalar(select(ConsentRecord).where(ConsentRecord.anonymous_id == body.anonymous_id))
    if consent is not None and consent.consent_status == CONSENT_DENIED:
        raise HTTPException(status_code=403, detail="Consent denied for this user")
    event = AnalyticsEvent(
        project_id=body.project_id.strip(),
        session_id=body.session_id.strip(),
        anonymous_id=body.anonymous_id.strip(),
        event_name=body.event_name.strip(),
        event_properties_json=body.event_properties,
        user_properties_json=body.user_properties,
        timestamp=body.timestamp,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return schemas.AnalyticsEventOut.model_validate(event)


@router.get("/events", response_model=list[schemas.AnalyticsEventOut])
def list_events(
    db: DB,
    project_id: str = Query(...),
    event_name: str | None = Query(default=None),
    anonymous_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
):
    query = select(AnalyticsEvent).where(AnalyticsEvent.project_id == project_id)
    if event_name:
        query = query.where(AnalyticsEvent.event_name == event_name)
    if anonymous_id:
        query = query.where(AnalyticsEvent.anonymous_id == anonymous_id)
    query = query.order_by(AnalyticsEvent.timestamp.desc()).limit(limit)
    rows = db.scalars(query).all()
    return [schemas.AnalyticsEventOut.model_validate(r) for r in rows]


@router.get("/events/count")
def event_count(db: DB, project_id: str = Query(...), event_name: str | None = Query(default=None)):
    query = select(func.count(AnalyticsEvent.id)).where(AnalyticsEvent.project_id == project_id)
    if event_name:
        query = query.where(AnalyticsEvent.event_name == event_name)
    total = db.scalar(query) or 0
    return {"project_id": project_id, "event_name": event_name, "count": int(total)}


@router.post("/consent", response_model=schemas.ConsentRecordOut, status_code=201)
def set_consent(body: schemas.ConsentRecordCreate, db: DB):
    existing = db.scalar(select(ConsentRecord).where(ConsentRecord.anonymous_id == body.anonymous_id))
    if existing is not None:
        existing.consent_status = body.consent_status
        existing.consent_version = body.consent_version
        db.commit()
        db.refresh(existing)
        return schemas.ConsentRecordOut.model_validate(existing)
    record = ConsentRecord(
        anonymous_id=body.anonymous_id.strip(),
        consent_status=body.consent_status,
        consent_version=body.consent_version,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return schemas.ConsentRecordOut.model_validate(record)


@router.get("/consent/{anonymous_id}", response_model=schemas.ConsentRecordOut)
def get_consent(anonymous_id: str, db: DB):
    record = db.scalar(select(ConsentRecord).where(ConsentRecord.anonymous_id == anonymous_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Consent record not found")
    return schemas.ConsentRecordOut.model_validate(record)


@router.patch("/consent/{anonymous_id}", response_model=schemas.ConsentRecordOut)
def update_consent(anonymous_id: str, body: schemas.ConsentRecordUpdate, db: DB):
    record = db.scalar(select(ConsentRecord).where(ConsentRecord.anonymous_id == anonymous_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Consent record not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return schemas.ConsentRecordOut.model_validate(record)


@router.post("/retention-policies", response_model=schemas.DataRetentionPolicyOut, status_code=201)
def create_retention_policy(body: schemas.DataRetentionPolicyCreate, user: CurrentUser, db: DB):
    existing = db.scalar(select(DataRetentionPolicy).where(DataRetentionPolicy.project_id == body.project_id))
    if existing is not None:
        raise HTTPException(status_code=409, detail="Retention policy already exists for this project")
    policy = DataRetentionPolicy(
        project_id=body.project_id.strip(),
        event_retention_days=body.event_retention_days,
        raw_data_retention_days=body.raw_data_retention_days,
        is_active=body.is_active,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return schemas.DataRetentionPolicyOut.model_validate(policy)


@router.get("/retention-policies", response_model=list[schemas.DataRetentionPolicyOut])
def list_retention_policies(db: DB):
    rows = db.scalars(select(DataRetentionPolicy).order_by(DataRetentionPolicy.created_at.desc())).all()
    return [schemas.DataRetentionPolicyOut.model_validate(r) for r in rows]


@router.patch("/retention-policies/{policy_id}", response_model=schemas.DataRetentionPolicyOut)
def update_retention_policy(policy_id: int, body: schemas.DataRetentionPolicyUpdate, user: CurrentUser, db: DB):
    policy = db.scalar(select(DataRetentionPolicy).where(DataRetentionPolicy.id == policy_id))
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(policy, field, value)
    db.commit()
    db.refresh(policy)
    return schemas.DataRetentionPolicyOut.model_validate(policy)


@router.post("/funnels", response_model=schemas.FunnelDefinitionOut, status_code=201)
def create_funnel(body: schemas.FunnelDefinitionCreate, user: CurrentUser, db: DB):
    funnel = FunnelDefinition(
        project_id=body.project_id.strip(),
        name=body.name.strip(),
        steps_json=body.steps,
    )
    db.add(funnel)
    db.commit()
    db.refresh(funnel)
    return schemas.FunnelDefinitionOut.model_validate(funnel)


@router.get("/funnels", response_model=list[schemas.FunnelDefinitionOut])
def list_funnels(db: DB, project_id: str | None = Query(default=None)):
    query = select(FunnelDefinition)
    if project_id:
        query = query.where(FunnelDefinition.project_id == project_id)
    rows = db.scalars(query.order_by(FunnelDefinition.created_at.desc())).all()
    return [schemas.FunnelDefinitionOut.model_validate(r) for r in rows]


@router.get("/retention-cohorts", response_model=list[schemas.RetentionCohortOut])
def list_retention_cohorts(db: DB, project_id: str = Query(...)):
    rows = db.scalars(
        select(RetentionCohort).where(RetentionCohort.project_id == project_id).order_by(RetentionCohort.cohort_date.desc())
    ).all()
    return [schemas.RetentionCohortOut.model_validate(r) for r in rows]


@router.post("/retention-cohorts", response_model=schemas.RetentionCohortOut, status_code=201)
def create_retention_cohort(body: schemas.RetentionCohortCreate, user: CurrentUser, db: DB):
    cohort = RetentionCohort(
        project_id=body.project_id.strip(),
        cohort_date=body.cohort_date,
        cohort_size=body.cohort_size,
        retention_json=body.retention,
    )
    db.add(cohort)
    db.commit()
    db.refresh(cohort)
    return schemas.RetentionCohortOut.model_validate(cohort)


@router.get("/stats/summary")
def analytics_stats(db: DB):
    total_events = db.scalar(select(func.count(AnalyticsEvent.id))) or 0
    total_projects = db.scalar(select(func.count(func.distinct(AnalyticsEvent.project_id)))) or 0
    granted_consent = db.scalar(select(func.count(ConsentRecord.id)).where(ConsentRecord.consent_status == CONSENT_GRANTED)) or 0
    denied_consent = db.scalar(select(func.count(ConsentRecord.id)).where(ConsentRecord.consent_status == CONSENT_DENIED)) or 0
    return {
        "total_events": int(total_events),
        "total_projects": int(total_projects),
        "granted_consent": int(granted_consent),
        "denied_consent": int(denied_consent),
    }
