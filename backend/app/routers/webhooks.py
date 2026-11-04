from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func, update
from sqlalchemy.orm import joinedload, selectinload

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    WebhookEndpoint,
    WebhookEvent,
    WebhookDelivery,
    WEBHOOK_STATUS_ACTIVE,
    WEBHOOK_STATUS_DISABLED,
    utcnow,
)

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


def _endpoint_out(endpoint: WebhookEndpoint) -> schemas.WebhookEndpointOut:
    return schemas.WebhookEndpointOut.model_validate(endpoint)


@router.get("/endpoints", response_model=list[schemas.WebhookEndpointOut])
def list_endpoints(db: DB, user: CurrentUser):
    rows = db.scalars(
        select(WebhookEndpoint).where(WebhookEndpoint.user_id == user.id).order_by(WebhookEndpoint.created_at.desc())
    ).all()
    return [_endpoint_out(r) for r in rows]


@router.post("/endpoints", response_model=schemas.WebhookEndpointOut, status_code=201)
def create_endpoint(body: schemas.WebhookEndpointCreate, user: CurrentUser, db: DB):
    endpoint = WebhookEndpoint(
        user_id=user.id,
        name=body.name.strip(),
        url=str(body.url).strip(),
        secret=body.secret,
        status=WEBHOOK_STATUS_ACTIVE,
        retry_max_attempts=body.retry_max_attempts,
        retry_initial_delay_ms=body.retry_initial_delay_ms,
        retry_max_delay_ms=body.retry_max_delay_ms,
        timeout_ms=body.timeout_ms,
        event_types_json=body.event_types,
    )
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)
    return _endpoint_out(endpoint)


@router.get("/endpoints/{endpoint_id}", response_model=schemas.WebhookEndpointOut)
def get_endpoint(endpoint_id: int, user: CurrentUser, db: DB):
    endpoint = db.scalar(
        select(WebhookEndpoint).where(WebhookEndpoint.id == endpoint_id, WebhookEndpoint.user_id == user.id)
    )
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return _endpoint_out(endpoint)


@router.patch("/endpoints/{endpoint_id}", response_model=schemas.WebhookEndpointOut)
def update_endpoint(endpoint_id: int, body: schemas.WebhookEndpointUpdate, user: CurrentUser, db: DB):
    endpoint = db.scalar(
        select(WebhookEndpoint).where(WebhookEndpoint.id == endpoint_id, WebhookEndpoint.user_id == user.id)
    )
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if field == "url" and value is not None:
            setattr(endpoint, field, str(value).strip())
        elif value is not None:
            setattr(endpoint, field, value)
    db.commit()
    db.refresh(endpoint)
    return _endpoint_out(endpoint)


@router.delete("/endpoints/{endpoint_id}", status_code=204)
def delete_endpoint(endpoint_id: int, user: CurrentUser, db: DB):
    endpoint = db.scalar(
        select(WebhookEndpoint).where(WebhookEndpoint.id == endpoint_id, WebhookEndpoint.user_id == user.id)
    )
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    db.delete(endpoint)
    db.commit()
    return None


