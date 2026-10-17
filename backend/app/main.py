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
    if not is_local and settings.SESSION_SECRET == DEFAULT_SESSION_SECRET:
        raise RuntimeError(
            "SESSION_SECRET is still the placeholder value — generate a long random string "
            "(python -c \"import secrets; print(secrets.token_urlsafe(32))\") before deploying."
        )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from app import models  # noqa: F401  (ensures tables are registered)
    from app.db import Base

    Base.metadata.create_all(get_engine())
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
        return response

    from app.routers import auth, chat, ingest, ml, problems, profiles, projects, recommendations, stats

    auth.setup_oauth(app)
    app.include_router(problems.router)
    app.include_router(stats.router)
    app.include_router(projects.router)
    app.include_router(auth.router)
    app.include_router(ingest.router)
    app.include_router(ml.router)
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
    candidate = (dist / full_path).resolve()
    if not candidate.is_relative_to(dist.resolve()):
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
