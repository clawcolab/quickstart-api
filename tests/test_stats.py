from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_stats_empty():
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


def test_stats_with_items():
    client.post("/items", json={"title": "Active Item", "status": "active"})
    client.post("/items", json={"title": "Archived Item", "status": "archived"})
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 2
    assert "active" in data
    assert "archived" in data
