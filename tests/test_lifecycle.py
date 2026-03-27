from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_full_item_lifecycle():
    # Create
    resp = client.post("/items", json={"title": "Lifecycle Item", "status": "active"})
    assert resp.status_code == 201
    item_id = resp.json()["id"]

    # Get
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Lifecycle Item"

    # Update (PATCH)
    resp = client.patch(f"/items/{item_id}", json={"title": "Updated Item"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Item"

    # Delete
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 204

    # Verify gone
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404
