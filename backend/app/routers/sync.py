from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    SyncRecord,
    SyncConflict,
    SYNC_RECORD_STATUS_PENDING,
    SYNC_RECORD_STATUS_SYNCED,
    SYNC_RECORD_STATUS_CONFLICT,
    SYNC_RECORD_STATUS_RESOLVED,
    SYNC_RECORD_STATUS_FAILED,
    utcnow,
)

router = APIRouter(prefix="/api/sync", tags=["sync"])


@router.post("/records", response_model=schemas.SyncRecordOut, status_code=201)
def create_sync_record(body: schemas.SyncRecordCreate, db: DB):
    existing = db.scalar(
        select(SyncRecord).where(
            SyncRecord.device_id == body.device_id,
            SyncRecord.collection == body.collection,
            SyncRecord.record_id == body.record_id,
        )
    )
    if existing is not None:
        existing.version_vector_json = body.version_vector
        existing.data_json = body.data
        existing.operation = body.operation
        existing.status = SYNC_RECORD_STATUS_PENDING
        existing.updated_at = utcnow()
        db.commit()
        db.refresh(existing)
        return schemas.SyncRecordOut.model_validate(existing)
    record = SyncRecord(
        device_id=body.device_id.strip(),
        collection=body.collection.strip(),
        record_id=body.record_id.strip(),
        version_vector_json=body.version_vector,
        data_json=body.data,
        operation=body.operation,
        status=SYNC_RECORD_STATUS_PENDING,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return schemas.SyncRecordOut.model_validate(record)


@router.get("/records", response_model=list[schemas.SyncRecordOut])
def list_sync_records(
    db: DB,
    device_id: str | None = Query(default=None),
    collection: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
):
    query = select(SyncRecord)
    if device_id:
        query = query.where(SyncRecord.device_id == device_id)
    if collection:
        query = query.where(SyncRecord.collection == collection)
    if status:
        query = query.where(SyncRecord.status == status)
    query = query.order_by(SyncRecord.updated_at.desc()).limit(limit)
    rows = db.scalars(query).all()
    return [schemas.SyncRecordOut.model_validate(r) for r in rows]


@router.get("/records/{record_id}", response_model=schemas.SyncRecordOut)
def get_sync_record(record_id: int, db: DB):
    record = db.scalar(select(SyncRecord).where(SyncRecord.id == record_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Sync record not found")
    return schemas.SyncRecordOut.model_validate(record)


@router.patch("/records/{record_id}", response_model=schemas.SyncRecordOut)
def update_sync_record(record_id: int, body: schemas.SyncRecordUpdate, db: DB):
    record = db.scalar(select(SyncRecord).where(SyncRecord.id == record_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Sync record not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return schemas.SyncRecordOut.model_validate(record)


@router.post("/records/{record_id}/sync", response_model=schemas.SyncRecordOut)
def mark_synced(record_id: int, db: DB):
    record = db.scalar(select(SyncRecord).where(SyncRecord.id == record_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Sync record not found")
    record.status = SYNC_RECORD_STATUS_SYNCED
    record.synced_at = utcnow()
    db.commit()
    db.refresh(record)
    return schemas.SyncRecordOut.model_validate(record)


@router.post("/records/{record_id}/conflict", response_model=schemas.SyncRecordOut)
def mark_conflict(record_id: int, conflict_with_record_id: str, db: DB):
    record = db.scalar(select(SyncRecord).where(SyncRecord.id == record_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Sync record not found")
    record.status = SYNC_RECORD_STATUS_CONFLICT
    record.conflict_with_record_id = conflict_with_record_id
    conflict = SyncConflict(
        collection=record.collection,
        record_id=record.record_id,
        local_version_json=record.data_json,
        remote_version_json={},
        local_vector_json=record.version_vector_json,
        remote_vector_json={},
        status="open",
    )
    db.add(conflict)
    db.commit()
    db.refresh(record)
    return schemas.SyncRecordOut.model_validate(record)


@router.get("/conflicts", response_model=list[schemas.SyncConflictOut])
def list_conflicts(db: DB, collection: str | None = Query(default=None), status: str | None = Query(default=None)):
    query = select(SyncConflict)
    if collection:
        query = query.where(SyncConflict.collection == collection)
    if status:
        query = query.where(SyncConflict.status == status)
    query = query.order_by(SyncConflict.created_at.desc())
    rows = db.scalars(query).all()
    return [schemas.SyncConflictOut.model_validate(r) for r in rows]


@router.get("/conflicts/{conflict_id}", response_model=schemas.SyncConflictOut)
def get_conflict(conflict_id: int, db: DB):
    conflict = db.scalar(select(SyncConflict).where(SyncConflict.id == conflict_id))
    if conflict is None:
        raise HTTPException(status_code=404, detail="Conflict not found")
    return schemas.SyncConflictOut.model_validate(conflict)


@router.patch("/conflicts/{conflict_id}", response_model=schemas.SyncConflictOut)
def resolve_conflict(conflict_id: int, body: schemas.SyncConflictUpdate, db: DB):
    conflict = db.scalar(select(SyncConflict).where(SyncConflict.id == conflict_id))
    if conflict is None:
        raise HTTPException(status_code=404, detail="Conflict not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(conflict, field, value)
    if body.status == "resolved" and conflict.resolved_at is None:
        conflict.resolved_at = utcnow()
    if body.resolved_data is not None:
        conflict.resolved_data_json = body.resolved_data
    db.commit()
    db.refresh(conflict)
    return schemas.SyncConflictOut.model_validate(conflict)


@router.delete("/conflicts/{conflict_id}", status_code=204)
def delete_conflict(conflict_id: int, db: DB):
    conflict = db.scalar(select(SyncConflict).where(SyncConflict.id == conflict_id))
    if conflict is None:
        raise HTTPException(status_code=404, detail="Conflict not found")
    db.delete(conflict)
    db.commit()
    return None


@router.get("/stats/summary")
def sync_stats(db: DB):
    total_records = db.scalar(select(func.count(SyncRecord.id))) or 0
    pending = db.scalar(select(func.count(SyncRecord.id)).where(SyncRecord.status == SYNC_RECORD_STATUS_PENDING)) or 0
    synced = db.scalar(select(func.count(SyncRecord.id)).where(SyncRecord.status == SYNC_RECORD_STATUS_SYNCED)) or 0
    conflicts = db.scalar(select(func.count(SyncRecord.id)).where(SyncRecord.status == SYNC_RECORD_STATUS_CONFLICT)) or 0
    open_conflicts = db.scalar(select(func.count(SyncConflict.id)).where(SyncConflict.status == "open")) or 0
    return {
        "total_records": int(total_records),
        "pending": int(pending),
        "synced": int(synced),
        "conflicts": int(conflicts),
        "open_conflicts": int(open_conflicts),
    }
