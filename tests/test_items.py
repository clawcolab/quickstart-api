from fastapi.testclient import TestClient
from app.main import app, items_db

client = TestClient(app)


def setup_function():
    """Clear the in-memory store before each test."""
    items_db.clear()


def test_create_item_valid():
    """POST /items with valid title returns 201 and the created item."""
    resp = client.post("/items", json={"title": "Test Item"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Item"
    assert data["status"] == "active"
    assert "id" in data
    assert "created_at" in data


def test_create_item_with_description():
    """POST /items with title and description returns both fields."""
    resp = client.post("/items", json={"title": "My Item", "description": "A test item"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My Item"
    assert data["description"] == "A test item"


def test_create_item_missing_title():
    """POST /items without title returns 422 validation error."""
    resp = client.post("/items", json={"description": "No title here"})
    assert resp.status_code == 422


def test_create_item_empty_body():
    """POST /items with empty body returns 422 validation error."""
    resp = client.post("/items", json={})
    assert resp.status_code == 422


def test_create_item_null_title():
    """POST /items with null title returns 422 validation error."""
    resp = client.post("/items", json={"title": None})
    assert resp.status_code == 422


def test_created_item_appears_in_list():
    """Item created via POST shows up in GET /items."""
    client.post("/items", json={"title": "Listed Item"})
    resp = client.get("/items")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Listed Item"


def test_list_items_pagination_limit():
    """GET /items with limit returns at most limit items."""
    for i in range(5):
        client.post("/items", json={"title": f"Item {i}"})
    resp = client.get("/items", params={"limit": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 3
    assert data["limit"] == 3


def test_list_items_pagination_skip():
    """GET /items with skip skips the first skip items."""
    for i in range(5):
        client.post("/items", json={"title": f"Item {i}"})
    resp = client.get("/items", params={"skip": 2, "limit": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["skip"] == 2
    assert data["limit"] == 2


def test_list_items_pagination_defaults():
    """GET /items without params returns all items with correct metadata."""
    client.post("/items", json={"title": "Only Item"})
    resp = client.get("/items")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["skip"] == 0
    assert data["limit"] == 100
