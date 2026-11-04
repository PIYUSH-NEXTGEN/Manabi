from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    ApiSpec,
    ApiContractComparison,
    ApiMonitoringTarget,
    ApiContractCheck,
    utcnow,
)

router = APIRouter(prefix="/api/api-contracts", tags=["api-contracts"])


def _spec_out(spec: ApiSpec) -> schemas.ApiSpecOut:
    return schemas.ApiSpecOut.model_validate(spec)


@router.get("/specs", response_model=list[schemas.ApiSpecOut])
def list_specs(db: DB, user: CurrentUser):
    rows = db.scalars(
        select(ApiSpec).where(ApiSpec.user_id == user.id).order_by(ApiSpec.created_at.desc())
    ).all()
    return [_spec_out(r) for r in rows]


@router.post("/specs", response_model=schemas.ApiSpecOut, status_code=201)
def create_spec(body: schemas.ApiSpecCreate, user: CurrentUser, db: DB):
    existing = db.scalar(
        select(ApiSpec).where(
            ApiSpec.user_id == user.id,
            ApiSpec.name == body.name.strip(),
            ApiSpec.version == body.version.strip(),
        )
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="A spec with this name and version already exists")
    spec = ApiSpec(
        user_id=user.id,
        name=body.name.strip(),
        version=body.version.strip(),
        spec_json=body.spec,
        source_type=body.source_type,
        source_url=body.source_url,
    )
    db.add(spec)
    db.commit()
    db.refresh(spec)
    return _spec_out(spec)


@router.get("/specs/{spec_id}", response_model=schemas.ApiSpecOut)
def get_spec(spec_id: int, user: CurrentUser, db: DB):
    spec = db.scalar(select(ApiSpec).where(ApiSpec.id == spec_id, ApiSpec.user_id == user.id))
    if spec is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return _spec_out(spec)


@router.patch("/specs/{spec_id}", response_model=schemas.ApiSpecOut)
def update_spec(spec_id: int, body: schemas.ApiSpecUpdate, user: CurrentUser, db: DB):
    spec = db.scalar(select(ApiSpec).where(ApiSpec.id == spec_id, ApiSpec.user_id == user.id))
    if spec is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(spec, field, value.strip() if isinstance(value, str) else value)
    spec.updated_at = utcnow()
    db.commit()
    db.refresh(spec)
    return _spec_out(spec)


@router.delete("/specs/{spec_id}", status_code=204)
def delete_spec(spec_id: int, user: CurrentUser, db: DB):
    spec = db.scalar(select(ApiSpec).where(ApiSpec.id == spec_id, ApiSpec.user_id == user.id))
    if spec is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    db.delete(spec)
    db.commit()
    return None


@router.post("/comparisons", response_model=schemas.ApiContractComparisonOut, status_code=201)
def create_comparison(body: schemas.ApiContractComparisonCreate, user: CurrentUser, db: DB):
    spec_a = db.scalar(select(ApiSpec).where(ApiSpec.id == body.spec_a_id, ApiSpec.user_id == user.id))
    if spec_a is None:
        raise HTTPException(status_code=404, detail="Spec A not found")
    spec_b = db.scalar(select(ApiSpec).where(ApiSpec.id == body.spec_b_id, ApiSpec.user_id == user.id))
    if spec_b is None:
        raise HTTPException(status_code=404, detail="Spec B not found")
    comparison = _compare_specs(spec_a.spec_json, spec_b.spec_json)
    breaking = comparison.get("breaking_changes", [])
    non_breaking = comparison.get("non_breaking_changes", [])
    affected = list({c.get("endpoint", "") for c in breaking if c.get("endpoint")})
    comp = ApiContractComparison(
        spec_a_id=body.spec_a_id,
        spec_b_id=body.spec_b_id,
        breaking_changes_count=len(breaking),
        non_breaking_changes_count=len(non_breaking),
        comparison_json=comparison,
        affected_endpoints_json=affected,
    )
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return schemas.ApiContractComparisonOut.model_validate(comp)


def _compare_specs(spec_a: dict, spec_b: dict) -> dict:
    """Detect breaking and non-breaking changes between two OpenAPI-like specs."""
    paths_a = spec_a.get("paths", {}) or {}
    paths_b = spec_b.get("paths", {}) or {}
    breaking = []
    non_breaking = []
    for path, ops_a in paths_a.items():
        ops_b = paths_b.get(path, {})
        for method, op_a in ops_a.items():
            if method not in ops_b:
                breaking.append(
                    {"endpoint": f"{method.upper()} {path}", "change": "endpoint_removed", "severity": "breaking"}
                )
                continue
            op_b = ops_b[method]
            params_a = {p.get("name"): p for p in op_a.get("parameters", []) or []}
            params_b = {p.get("name"): p for p in ops_b.get("parameters", []) or []}
            for pname, pdef in params_a.items():
                if pname not in params_b:
                    breaking.append(
                        {
                            "endpoint": f"{method.upper()} {path}",
                            "change": f"parameter_removed:{pname}",
                            "severity": "breaking",
                        }
                    )
            responses_a = op_a.get("responses", {}) or {}
            responses_b = op_b.get("responses", {}) or []
            if isinstance(responses_b, dict):
                for rcode in responses_a:
                    if rcode not in responses_b:
                        breaking.append(
                            {
                                "endpoint": f"{method.upper()} {path}",
                                "change": f"response_removed:{rcode}",
                                "severity": "breaking",
                            }
                        )
            request_body_a = op_a.get("requestBody")
            request_body_b = op_b.get("requestBody")
            if request_body_a and not request_body_b:
                breaking.append(
                    {"endpoint": f"{method.upper()} {path}", "change": "request_body_removed", "severity": "breaking"}
                )
            if not request_body_a and request_body_b:
                non_breaking.append(
                    {"endpoint": f"{method.upper()} {path}", "change": "request_body_added", "severity": "non_breaking"}
                )
    return {"breaking_changes": breaking, "non_breaking_changes": non_breaking}


