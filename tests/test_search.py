from fastapi.testclient import TestClient
from app.main import app, items_db

client = TestClient(app)


def test_search_matching():
    items_db.clear()
    client.post("/items", json={"title": "Python tutorial"})
    client.post("/items", json={"title": "JavaScript guide"})
    resp = client.get("/items/search?q=python")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert "python" in data["items"][0]["title"].lower()


def test_search_case_insensitive():
    items_db.clear()
    client.post("/items", json={"title": "Python tutorial"})
    resp = client.get("/items/search?q=PYTHON")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1


def test_search_empty_returns_all():
    items_db.clear()
    client.post("/items", json={"title": "Item 1"})
    client.post("/items", json={"title": "Item 2"})
    resp = client.get("/items/search?q=")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
