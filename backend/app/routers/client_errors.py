"""Browser failure intake.

The frontend cannot count on a developer watching the browser console after a
deploy. This endpoint accepts a small, bounded error report from the same
origin, records it through the normal logger (with the request id and the
backend request id from the failing call), and rate-limits per IP so it cannot
be used to flood logs. It stores nothing and accepts no request bodies beyond
the report fields.
"""

import logging

from fastapi import APIRouter, Request, Response

from app import schemas
from app.deps import DB
from app.services.ratelimit import RateLimiter

router = APIRouter(tags=["observability"])
logger = logging.getLogger(__name__)

CLIENT_ERROR_LIMITER = RateLimiter("CLIENT_ERROR_RATE_LIMIT_PER_HOUR")


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@router.post("/api/client-errors", status_code=204, include_in_schema=True)
def report_client_error(
    body: schemas.ClientErrorIn, request: Request, db: DB
) -> Response:
    retry = CLIENT_ERROR_LIMITER.check(db, f"client-error-ip:{_client_ip(request)}")
    if retry is not None:
        logger.warning(
            "Client error report rate limited",
            extra={"event": "client_error_rate_limited", "retry_after": retry},
        )
        return Response(status_code=429, headers={"Retry-After": str(retry)})

    logger.error(
        "Client error reported route=%s event=%s",
        body.route or "-",
        body.event,
        extra={
            "event": "client_error",
            "client_event": body.event,
            "client_route": body.route,
            "client_message": (body.message or "")[:300] or None,
            "client_stack": (body.stack or "")[:2000] or None,
            "component_stack": (body.component_stack or "")[:1000] or None,
            "error_type": body.error_name or "Error",
            "client_app_version": body.app_version,
            "backend_request_id": body.backend_request_id,
        },
    )
    return Response(status_code=204)
