from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    IngestionJob,
    IngestedFile,
    ProcessingWorker,
    utcnow,
)

router = APIRouter(prefix="/api/ingestion", tags=["ingestion"])


def _job_out(job: IngestionJob) -> schemas.IngestionJobOut:
    return schemas.IngestionJobOut.model_validate(job)


@router.get("/jobs", response_model=list[schemas.IngestionJobOut])
def list_jobs(db: DB, user: CurrentUser, status: str | None = Query(default=None)):
    query = select(IngestionJob).where(IngestionJob.user_id == user.id)
    if status:
        query = query.where(IngestionJob.status == status)
    query = query.order_by(IngestionJob.created_at.desc())
    rows = db.scalars(query).all()
    return [_job_out(r) for r in rows]


@router.post("/jobs", response_model=schemas.IngestionJobOut, status_code=201)
def create_job(body: schemas.IngestionJobCreate, user: CurrentUser, db: DB):
    job = IngestionJob(
        user_id=user.id,
        name=body.name.strip(),
        status="pending",
        config_json=body.config,
        created_at=utcnow(),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return _job_out(job)


@router.get("/jobs/{job_id}", response_model=schemas.IngestionJobOut)
def get_job(job_id: int, user: CurrentUser, db: DB):
    job = db.scalar(
        select(IngestionJob).where(IngestionJob.id == job_id, IngestionJob.user_id == user.id)
    )
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return _job_out(job)


@router.patch("/jobs/{job_id}", response_model=schemas.IngestionJobOut)
def update_job(job_id: int, body: schemas.IngestionJobUpdate, user: CurrentUser, db: DB):
    job = db.scalar(
        select(IngestionJob).where(IngestionJob.id == job_id, IngestionJob.user_id == user.id)
    )
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return _job_out(job)


@router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, user: CurrentUser, db: DB):
    job = db.scalar(
        select(IngestionJob).where(IngestionJob.id == job_id, IngestionJob.user_id == user.id)
    )
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return None


@router.post("/jobs/{job_id}/files", response_model=schemas.IngestedFileOut, status_code=201)
def add_file(job_id: int, body: schemas.IngestedFileCreate, user: CurrentUser, db: DB):
    job = db.scalar(
        select(IngestionJob).where(IngestionJob.id == job_id, IngestionJob.user_id == user.id)
    )
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    existing = db.scalar(
        select(IngestedFile).where(IngestedFile.content_hash == body.content_hash, IngestedFile.job_id == job_id)
    ) if body.content_hash else None
    is_duplicate = existing is not None
    file = IngestedFile(
        job_id=job_id,
        original_filename=body.original_filename.strip(),
        stored_path=body.stored_path.strip(),
        content_hash=body.content_hash,
        file_size=body.file_size,
        mime_type=body.mime_type,
        status="pending",
        validation_errors_json=[],
        is_duplicate=is_duplicate,
        duplicate_of_file_id=existing.id if existing else None,
        created_at=utcnow(),
    )
    if is_duplicate:
        job.skipped_duplicates = (job.skipped_duplicates or 0) + 1
    else:
        job.total_files = (job.total_files or 0) + 1
    db.add(file)
    db.commit()
    db.refresh(file)
    return schemas.IngestedFileOut.model_validate(file)


@router.get("/jobs/{job_id}/files", response_model=list[schemas.IngestedFileOut])
def list_files(job_id: int, user: CurrentUser, db: DB):
    job = db.scalar(
        select(IngestionJob).where(IngestionJob.id == job_id, IngestionJob.user_id == user.id)
    )
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    rows = db.scalars(
        select(IngestedFile).where(IngestedFile.job_id == job_id).order_by(IngestedFile.created_at.desc())
    ).all()
    return [schemas.IngestedFileOut.model_validate(r) for r in rows]


@router.patch("/files/{file_id}", response_model=schemas.IngestedFileOut)
def update_file(file_id: int, body: schemas.IngestedFileBase, user: CurrentUser, db: DB):
    file = db.scalar(
        select(IngestedFile).join(IngestionJob).where(IngestedFile.id == file_id, IngestionJob.user_id == user.id)
    )
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(file, field, value)
    db.commit()
    db.refresh(file)
    return schemas.IngestedFileOut.model_validate(file)


@router.post("/workers", response_model=schemas.ProcessingWorkerOut, status_code=201)
def create_worker(body: schemas.ProcessingWorkerCreate, user: CurrentUser, db: DB):
    existing = db.scalar(select(ProcessingWorker).where(ProcessingWorker.worker_name == body.worker_name))
    if existing is not None:
        raise HTTPException(status_code=409, detail="Worker already exists")
    worker = ProcessingWorker(worker_name=body.worker_name.strip(), status=body.status)
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return schemas.ProcessingWorkerOut.model_validate(worker)


@router.get("/workers", response_model=list[schemas.ProcessingWorkerOut])
def list_workers(db: DB):
    rows = db.scalars(select(ProcessingWorker).order_by(ProcessingWorker.created_at.desc())).all()
    return [schemas.ProcessingWorkerOut.model_validate(r) for r in rows]


@router.patch("/workers/{worker_id}", response_model=schemas.ProcessingWorkerOut)
def update_worker(worker_id: int, body: schemas.ProcessingWorkerBase, user: CurrentUser, db: DB):
    worker = db.scalar(select(ProcessingWorker).where(ProcessingWorker.id == worker_id))
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(worker, field, value)
    db.commit()
    db.refresh(worker)
    return schemas.ProcessingWorkerOut.model_validate(worker)


@router.get("/stats/summary")
def ingestion_stats(db: DB, user: CurrentUser):
    total_jobs = db.scalar(select(func.count(IngestionJob.id)).where(IngestionJob.user_id == user.id)) or 0
    total_files = db.scalar(
        select(func.count(IngestedFile.id)).join(IngestionJob).where(IngestionJob.user_id == user.id)
    ) or 0
    duplicate_files = db.scalar(
        select(func.count(IngestedFile.id))
        .join(IngestionJob)
        .where(IngestionJob.user_id == user.id, IngestedFile.is_duplicate == True)
    ) or 0
    pending_jobs = db.scalar(
        select(func.count(IngestionJob.id)).where(IngestionJob.user_id == user.id, IngestionJob.status == "pending")
    ) or 0
    return {
        "total_jobs": int(total_jobs),
        "pending_jobs": int(pending_jobs),
        "total_files": int(total_files),
        "duplicate_files": int(duplicate_files),
    }
