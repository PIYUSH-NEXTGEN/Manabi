from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app import schemas
from app.deps import DB, CurrentUser
from app.models import (
    SalesChannel,
    InventoryItem,
    InventoryReservation,
    StockReconciliation,
    RESERVATION_STATUS_ACTIVE,
    RESERVATION_STATUS_CONSUMED,
    RESERVATION_STATUS_RELEASED,
    RESERVATION_STATUS_EXPIRED,
    utcnow,
)

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


def _channel_out(c: SalesChannel) -> schemas.SalesChannelOut:
    return schemas.SalesChannelOut.model_validate(c)


@router.get("/channels", response_model=list[schemas.SalesChannelOut])
def list_channels(db: DB, user: CurrentUser):
    rows = db.scalars(select(SalesChannel).order_by(SalesChannel.created_at.desc())).all()
    return [_channel_out(r) for r in rows]


@router.post("/channels", response_model=schemas.SalesChannelOut, status_code=201)
def create_channel(body: schemas.SalesChannelCreate, user: CurrentUser, db: DB):
    channel = SalesChannel(
        name=body.name.strip(),
        channel_type=body.channel_type.strip(),
        config_json=body.config,
        is_active=body.is_active,
    )
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return _channel_out(channel)


@router.get("/channels/{channel_id}", response_model=schemas.SalesChannelOut)
def get_channel(channel_id: int, user: CurrentUser, db: DB):
    channel = db.scalar(select(SalesChannel).where(SalesChannel.id == channel_id))
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return _channel_out(channel)


@router.patch("/channels/{channel_id}", response_model=schemas.SalesChannelOut)
def update_channel(channel_id: int, body: schemas.SalesChannelUpdate, user: CurrentUser, db: DB):
    channel = db.scalar(select(SalesChannel).where(SalesChannel.id == channel_id))
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(channel, field, str(value).strip() if isinstance(value, str) else value)
    db.commit()
    db.refresh(channel)
    return _channel_out(channel)


@router.delete("/channels/{channel_id}", status_code=204)
def delete_channel(channel_id: int, user: CurrentUser, db: DB):
    channel = db.scalar(select(SalesChannel).where(SalesChannel.id == channel_id))
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    db.delete(channel)
    db.commit()
    return None


@router.get("/channels/{channel_id}/items", response_model=list[schemas.InventoryItemOut])
def list_items(channel_id: int, db: DB, user: CurrentUser, sku: str | None = Query(default=None), low_stock: bool | None = Query(default=None)):
    channel = db.scalar(select(SalesChannel).where(SalesChannel.id == channel_id))
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    query = select(InventoryItem).where(InventoryItem.channel_id == channel_id)
    if sku:
        query = query.where(InventoryItem.sku == sku)
    if low_stock:
        query = query.where(InventoryItem.available_quantity <= InventoryItem.reorder_threshold)
    query = query.order_by(InventoryItem.sku.asc())
    rows = db.scalars(query).all()
    return [schemas.InventoryItemOut.model_validate(r) for r in rows]


