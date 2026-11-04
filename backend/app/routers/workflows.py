from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    Workflow,
    WorkflowExecution,
    WorkflowStepExecution,
    WORKFLOW_STATUS_DRAFT,
    WORKFLOW_STATUS_ACTIVE,
    EXECUTION_STATUS_PENDING,
    STEP_STATUS_PENDING,
    utcnow,
)

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


def _workflow_out(w: Workflow) -> schemas.WorkflowOut:
    return schemas.WorkflowOut.model_validate(w)


@router.get("", response_model=list[schemas.WorkflowOut])
def list_workflows(db: DB, user: CurrentUser, status: str | None = Query(default=None)):
    query = select(Workflow).where(Workflow.user_id == user.id)
    if status:
        query = query.where(Workflow.status == status)
    query = query.order_by(Workflow.updated_at.desc())
    rows = db.scalars(query).all()
    return [_workflow_out(r) for r in rows]


@router.post("", response_model=schemas.WorkflowOut, status_code=201)
def create_workflow(body: schemas.WorkflowCreate, user: CurrentUser, db: DB):
    workflow = Workflow(
        user_id=user.id,
        name=body.name.strip(),
        description=body.description,
        definition_json=body.definition,
        status=WORKFLOW_STATUS_DRAFT,
        trigger_type=body.trigger_type,
        trigger_config_json=body.trigger_config,
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return _workflow_out(workflow)


@router.get("/{workflow_id}", response_model=schemas.WorkflowOut)
def get_workflow(workflow_id: int, user: CurrentUser, db: DB):
    workflow = db.scalar(
        select(Workflow).where(Workflow.id == workflow_id, Workflow.user_id == user.id)
    )
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_out(workflow)


@router.patch("/{workflow_id}", response_model=schemas.WorkflowOut)
def update_workflow(workflow_id: int, body: schemas.WorkflowUpdate, user: CurrentUser, db: DB):
    workflow = db.scalar(
        select(Workflow).where(Workflow.id == workflow_id, Workflow.user_id == user.id)
    )
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(workflow, field, value)
    db.commit()
    db.refresh(workflow)
    return _workflow_out(workflow)


@router.delete("/{workflow_id}", status_code=204)
def delete_workflow(workflow_id: int, user: CurrentUser, db: DB):
    workflow = db.scalar(
        select(Workflow).where(Workflow.id == workflow_id, Workflow.user_id == user.id)
    )
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    db.delete(workflow)
    db.commit()
    return None


@router.post("/{workflow_id}/publish", response_model=schemas.WorkflowOut)
def publish_workflow(workflow_id: int, user: CurrentUser, db: DB):
    workflow = db.scalar(
        select(Workflow).where(Workflow.id == workflow_id, Workflow.user_id == user.id)
    )
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow.status = WORKFLOW_STATUS_ACTIVE
    db.commit()
    db.refresh(workflow)
    return _workflow_out(workflow)


@router.post("/{workflow_id}/archive", response_model=schemas.WorkflowOut)
def archive_workflow(workflow_id: int, user: CurrentUser, db: DB):
    workflow = db.scalar(
        select(Workflow).where(Workflow.id == workflow_id, Workflow.user_id == user.id)
    )
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow.status = "archived"
    db.commit()
    db.refresh(workflow)
    return _workflow_out(workflow)


@router.post("/executions", response_model=schemas.WorkflowExecutionOut, status_code=201)
def create_execution(body: schemas.WorkflowExecutionCreate, user: CurrentUser, db: DB):
    workflow = db.scalar(
        select(Workflow).where(Workflow.id == body.workflow_id, Workflow.user_id == user.id)
    )
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if workflow.status != WORKFLOW_STATUS_ACTIVE:
        raise HTTPException(status_code=400, detail="Workflow must be active to execute")
    execution = WorkflowExecution(
        workflow_id=body.workflow_id,
        trigger_payload_json=body.trigger_payload,
        context_json=body.context,
        status=EXECUTION_STATUS_PENDING,
        started_at=utcnow(),
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return schemas.WorkflowExecutionOut.model_validate(execution)


@router.get("/executions", response_model=list[schemas.WorkflowExecutionOut])
def list_executions(db: DB, user: CurrentUser, workflow_id: int | None = Query(default=None), status: str | None = Query(default=None)):
    query = select(WorkflowExecution).join(Workflow).where(Workflow.user_id == user.id)
    if workflow_id is not None:
        query = query.where(WorkflowExecution.workflow_id == workflow_id)
    if status is not None:
        query = query.where(WorkflowExecution.status == status)
    query = query.order_by(WorkflowExecution.started_at.desc())
    rows = db.scalars(query).all()
    return [schemas.WorkflowExecutionOut.model_validate(r) for r in rows]


@router.get("/executions/{execution_id}", response_model=schemas.WorkflowExecutionOut)
def get_execution(execution_id: int, user: CurrentUser, db: DB):
    execution = db.scalar(
        select(WorkflowExecution)
        .join(Workflow)
        .where(WorkflowExecution.id == execution_id, Workflow.user_id == user.id)
    )
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    return schemas.WorkflowExecutionOut.model_validate(execution)


@router.post("/executions/{execution_id}/steps", response_model=schemas.WorkflowStepExecutionOut, status_code=201)
def create_step_execution(execution_id: int, body: schemas.WorkflowStepExecutionCreate, user: CurrentUser, db: DB):
    execution = db.scalar(
        select(WorkflowExecution)
        .join(Workflow)
        .where(WorkflowExecution.id == execution_id, Workflow.user_id == user.id)
    )
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    step = WorkflowStepExecution(
        execution_id=execution_id,
        step_id=body.step_id.strip(),
        step_type=body.step_type.strip(),
        input_json=body.input,
        max_retries=body.max_retries,
        depends_on_json=body.depends_on,
        status=STEP_STATUS_PENDING,
        attempt_number=1,
    )
    db.add(step)
    db.commit()
    db.refresh(step)
    return schemas.WorkflowStepExecutionOut.model_validate(step)


@router.get("/executions/{execution_id}/steps", response_model=list[schemas.WorkflowStepExecutionOut])
def list_steps(execution_id: int, user: CurrentUser, db: DB):
    execution = db.scalar(
        select(WorkflowExecution)
        .join(Workflow)
        .where(WorkflowExecution.id == execution_id, Workflow.user_id == user.id)
    )
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    rows = db.scalars(
        select(WorkflowStepExecution)
        .where(WorkflowStepExecution.execution_id == execution_id)
        .order_by(WorkflowStepExecution.id.asc())
    ).all()
    return [schemas.WorkflowStepExecutionOut.model_validate(r) for r in rows]


@router.patch("/steps/{step_id}", response_model=schemas.WorkflowStepExecutionOut)
def update_step(step_id: int, body: schemas.WorkflowStepExecutionBase, user: CurrentUser, db: DB):
    step = db.scalar(
        select(WorkflowStepExecution)
        .join(WorkflowExecution)
        .join(Workflow)
        .where(WorkflowStepExecution.id == step_id, Workflow.user_id == user.id)
    )
    if step is None:
        raise HTTPException(status_code=404, detail="Step not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(step, field, value)
    db.commit()
    db.refresh(step)
    return schemas.WorkflowStepExecutionOut.model_validate(step)


@router.get("/stats/summary")
def workflow_stats(db: DB, user: CurrentUser):
    total_workflows = db.scalar(select(func.count(Workflow.id)).where(Workflow.user_id == user.id)) or 0
    active_workflows = db.scalar(
        select(func.count(Workflow.id)).where(Workflow.user_id == user.id, Workflow.status == WORKFLOW_STATUS_ACTIVE)
    ) or 0
    total_executions = db.scalar(
        select(func.count(WorkflowExecution.id)).join(Workflow).where(Workflow.user_id == user.id)
    ) or 0
    failed_executions = db.scalar(
        select(func.count(WorkflowExecution.id))
        .join(Workflow)
        .where(Workflow.user_id == user.id, WorkflowExecution.status == "failed")
    ) or 0
    return {
        "total_workflows": int(total_workflows),
        "active_workflows": int(active_workflows),
        "total_executions": int(total_executions),
        "failed_executions": int(failed_executions),
    }
