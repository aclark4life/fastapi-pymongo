"""Minimal CRUD app: FastAPI + PyMongo Async, via fastapi-pymongo.

Run:
    pip install -e ".[dev]"
    uvicorn examples.quickstart.main:app --reload
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Depends, FastAPI, HTTPException
from pymongo.asynchronous.database import AsyncDatabase

from fastapi_pymongo import MongoSettings, PyObjectId, mongo_lifespan
from fastapi_pymongo.lifespan import get_database

settings = MongoSettings()
app = FastAPI(lifespan=mongo_lifespan(settings))
db_dependency = get_database(settings)


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)
    name: str
    price: float


@app.post("/items", response_model=Item)
async def create_item(item: Item, db: AsyncDatabase = Depends(db_dependency)):
    doc = item.model_dump(by_alias=True)
    await db.items.insert_one(doc)
    return doc


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str, db: AsyncDatabase = Depends(db_dependency)):
    doc = await db.items.find_one({"_id": PyObjectId(item_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return doc


@app.get("/items", response_model=list[Item])
async def list_items(db: AsyncDatabase = Depends(db_dependency)):
    return await db.items.find().to_list()


@app.delete("/items/{item_id}")
async def delete_item(item_id: str, db: AsyncDatabase = Depends(db_dependency)):
    result = await db.items.delete_one({"_id": PyObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}
