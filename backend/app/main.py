import logging
import time
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, TimeoutError as SATimeoutError

from app.config import get_settings
from app.db import get_engine
from app.logging_config import configure_logging, request_id_var

logger = logging.getLogger(__name__)

INTERNAL_ERROR_MESSAGE = "Something went wrong on our side. Try again."
DATABASE_UNAVAILABLE_MESSAGE = "The service is temporarily unavailable. Try again shortly."


DEFAULT_SESSION_SECRET = "change-me-long-random-string"


def _is_local_base_url(base_url: str) -> bool:
    host = (urlsplit(base_url).hostname or "").lower()
    return host in {"localhost", "127.0.0.1", "::1"}


def guard_deploy_secrets(settings) -> None:
    """Fail fast on unsafe deploy settings (local dev keeps its defaults)."""
    app_env = getattr(settings, "APP_ENV", "development")
    base_url = (settings.BASE_URL or "").strip().rstrip("/")
    is_local = _is_local_base_url(base_url)

    if app_env == "production":
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" or not parsed.netloc or is_local:
            raise RuntimeError(
                "APP_ENV=production requires BASE_URL to be a public https:// origin. "
                "Set BASE_URL to the deployed domain before starting the service."
            )
        database_url = str(getattr(settings, "DATABASE_URL", "")).strip().lower()
        if database_url.startswith("sqlite"):
            raise RuntimeError(
                "APP_ENV=production requires a durable non-SQLite DATABASE_URL. "
                "Set the managed Postgres connection string before starting the service."
            )
        frontend_url = (getattr(settings, "FRONTEND_URL", "") or "").strip().rstrip("/")
        if frontend_url:
            parsed_frontend = urlsplit(frontend_url)
            if parsed_frontend.scheme != "https" or not parsed_frontend.netloc:
                raise RuntimeError(
                    "APP_ENV=production requires FRONTEND_URL to be a public https:// "
                    "origin when it is set. Leave it empty for a single-service deploy."
                )

    if is_local:
        return

    secret = (settings.SESSION_SECRET or "").strip()
    # An empty or short key still signs cookies, and a predictable key lets
    # anyone mint a session cookie for any account. Enforce real entropy on
    # deploy; the local placeholder stays convenient for development.
    if len(secret) < 32 or secret == DEFAULT_SESSION_SECRET:
        raise RuntimeError(
            "SESSION_SECRET must be at least 32 characters of random data and not the "
            "placeholder value. Generate one with "
            "python -c \"import secrets; print(secrets.token_urlsafe(32))\" before deploying."
        )


def _database_kind() -> str:
    """Deployment-safe database label: never include credentials or the URL."""
    url = str(get_settings().DATABASE_URL).strip().lower()
    if url.startswith("sqlite"):
        return "sqlite"
    if url.startswith(("postgres://", "postgresql://", "postgresql+")):
        return "postgres"
    return "other"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from app import models  # noqa: F401  (ensures tables are registered)
    from app.db import Base, normalized_database_url

    try:
        database_url = normalized_database_url(get_settings().DATABASE_URL)
        if database_url.startswith("sqlite"):
            # Local dev / tests keep the create-all convenience. Production
            # (Postgres) must never silently diverge from migrations (§6.1).
            Base.metadata.create_all(get_engine())
        else:
            from app.migrations import upgrade_to_head

            upgrade_to_head()
    except Exception:
        logger.exception(
            "Service startup failed",
            extra={"event": "service_startup_failed", "database": _database_kind()},
        )
        raise

    logger.info(
        "Service started env=%s database=%s",
        get_settings().APP_ENV,
        _database_kind(),
        extra={"event": "service_startup", "database": _database_kind()},
    )
    try:
        yield
    finally:
        try:
            # Release pooled HTTP connections and DB sockets after uvicorn stops
            # accepting requests, so a redeploy never abandons them.
            from app.services import github

            await github.close_client()
            get_engine().dispose()
        finally:
            logger.info("Service stopped", extra={"event": "service_shutdown"})


def _request_id(request: Request) -> str:
    """Trust a bounded caller-supplied id, otherwise mint one for correlation."""
    raw = request.headers.get("X-Request-ID") if hasattr(request, "headers") else None
    if isinstance(raw, str):
        candidate = raw.strip()
        if (
            candidate
            and len(candidate) <= 64
            and all(char.isalnum() or char in "-_." for char in candidate)
        ):
            return candidate
    return uuid.uuid4().hex


def _request_id_from_state(request: Request) -> str:
    """Prefer the id the middleware already attached, so logs and responses match."""
    state = getattr(request, "state", None)
    existing = getattr(state, "request_id", None)
    if isinstance(existing, str) and existing:
        return existing
    return _request_id(request)


def _safe_path(request: Request) -> str:
    url = getattr(request, "url", None)
    path = getattr(url, "path", None)
    return path if isinstance(path, str) and path else "?"


def _route_template(request: Request) -> str:
    """Route template, never the raw URL: ids and query strings stay out of logs."""
    scope = getattr(request, "scope", None) or {}
    route = scope.get("route") if isinstance(scope, dict) else None
    template = getattr(route, "path", None)
    if isinstance(template, str) and template.startswith("/api"):
        return template
    return "<unmatched>"


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """One safe JSON 500 for unexpected API failures; details stay in logs."""
    request_id = _request_id_from_state(request)
    logger.error(
        "Unhandled error method=%s path=%s",
        getattr(request, "method", "?"),
        _safe_path(request),
        extra={
            "event": "unhandled_exception",
            "method": getattr(request, "method", "?"),
            "path": _safe_path(request),
            "error_type": type(exc).__name__,
        },
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": {"code": "internal_error", "message": INTERNAL_ERROR_MESSAGE}
        },
        headers={"X-Request-ID": request_id},
    )


