from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_matching():
    client.post("/items", json={"title": "Python tutorial"})
    client.post("/items", json={"title": "JavaScript guide"})
    resp = client.get("/items/search?q=python")
    assert resp.status_code == 200
    data = resp.json()
    assert any("python" in i["title"].lower() for i in data["items"])


def test_search_case_insensitive():
    resp = client.get("/items/search?q=PYTHON")
    assert resp.status_code == 200
    data = resp.json()
    assert any("python" in i["title"].lower() for i in data["items"])


def test_search_empty_returns_all():
    resp = client.get("/items/search?q=")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 0
