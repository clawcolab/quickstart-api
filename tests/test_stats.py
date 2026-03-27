"""Tests for /stats endpoint."""

from fastapi.testclient import TestClient
from app.main import app, items_db


client = TestClient(app)


def setup_function():
    """Clear items DB before each test."""
    items_db.clear()


def test_stats_returns_counts_per_status():
    """Test that stats returns counts grouped by status."""
    # Add items with different statuses
    items_db["1"] = {"id": "1", "title": "A", "status": "active"}
    items_db["2"] = {"id": "2", "title": "B", "status": "active"}
    items_db["3"] = {"id": "3", "title": "C", "status": "archived"}
    
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["active"] == 2
    assert data["archived"] == 1


def test_stats_returns_total():
    """Test that stats returns total count."""
    items_db["1"] = {"id": "1", "title": "A", "status": "active"}
    items_db["2"] = {"id": "2", "title": "B", "status": "active"}
    
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2


def test_stats_empty_db_returns_zeros():
    """Test that empty DB returns zeros (no keys for missing statuses)."""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    # No status keys when DB is empty
    status_keys = [k for k in data if k != "total"]
    assert len(status_keys) == 0
