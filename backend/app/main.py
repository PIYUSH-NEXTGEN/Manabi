from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import text

from app.config import get_settings
from app.db import get_engine


def frontend_dist() -> Path | None:
    """Serve frontend/dist when it exists (built frontend, step B11)."""
    dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    return dist if (dist / "index.html").is_file() else None


DEFAULT_SESSION_SECRET = "change-me-long-random-string"


def guard_deploy_secrets(settings) -> None:
    """Fail fast on obviously unsafe deploy settings (local dev keeps defaults)."""
    is_local = "localhost" in settings.BASE_URL or settings.BASE_URL.startswith("http://127.0.0.1")
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


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from app import models  # noqa: F401  (ensures tables are registered)
    from app.db import Base, normalized_database_url

    database_url = normalized_database_url(get_settings().DATABASE_URL)
    if database_url.startswith("sqlite"):
        # Local dev / tests keep the create-all convenience. Production
        # (Postgres) must never silently diverge from migrations (§6.1).
        Base.metadata.create_all(get_engine())
    else:
        from app.migrations import upgrade_to_head

        upgrade_to_head()
    yield
    get_engine().dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    guard_deploy_secrets(settings)
    app = FastAPI(title="MANABI API", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"] if "localhost" in settings.BASE_URL else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health() -> dict[str, str]:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}

    @app.middleware("http")
    async def basic_security_headers(request: Request, call_next):
        # Platform TLS/load balancer owns HSTS; these are process-level and free.
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        # This app never needs to be framed by another origin; deny it to
        # stop clickjacking of the session-backed buttons.
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Content-Security-Policy", "frame-ancestors 'none'")
        if request.url.path.startswith("/api/"):
            # Authenticated JSON (me, dashboard, admin) must not sit in browser
            # or intermediary caches where a shared machine could replay it.
            response.headers.setdefault("Cache-Control", "no-store")
        return response

    from app.routers import admin, auth, chat, problems, profiles, projects, recommendations, stats

    auth.setup_oauth(app)
    app.include_router(problems.router)
    app.include_router(stats.router)
    app.include_router(projects.router)
    app.include_router(admin.router)
    app.include_router(admin.problems_router)
    app.include_router(auth.router)
    app.include_router(chat.router)
    app.include_router(recommendations.router)
    app.include_router(profiles.router)

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa(request: Request, full_path: str):
        dist = frontend_dist()
        if dist is None:
            raise HTTPException(status_code=404, detail="Not found")
        return _spa_response(dist, full_path, request.headers.get("accept", ""))

    return app


def _spa_response(dist: Path, full_path: str, accept: str) -> FileResponse:
    """Serve an existing file; browser navigations fall back to index.html. Escape attempts → 404."""
    if full_path.startswith("api/") or full_path == "api":
        raise HTTPException(status_code=404, detail="Not found")
    try:
        root = dist.resolve()
        candidate = (dist / full_path).resolve()
    except OSError:
        # Windows raises for UNC/network paths and other unrepresentable
        # names instead of returning a path. Treat it as an escape.
        raise HTTPException(status_code=404, detail="Not found")
    if not candidate.is_relative_to(root):
        raise HTTPException(status_code=404, detail="Not found")
    if full_path and candidate.is_file():
        if full_path.startswith("assets/"):
            # Vite content-hashes these names: safe to cache forever.
            return FileResponse(candidate, headers={"Cache-Control": "public, max-age=31536000, immutable"})
        return FileResponse(candidate)
    # A missing asset (stale cache, broken deploy) must 404, never come back as HTML.
    if full_path and "text/html" not in accept:
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(dist / "index.html", headers={"Cache-Control": "no-cache"})


app = create_app()