@router.post("/endpoints/{endpoint_id}/events", response_model=schemas.WebhookEventOut, status_code=201)
def ingest_event(endpoint_id: int, body: schemas.WebhookEventCreate, user: CurrentUser, db: DB):
    endpoint = db.scalar(
        select(WebhookEndpoint).where(WebhookEndpoint.id == endpoint_id, WebhookEndpoint.user_id == user.id)
    )
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    event = WebhookEvent(
        endpoint_id=endpoint_id,
        event_id=body.event_id,
        event_type=body.event_type,
        payload_json=body.payload,
        headers_json=body.headers,
        received_at=utcnow(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return schemas.WebhookEventOut.model_validate(event)


@router.get("/endpoints/{endpoint_id}/events", response_model=list[schemas.WebhookEventOut])
def list_events(endpoint_id: int, user: CurrentUser, db: DB, limit: int = Query(default=50, ge=1, le=200)):
    endpoint = db.scalar(
        select(WebhookEndpoint).where(WebhookEndpoint.id == endpoint_id, WebhookEndpoint.user_id == user.id)
    )
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    rows = db.scalars(
        select(WebhookEvent)
        .where(WebhookEvent.endpoint_id == endpoint_id)
        .order_by(WebhookEvent.received_at.desc())
        .limit(limit)
    ).all()
    return [schemas.WebhookEventOut.model_validate(r) for r in rows]


@router.post("/deliveries", response_model=schemas.WebhookDeliveryOut, status_code=201)
def create_delivery(body: schemas.WebhookDeliveryCreate, user: CurrentUser, db: DB):
    endpoint = db.scalar(
        select(WebhookEndpoint).where(WebhookEndpoint.id == body.endpoint_id, WebhookEndpoint.user_id == user.id)
    )
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    delivery = WebhookDelivery(
        endpoint_id=body.endpoint_id,
        event_id=body.event_id,
        status=body.status,
        scheduled_at=body.scheduled_at or utcnow(),
    )
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return schemas.WebhookDeliveryOut.model_validate(delivery)


@router.get("/deliveries", response_model=list[schemas.WebhookDeliveryOut])
def list_deliveries(
    db: DB,
    user: CurrentUser,
    endpoint_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    query = select(WebhookDelivery).join(WebhookEndpoint).where(WebhookEndpoint.user_id == user.id)
    if endpoint_id is not None:
        query = query.where(WebhookDelivery.endpoint_id == endpoint_id)
    if status is not None:
        query = query.where(WebhookDelivery.status == status)
    query = query.order_by(WebhookDelivery.created_at.desc()).limit(limit)
    rows = db.scalars(query).all()
    return [schemas.WebhookDeliveryOut.model_validate(r) for r in rows]


@router.get("/deliveries/{delivery_id}", response_model=schemas.WebhookDeliveryOut)
def get_delivery(delivery_id: int, user: CurrentUser, db: DB):
    delivery = db.scalar(
        select(WebhookDelivery)
        .join(WebhookEndpoint)
        .where(WebhookDelivery.id == delivery_id, WebhookEndpoint.user_id == user.id)
    )
    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return schemas.WebhookDeliveryOut.model_validate(delivery)


@router.patch("/deliveries/{delivery_id}", response_model=schemas.WebhookDeliveryOut)
def update_delivery(delivery_id: int, body: schemas.WebhookDeliveryBase, user: CurrentUser, db: DB):
    delivery = db.scalar(
        select(WebhookDelivery)
        .join(WebhookEndpoint)
        .where(WebhookDelivery.id == delivery_id, WebhookEndpoint.user_id == user.id)
    )
    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(delivery, field, value)
    if body.status in ("delivered", "failed", "dead_letter") and delivery.attempted_at is None:
        delivery.attempted_at = utcnow()
    db.commit()
    db.refresh(delivery)
    return schemas.WebhookDeliveryOut.model_validate(delivery)


@router.post("/deliveries/{delivery_id}/retry", response_model=schemas.WebhookDeliveryOut)
def retry_delivery(delivery_id: int, user: CurrentUser, db: DB):
    delivery = db.scalar(
        select(WebhookDelivery)
        .options(joinedload(WebhookDelivery.endpoint))
        .join(WebhookEndpoint)
        .where(WebhookDelivery.id == delivery_id, WebhookEndpoint.user_id == user.id)
    )
    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    if delivery.status not in ("failed", "dead_letter"):
        raise HTTPException(status_code=400, detail="Only failed or dead_letter deliveries can be retried")
    endpoint = delivery.endpoint
    delivery.status = "queued"
    delivery.attempt_number = (delivery.attempt_number or 1) + 1
    delivery.next_retry_at = utcnow() + timedelta(milliseconds=endpoint.retry_initial_delay_ms)
    delivery.error_message = None
    db.commit()
    db.refresh(delivery)
    return schemas.WebhookDeliveryOut.model_validate(delivery)


@router.get("/stats/summary")
def delivery_stats(db: DB, user: CurrentUser):
    total_endpoints = db.scalar(
        select(func.count(WebhookEndpoint.id)).where(WebhookEndpoint.user_id == user.id)
    ) or 0
    active_endpoints = db.scalar(
        select(func.count(WebhookEndpoint.id)).where(
            WebhookEndpoint.user_id == user.id, WebhookEndpoint.status == WEBHOOK_STATUS_ACTIVE
        )
    ) or 0
    total_deliveries = db.scalar(
        select(func.count(WebhookDelivery.id)).join(WebhookEndpoint).where(WebhookEndpoint.user_id == user.id)
    ) or 0
    failed_deliveries = db.scalar(
        select(func.count(WebhookDelivery.id))
        .join(WebhookEndpoint)
        .where(WebhookEndpoint.user_id == user.id, WebhookDelivery.status == "failed")
    ) or 0
    dead_letter = db.scalar(
        select(func.count(WebhookDelivery.id))
        .join(WebhookEndpoint)
        .where(WebhookEndpoint.user_id == user.id, WebhookDelivery.status == "dead_letter")
    ) or 0
    return {
        "total_endpoints": int(total_endpoints),
        "active_endpoints": int(active_endpoints),
        "total_deliveries": int(total_deliveries),
        "failed_deliveries": int(failed_deliveries),
        "dead_letter_deliveries": int(dead_letter),
        "success_rate": round((total_deliveries - failed_deliveries - dead_letter) / max(total_deliveries, 1) * 100, 2),
    }