@router.post("/channels/{channel_id}/items", response_model=schemas.InventoryItemOut, status_code=201)
def create_item(channel_id: int, body: schemas.InventoryItemCreate, user: CurrentUser, db: DB):
    channel = db.scalar(select(SalesChannel).where(SalesChannel.id == channel_id))
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    existing = db.scalar(
        select(InventoryItem).where(InventoryItem.channel_id == channel_id, InventoryItem.sku == body.sku.strip())
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="Item with this SKU already exists in channel")
    item = InventoryItem(
        channel_id=channel_id,
        sku=body.sku.strip(),
        name=body.name.strip(),
        total_quantity=body.total_quantity,
        reserved_quantity=body.reserved_quantity,
        available_quantity=body.available_quantity,
        reorder_threshold=body.reorder_threshold,
        metadata_json=body.metadata,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return schemas.InventoryItemOut.model_validate(item)


@router.get("/items/{item_id}", response_model=schemas.InventoryItemOut)
def get_item(item_id: int, db: DB, user: CurrentUser):
    item = db.scalar(
        select(InventoryItem).join(SalesChannel).where(InventoryItem.id == item_id)
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return schemas.InventoryItemOut.model_validate(item)


@router.patch("/items/{item_id}", response_model=schemas.InventoryItemOut)
def update_item(item_id: int, body: schemas.InventoryItemUpdate, user: CurrentUser, db: DB):
    item = db.scalar(
        select(InventoryItem).join(SalesChannel).where(InventoryItem.id == item_id)
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return schemas.InventoryItemOut.model_validate(item)


@router.post("/reservations", response_model=schemas.InventoryReservationOut, status_code=201)
def create_reservation(body: schemas.InventoryReservationCreate, user: CurrentUser, db: DB):
    item = db.scalar(select(InventoryItem).where(InventoryItem.id == body.item_id))
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.available_quantity < body.quantity:
        raise HTTPException(status_code=409, detail="Insufficient inventory available")
    channel = db.scalar(select(SalesChannel).where(SalesChannel.id == body.channel_id))
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    reservation = InventoryReservation(
        item_id=body.item_id,
        channel_id=body.channel_id,
        external_order_id=body.external_order_id,
        quantity=body.quantity,
        status=RESERVATION_STATUS_ACTIVE,
        reserved_at=utcnow(),
        expires_at=body.expires_at,
    )
    item.available_quantity = (item.available_quantity or 0) - body.quantity
    item.reserved_quantity = (item.reserved_quantity or 0) + body.quantity
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return schemas.InventoryReservationOut.model_validate(reservation)


@router.get("/reservations", response_model=list[schemas.InventoryReservationOut])
def list_reservations(db: DB, user: CurrentUser, item_id: int | None = Query(default=None), status: str | None = Query(default=None)):
    query = select(InventoryReservation).join(InventoryItem).join(SalesChannel)
    if item_id is not None:
        query = query.where(InventoryReservation.item_id == item_id)
    if status is not None:
        query = query.where(InventoryReservation.status == status)
    query = query.order_by(InventoryReservation.reserved_at.desc())
    rows = db.scalars(query).all()
    return [schemas.InventoryReservationOut.model_validate(r) for r in rows]


@router.patch("/reservations/{reservation_id}", response_model=schemas.InventoryReservationOut)
def update_reservation(reservation_id: int, body: schemas.InventoryReservationUpdate, user: CurrentUser, db: DB):
    reservation = db.scalar(
        select(InventoryReservation).join(InventoryItem).join(SalesChannel).where(InventoryReservation.id == reservation_id)
    )
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    item = reservation.item
    old_status = reservation.status
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(reservation, field, value)
    new_status = reservation.status
    if old_status == RESERVATION_STATUS_ACTIVE and new_status == RESERVATION_STATUS_CONSUMED:
        reservation.consumed_at = utcnow()
        item.reserved_quantity = max(0, (item.reserved_quantity or 0) - reservation.quantity)
    elif old_status == RESERVATION_STATUS_ACTIVE and new_status == RESERVATION_STATUS_RELEASED:
        reservation.released_at = utcnow()
        item.available_quantity = (item.available_quantity or 0) + reservation.quantity
        item.reserved_quantity = max(0, (item.reserved_quantity or 0) - reservation.quantity)
    elif old_status == RESERVATION_STATUS_ACTIVE and new_status == RESERVATION_STATUS_EXPIRED:
        item.available_quantity = (item.available_quantity or 0) + reservation.quantity
        item.reserved_quantity = max(0, (item.reserved_quantity or 0) - reservation.quantity)
    db.commit()
    db.refresh(reservation)
    return schemas.InventoryReservationOut.model_validate(reservation)


@router.post("/reconciliations", response_model=schemas.StockReconciliationOut, status_code=201)
def create_reconciliation(body: schemas.StockReconciliationCreate, user: CurrentUser, db: DB):
    item = db.scalar(select(InventoryItem).where(InventoryItem.id == body.item_id))
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    discrepancy = body.actual_quantity - body.expected_quantity
    rec = StockReconciliation(
        item_id=body.item_id,
        expected_quantity=body.expected_quantity,
        actual_quantity=body.actual_quantity,
        discrepancy=discrepancy,
        reason=body.reason,
        reconciled_by_user_id=body.reconciled_by_user_id or user.id,
        reconciled_at=utcnow(),
    )
    item.total_quantity = body.actual_quantity
    item.available_quantity = max(0, body.actual_quantity - (item.reserved_quantity or 0))
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return schemas.StockReconciliationOut.model_validate(rec)


@router.get("/reconciliations", response_model=list[schemas.StockReconciliationOut])
def list_reconciliations(db: DB, user: CurrentUser, item_id: int | None = Query(default=None)):
    query = select(StockReconciliation).join(InventoryItem)
    if item_id is not None:
        query = query.where(StockReconciliation.item_id == item_id)
    query = query.order_by(StockReconciliation.reconciled_at.desc())
    rows = db.scalars(query).all()
    return [schemas.StockReconciliationOut.model_validate(r) for r in rows]


@router.get("/stats/summary")
def inventory_stats(db: DB):
    total_items = db.scalar(select(func.count(InventoryItem.id))) or 0
    total_channels = db.scalar(select(func.count(SalesChannel.id))) or 0
    active_reservations = db.scalar(
        select(func.count(InventoryReservation.id)).where(InventoryReservation.status == RESERVATION_STATUS_ACTIVE)
    ) or 0
    low_stock = db.scalar(
        select(func.count(InventoryItem.id)).where(InventoryItem.available_quantity <= InventoryItem.reorder_threshold)
    ) or 0
    return {
        "total_items": int(total_items),
        "total_channels": int(total_channels),
        "active_reservations": int(active_reservations),
        "low_stock_items": int(low_stock),
    }