async def database_unavailable_handler(
    request: Request, exc: OperationalError | SATimeoutError
) -> JSONResponse:
    """A dependency outage is not an application bug: report 503, not 500."""
    request_id = _request_id_from_state(request)
    logger.error(
        "Database unavailable method=%s path=%s",
        getattr(request, "method", "?"),
        _safe_path(request),
        extra={
            "event": "database_unavailable",
            "method": getattr(request, "method", "?"),
            "path": _safe_path(request),
            "database": _database_kind(),
            "error_type": type(exc).__name__,
        },
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=503,
        content={
            "detail": {
                "code": "database_unavailable",
                "message": DATABASE_UNAVAILABLE_MESSAGE,
            }
        },
        headers={"X-Request-ID": request_id},
    )


def _apply_security_headers(
    response, path: str, request_id: str, settings
) -> None:
    response.headers.setdefault("X-Request-ID", request_id)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    # This app never needs to be framed by another origin; deny it to
    # stop clickjacking of the session-backed buttons.
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Content-Security-Policy", "frame-ancestors 'none'")
    if settings.BASE_URL.startswith("https://"):
        # Render terminates TLS at its edge; HSTS still belongs on the
        # response so browsers refuse a later plain-HTTP downgrade.
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000")
    if path.startswith("/api/"):
        # Authenticated JSON (me, dashboard, admin) must not sit in browser
        # or intermediary caches where a shared machine could replay it.
        response.headers.setdefault("Cache-Control", "no-store")


def _log_access(request: Request, status: int, duration_ms: float) -> None:
    """One access line per API request, plus a slow-request warning.

    Health probes are logged only when they fail or are slow; Render polls them
    continuously and their success lines would bury real incidents.
    """
    try:
        path = _safe_path(request)
        if not path.startswith("/api/"):
            return
        route = _route_template(request)
        slow_ms = max(1, int(getattr(get_settings(), "SLOW_REQUEST_MS", 2000)))
        extra = {
            "event": "request_completed",
            "method": getattr(request, "method", "?"),
            "path": route,
            "status": int(status),
            "duration_ms": round(float(duration_ms), 1),
        }
        if path.startswith("/api/health") and status < 500 and duration_ms < slow_ms:
            return
        if status >= 500:
            logger.error(
                "Request failed status=%s path=%s", status, route, extra={**extra, "event": "request_failed"}
            )
        else:
            logger.info("Request completed status=%s path=%s", status, route, extra=extra)
        if duration_ms >= slow_ms:
            logger.warning(
                "Slow request duration_ms=%s path=%s",
                extra["duration_ms"],
                route,
                extra={**extra, "event": "slow_request"},
            )
    except Exception:  # noqa: BLE001 - diagnostics must never break a request
        return


def create_app() -> FastAPI:
    try:
        settings = get_settings()
    except Exception:
        # Settings validation runs before the normal handler exists. Keep the
        # failure visible in platform logs even if the formatter is not ready.
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger(__name__).exception(
            "Configuration failed to load", extra={"event": "config_load_failed"}
        )
        raise
    configure_logging(settings)
    try:
        guard_deploy_secrets(settings)
    except RuntimeError:
        logger.critical(
            "Deployment configuration rejected",
            extra={"event": "config_invalid", "environment": settings.APP_ENV},
        )
        raise
    app = FastAPI(title="MANABI API", lifespan=lifespan)
    # Specific dependency/timeout handlers win over the generic Exception one.
    app.add_exception_handler(OperationalError, database_unavailable_handler)
    app.add_exception_handler(SATimeoutError, database_unavailable_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    # The split-deploy frontend origin is always allowed; CORS_ALLOW_ORIGINS
    # stays available for additional custom domains.
    allowed_origins: list[str] = []
    for origin in (
        settings.CORS_ALLOW_ORIGINS.split(",") + [settings.FRONTEND_URL]
    ):
        origin = origin.strip()
        if origin and origin not in allowed_origins:
            allowed_origins.append(origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health/live")
    def liveness() -> dict[str, str]:
        """Process liveness only: never restart-loop on a database outage."""
        return {"status": "ok"}

    @app.get("/api/health")
    @app.get("/api/health/ready")
    def readiness() -> dict[str, str]:
        """Readiness: the service cannot serve its main API without the DB."""
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}

    @app.middleware("http")
    async def request_observability(request: Request, call_next):
        request_id = _request_id(request)
        request.state.request_id = request_id
        context_token = request_id_var.set(request_id)
        started = time.perf_counter()
        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - started) * 1000
            _apply_security_headers(response, request.url.path, request_id, settings)
            _log_access(request, response.status_code, duration_ms)
            return response
        except Exception:
            duration_ms = (time.perf_counter() - started) * 1000
            _log_access(request, 500, duration_ms)
            raise
        finally:
            request_id_var.reset(context_token)

    from app.routers import (
        admin,
        auth,
        chat,
        client_errors,
        problems,
        profiles,
        projects,
        recommendations,
        stats,
        visitors,
    )

    auth.setup_oauth(app)
    app.include_router(problems.router)
    app.include_router(stats.router)
    app.include_router(visitors.router)
    app.include_router(projects.router)
    app.include_router(admin.router)
    app.include_router(admin.problems_router)
    app.include_router(auth.router)
    app.include_router(chat.router)
    app.include_router(recommendations.router)
    app.include_router(profiles.router)
    app.include_router(client_errors.router)

    return app


app = create_app()
