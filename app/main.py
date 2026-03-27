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


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 100):
    all_items = list(items_db.values())
    total = len(all_items)
    paginated = all_items[skip : skip + limit]
    return {"items": paginated, "total": total, "skip": skip, "limit": limit}


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


@app.patch("/items/{item_id}")
async def update_item(item_id: str, update: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item = items_db[item_id]
    if update.title is not None:
        item["title"] = update.title
    if update.description is not None:
        item["description"] = update.description
    if update.status is not None:
        item["status"] = update.status
    items_db[item_id] = item
    return item
