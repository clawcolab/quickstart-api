from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI(title="Quickstart API", version="0.1.0")

# In-memory store
items_db: dict = {}


class Item(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "active"


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/items")
async def list_items():
    return {"items": list(items_db.values()), "total": len(items_db)}


@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items", status_code=201)
async def create_item(item: Item):
    item_id = str(uuid.uuid4())
    record = {
        "id": item_id,
        "title": item.title,
        "description": item.description,
        "status": item.status,
        "created_at": datetime.utcnow().isoformat()
    }
    items_db[item_id] = record
    return record


@app.get("/stats")
async def get_stats():
    counts = {}
    for item in items_db.values():
        status = item.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    counts["total"] = len(items_db)
    return counts