@router.get("/comparisons", response_model=list[schemas.ApiContractComparisonOut])
def list_comparisons(db: DB, user: CurrentUser, limit: int = Query(default=50, ge=1, le=200)):
    rows = db.scalars(
        select(ApiContractComparison)
        .join(ApiSpec)
        .where(ApiSpec.user_id == user.id)
        .order_by(ApiContractComparison.created_at.desc())
        .limit(limit)
    ).all()
    return [schemas.ApiContractComparisonOut.model_validate(r) for r in rows]


@router.get("/comparisons/{comparison_id}", response_model=schemas.ApiContractComparisonOut)
def get_comparison(comparison_id: int, user: CurrentUser, db: DB):
    comp = db.scalar(
        select(ApiContractComparison)
        .join(ApiSpec)
        .where(ApiContractComparison.id == comparison_id, ApiSpec.user_id == user.id)
    )
    if comp is None:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return schemas.ApiContractComparisonOut.model_validate(comp)


@router.get("/monitoring-targets", response_model=list[schemas.ApiMonitoringTargetOut])
def list_monitoring_targets(db: DB, user: CurrentUser):
    rows = db.scalars(
        select(ApiMonitoringTarget).where(ApiMonitoringTarget.user_id == user.id).order_by(ApiMonitoringTarget.created_at.desc())
    ).all()
    return [schemas.ApiMonitoringTargetOut.model_validate(r) for r in rows]


@router.post("/monitoring-targets", response_model=schemas.ApiMonitoringTargetOut, status_code=201)
def create_monitoring_target(body: schemas.ApiMonitoringTargetCreate, user: CurrentUser, db: DB):
    target = ApiMonitoringTarget(
        user_id=user.id,
        name=body.name.strip(),
        base_url=str(body.base_url).strip(),
        spec_id=body.spec_id,
        check_interval_seconds=body.check_interval_seconds,
        is_active=body.is_active,
    )
    db.add(target)
    db.commit()
    db.refresh(target)
    return schemas.ApiMonitoringTargetOut.model_validate(target)


@router.patch("/monitoring-targets/{target_id}", response_model=schemas.ApiMonitoringTargetOut)
def update_monitoring_target(target_id: int, body: schemas.ApiMonitoringTargetUpdate, user: CurrentUser, db: DB):
    target = db.scalar(
        select(ApiMonitoringTarget).where(ApiMonitoringTarget.id == target_id, ApiMonitoringTarget.user_id == user.id)
    )
    if target is None:
        raise HTTPException(status_code=404, detail="Monitoring target not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(target, field, str(value).strip() if isinstance(value, str) else value)
    db.commit()
    db.refresh(target)
    return schemas.ApiMonitoringTargetOut.model_validate(target)


@router.delete("/monitoring-targets/{target_id}", status_code=204)
def delete_monitoring_target(target_id: int, user: CurrentUser, db: DB):
    target = db.scalar(
        select(ApiMonitoringTarget).where(ApiMonitoringTarget.id == target_id, ApiMonitoringTarget.user_id == user.id)
    )
    if target is None:
        raise HTTPException(status_code=404, detail="Monitoring target not found")
    db.delete(target)
    db.commit()
    return None


@router.post("/monitoring-targets/{target_id}/check", response_model=schemas.ApiContractCheckOut, status_code=201)
def run_contract_check(target_id: int, user: CurrentUser, db: DB):
    target = db.scalar(
        select(ApiMonitoringTarget).where(ApiMonitoringTarget.id == target_id, ApiMonitoringTarget.user_id == user.id)
    )
    if target is None:
        raise HTTPException(status_code=404, detail="Monitoring target not found")
    check = ApiContractCheck(
        target_id=target_id,
        status="pass",
        breaking_changes_detected=0,
        results_json={"checked_at": utcnow().isoformat(), "target": target.name},
    )
    target.last_checked_at = utcnow()
    db.add(check)
    db.commit()
    db.refresh(check)
    return schemas.ApiContractCheckOut.model_validate(check)


@router.get("/monitoring-targets/{target_id}/checks", response_model=list[schemas.ApiContractCheckOut])
def list_checks(target_id: int, db: DB, user: CurrentUser, limit: int = Query(default=50, ge=1, le=200)):
    target = db.scalar(
        select(ApiMonitoringTarget).where(ApiMonitoringTarget.id == target_id, ApiMonitoringTarget.user_id == user.id)
    )
    if target is None:
        raise HTTPException(status_code=404, detail="Monitoring target not found")
    rows = db.scalars(
        select(ApiContractCheck)
        .where(ApiContractCheck.target_id == target_id)
        .order_by(ApiContractCheck.checked_at.desc())
        .limit(limit)
    ).all()
    return [schemas.ApiContractCheckOut.model_validate(r) for r in rows]
