from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_ping():
    assert client.get("/api/core/ping").json()["pong"] is True


def test_infra_check_without_keys_returns_503(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    assert client.get("/api/core/infra-check").status_code == 503
