from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_ok_and_db_responds():
    with TestClient(app) as client:
        res = client.get("/api/health", headers={"X-Request-ID": "health-check-1"})
        ready = client.get("/api/health/ready")
        live = client.get("/api/health/live")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    assert res.headers["X-Request-ID"] == "health-check-1"
    assert ready.status_code == 200 and ready.json() == {"status": "ok"}
    assert live.status_code == 200 and live.json() == {"status": "ok"}
