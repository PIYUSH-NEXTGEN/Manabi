"""Centralized logging for MANABI.

One place configures the root handler so the application, uvicorn, and library
loggers share a single format. Request-scoped values travel in a ContextVar:
an error logged deep inside a service still carries the request id that the
access log printed, which is what makes a production incident traceable.

Production emits one JSON object per line. Development and tests keep a compact
text line. Both formats redact credentials centrally, so no module has to
remember which field is sensitive.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

SERVICE_NAME = "manabi-api"

# Set by the request middleware; services log without passing it explicitly.
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

_SECRET_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Authorization headers, including Bearer tokens.
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]{8,}"), r"\1 ***"),
    # Common credential keys in free-form messages and exception text.
    (
        re.compile(
            r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|authorization|"
            r"cookie|set-cookie|github_token|access_token|refresh_token|"
            r"session|client_secret)\b\s*[:=]\s*['\"]?([^\s,'\"]{3,})"
        ),
        r"\1=***",
    ),
    # Provider-specific key shapes.
    (re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})"), "[redacted-token]"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{20,}"), "[redacted-token]"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{10,}"), "[redacted-token]"),
    # Database URLs with inline credentials.
    (
        re.compile(r"(?i)\b(postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://([^:\s/@]+):([^@\s]+)@"),
        r"\1://\2:***@",
    ),
)

_OPTIONAL_FIELDS = (
    "event",
    "method",
    "path",
    "status",
    "duration_ms",
    "error_type",
    "operation",
    "user_id",
    "component",
    "database",
    "project_id",
    "admin_id",
    "reason",
    "retry_after",
    "client_event",
    "client_route",
    "client_message",
    "client_stack",
    "component_stack",
    "client_app_version",
    "backend_request_id",
)


def redact(value: str) -> str:
    """Mask credentials that may appear in messages or exception text."""
    text = str(value)
    for pattern, replacement in _SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def _one_line(value: Any) -> str:
    return str(value).replace("\r", "\\r").replace("\n", "\\n")


def _version(settings: Any) -> str:
    configured = str(getattr(settings, "APP_VERSION", "") or "").strip()
    commit = os.environ.get("RENDER_GIT_COMMIT", "").strip()
    return (configured or commit or "dev")[:80]


class ContextFilter(logging.Filter):
    """Attach request, service, environment, and version fields to every record."""

    def __init__(self, environment: str, version: str):
        super().__init__()
        self.environment = environment
        self.version = version

    def filter(self, record: logging.LogRecord) -> bool:
        if not getattr(record, "request_id", None):
            record.request_id = request_id_var.get() or "-"
        if not getattr(record, "service", None):
            record.service = SERVICE_NAME
        if not getattr(record, "environment", None):
            record.environment = self.environment
        if not getattr(record, "version", None):
            record.version = self.version
        return True


class _BaseFormatter(logging.Formatter):
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        return (
            datetime.fromtimestamp(record.created, tz=UTC)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )

    def _error_type(self, record: logging.LogRecord) -> str | None:
        if record.exc_info and record.exc_info[0] is not None:
            return record.exc_info[0].__name__
        value = getattr(record, "error_type", None)
        return str(value) if value else None


class JsonFormatter(_BaseFormatter):
    """One JSON object per line, with predictable field names."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": getattr(record, "service", SERVICE_NAME),
            "environment": getattr(record, "environment", "unknown"),
            "version": getattr(record, "version", "dev"),
            "logger": record.name,
            "message": redact(record.getMessage()),
            "request_id": getattr(record, "request_id", "-"),
        }
        for field in _OPTIONAL_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = redact(value) if isinstance(value, str) else value
        error_type = self._error_type(record)
        if error_type:
            payload["error_type"] = error_type
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            payload["exception"] = redact(record.exc_text)
        return json.dumps(payload, default=str, ensure_ascii=True)


class TextFormatter(_BaseFormatter):
    """Compact single-line development log with the same fields."""

    def format(self, record: logging.LogRecord) -> str:
        parts = [
            self.formatTime(record),
            record.levelname,
            getattr(record, "service", SERVICE_NAME),
            record.name,
            f"[request_id={getattr(record, 'request_id', '-')}]",
            record.getMessage(),
        ]
        for field in _OPTIONAL_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                parts.append(f"{field}={_one_line(value)}")
        error_type = self._error_type(record)
        if error_type:
            parts.append(f"error_type={error_type}")
        line = " ".join(parts)
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            line = f"{line}\n{record.exc_text}"
        return redact(line)


def _existing_handler() -> logging.Handler | None:
    for handler in logging.getLogger().handlers:
        if getattr(handler, "_manabi", False):
            return handler
    return None


def configure_logging(settings: Any | None = None) -> None:
    """Configure the root logger once (safe to call again after settings change)."""
    if settings is None:
        from app.config import get_settings

        settings = get_settings()

    level_name = str(getattr(settings, "LOG_LEVEL", "INFO") or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    environment = str(getattr(settings, "APP_ENV", "development") or "development")
    version = _version(settings)

    log_format = str(getattr(settings, "LOG_FORMAT", "") or "").lower()
    if log_format not in {"json", "text"}:
        log_format = "json" if environment == "production" else "text"

    formatter: logging.Formatter = JsonFormatter() if log_format == "json" else TextFormatter()

    root = logging.getLogger()
    previous = _existing_handler()
    if previous is not None:
        root.removeHandler(previous)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    handler.addFilter(ContextFilter(environment, version))
    handler._manabi = True  # type: ignore[attr-defined]
    root.addHandler(handler)
    root.setLevel(level)

    # Third-party loggers are chatty and can include URLs. The application
    # emits its own dependency diagnostics, so keep these at WARNING.
    for name in ("httpx", "httpcore", "authlib"):
        logging.getLogger(name).setLevel(max(level, logging.WARNING))
    if level > logging.DEBUG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # Uvicorn normally formats its startup/error lines with its own handler,
    # which would put two formats in the same stream. Route them through the
    # root handler so a deploy log stays searchable end to end.
    for name in ("uvicorn", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True
    # Uvicorn decides whether to emit its plain access line from
    # access_logger.hasHandlers(), so propagating would re-enable it even with
    # --no-access-log. The app middleware is the single access log.
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    access_logger.propagate = False
