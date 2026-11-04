from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    Tenant,
    TenantMembership,
    TenantResource,
    SecurityFinding,
    RolePermission,
    ROLE_ADMIN,
    ROLE_MEMBER,
    ROLE_VIEWER,
    utcnow,
)

router = APIRouter(prefix="/api/tenant-security", tags=["tenant-security"])


def _tenant_out(t: Tenant) -> schemas.TenantOut:
    return schemas.TenantOut.model_validate(t)


@router.get("/tenants", response_model=list[schemas.TenantOut])
def list_tenants(db: DB, user: CurrentUser):
    rows = db.scalars(select(Tenant).order_by(Tenant.created_at.desc())).all()
    return [_tenant_out(r) for r in rows]


@router.post("/tenants", response_model=schemas.TenantOut, status_code=201)
def create_tenant(body: schemas.TenantCreate, user: CurrentUser, db: DB):
    existing = db.scalar(select(Tenant).where(Tenant.slug == body.slug.strip().lower()))
    if existing is not None:
        raise HTTPException(status_code=409, detail="A tenant with this slug already exists")
    tenant = Tenant(
        name=body.name.strip(),
        slug=body.slug.strip().lower(),
        plan=body.plan,
        settings_json=body.settings,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    membership = TenantMembership(user_id=user.id, tenant_id=tenant.id, role=ROLE_ADMIN)
    db.add(membership)
    db.commit()
    return _tenant_out(tenant)


@router.get("/tenants/{tenant_id}", response_model=schemas.TenantOut)
def get_tenant(tenant_id: int, user: CurrentUser, db: DB):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return _tenant_out(tenant)


@router.patch("/tenants/{tenant_id}", response_model=schemas.TenantOut)
def update_tenant(tenant_id: int, body: schemas.TenantUpdate, user: CurrentUser, db: DB):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(tenant, field, str(value).strip().lower() if field == "slug" and isinstance(value, str) else value)
    db.commit()
    db.refresh(tenant)
    return _tenant_out(tenant)


@router.delete("/tenants/{tenant_id}", status_code=204)
def delete_tenant(tenant_id: int, user: CurrentUser, db: DB):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    db.delete(tenant)
    db.commit()
    return None


@router.get("/tenants/{tenant_id}/memberships", response_model=list[schemas.TenantMembershipOut])
def list_memberships(tenant_id: int, db: DB, user: CurrentUser):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    rows = db.scalars(
        select(TenantMembership).where(TenantMembership.tenant_id == tenant_id).order_by(TenantMembership.joined_at.desc())
    ).all()
    return [schemas.TenantMembershipOut.model_validate(r) for r in rows]


@router.post("/tenants/{tenant_id}/memberships", response_model=schemas.TenantMembershipOut, status_code=201)
def create_membership(tenant_id: int, body: schemas.TenantMembershipCreate, user: CurrentUser, db: DB):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    existing = db.scalar(
        select(TenantMembership).where(
            TenantMembership.user_id == body.user_id, TenantMembership.tenant_id == tenant_id
        )
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="User is already a member of this tenant")
    membership = TenantMembership(user_id=body.user_id, tenant_id=tenant_id, role=body.role)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return schemas.TenantMembershipOut.model_validate(membership)


@router.patch("/tenants/{tenant_id}/memberships/{membership_id}", response_model=schemas.TenantMembershipOut)
def update_membership(tenant_id: int, membership_id: int, body: schemas.TenantMembershipBase, user: CurrentUser, db: DB):
    membership = db.scalar(
        select(TenantMembership).where(TenantMembership.id == membership_id, TenantMembership.tenant_id == tenant_id)
    )
    if membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    if body.role is not None:
        membership.role = body.role
    db.commit()
    db.refresh(membership)
    return schemas.TenantMembershipOut.model_validate(membership)


@router.delete("/tenants/{tenant_id}/memberships/{membership_id}", status_code=204)
def delete_membership(tenant_id: int, membership_id: int, user: CurrentUser, db: DB):
    membership = db.scalar(
        select(TenantMembership).where(TenantMembership.id == membership_id, TenantMembership.tenant_id == tenant_id)
    )
    if membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    db.delete(membership)
    db.commit()
    return None


@router.get("/tenants/{tenant_id}/resources", response_model=list[schemas.TenantResourceOut])
def list_resources(tenant_id: int, db: DB, user: CurrentUser):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    rows = db.scalars(
        select(TenantResource).where(TenantResource.tenant_id == tenant_id).order_by(TenantResource.created_at.desc())
    ).all()
    return [schemas.TenantResourceOut.model_validate(r) for r in rows]


@router.post("/tenants/{tenant_id}/resources", response_model=schemas.TenantResourceOut, status_code=201)
def create_resource(tenant_id: int, body: schemas.TenantResourceCreate, user: CurrentUser, db: DB):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    resource = TenantResource(
        tenant_id=tenant_id,
        resource_type=body.resource_type.strip(),
        resource_id=body.resource_id.strip(),
        owner_user_id=body.owner_user_id,
        metadata_json=body.metadata,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return schemas.TenantResourceOut.model_validate(resource)


@router.get("/tenants/{tenant_id}/findings", response_model=list[schemas.SecurityFindingOut])
def list_findings(tenant_id: int, db: DB, user: CurrentUser, severity: str | None = Query(default=None), status: str | None = Query(default=None)):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    query = select(SecurityFinding).where(SecurityFinding.tenant_id == tenant_id)
    if severity:
        query = query.where(SecurityFinding.severity == severity)
    if status:
        query = query.where(SecurityFinding.status == status)
    query = query.order_by(SecurityFinding.detected_at.desc())
    rows = db.scalars(query).all()
    return [schemas.SecurityFindingOut.model_validate(r) for r in rows]


@router.post("/tenants/{tenant_id}/findings", response_model=schemas.SecurityFindingOut, status_code=201)
def create_finding(tenant_id: int, body: schemas.SecurityFindingCreate, user: CurrentUser, db: DB):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    finding = SecurityFinding(
        tenant_id=tenant_id,
        check_type=body.check_type.strip(),
        severity=body.severity,
        title=body.title.strip(),
        description=body.description.strip(),
        affected_resource=body.affected_resource,
        remediation=body.remediation,
        status=body.status,
        detected_at=utcnow(),
    )
    db.add(finding)
    db.commit()
    db.refresh(finding)
    return schemas.SecurityFindingOut.model_validate(finding)


@router.patch("/findings/{finding_id}", response_model=schemas.SecurityFindingOut)
def update_finding(finding_id: int, body: schemas.SecurityFindingUpdate, user: CurrentUser, db: DB):
    finding = db.scalar(select(SecurityFinding).where(SecurityFinding.id == finding_id))
    if finding is None:
        raise HTTPException(status_code=404, detail="Finding not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(finding, field, value)
    if body.status == "resolved" and finding.resolved_at is None:
        finding.resolved_at = utcnow()
    db.commit()
    db.refresh(finding)
    return schemas.SecurityFindingOut.model_validate(finding)


@router.get("/roles/permissions", response_model=list[schemas.RolePermissionOut])
def list_role_permissions(db: DB):
    rows = db.scalars(select(RolePermission).order_by(RolePermission.role, RolePermission.permission)).all()
    return [schemas.RolePermissionOut.model_validate(r) for r in rows]


@router.post("/roles/permissions", response_model=schemas.RolePermissionOut, status_code=201)
def create_role_permission(body: schemas.RolePermissionCreate, user: CurrentUser, db: DB):
    existing = db.scalar(
        select(RolePermission).where(RolePermission.role == body.role, RolePermission.permission == body.permission)
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="Role permission already exists")
    perm = RolePermission(role=body.role.strip(), permission=body.permission.strip(), resource_type=body.resource_type)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return schemas.RolePermissionOut.model_validate(perm)


@router.delete("/roles/permissions/{perm_id}", status_code=204)
def delete_role_permission(perm_id: int, user: CurrentUser, db: DB):
    perm = db.scalar(select(RolePermission).where(RolePermission.id == perm_id))
    if perm is None:
        raise HTTPException(status_code=404, detail="Role permission not found")
    db.delete(perm)
    db.commit()
    return None


@router.get("/audit/summary")
def audit_summary(db: DB):
    total_tenants = db.scalar(select(func.count(Tenant.id))) or 0
    open_findings = db.scalar(select(func.count(SecurityFinding.id)).where(SecurityFinding.status == "open")) or 0
    critical_findings = db.scalar(
        select(func.count(SecurityFinding.id)).where(SecurityFinding.severity == "critical", SecurityFinding.status == "open")
    ) or 0
    high_findings = db.scalar(
        select(func.count(SecurityFinding.id)).where(SecurityFinding.severity == "high", SecurityFinding.status == "open")
    ) or 0
    return {
        "total_tenants": int(total_tenants),
        "open_findings": int(open_findings),
        "critical_findings": int(critical_findings),
        "high_findings": int(high_findings),
    }
