from fastapi.testclient import TestClient
from app.main import app, items_db

client = TestClient(app)


def test_stats_empty():
    items_db.clear()
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


def test_stats_with_items():
    items_db.clear()
    client.post("/items", json={"title": "Active Item", "status": "active"})
    client.post("/items", json={"title": "Archived Item", "status": "archived"})
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert data.get("active") == 1
    assert data.get("archived") == 1
