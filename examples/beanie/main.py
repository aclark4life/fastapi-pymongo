"""Minimal CRUD app: FastAPI + Beanie, via fastapi-pymongo's beanie_lifespan.

Compare against examples/quickstart/main.py, which does the same thing
with raw PyMongo and PyObjectId instead of an ODM.

Run:
    pip install -e ".[dev,beanie]"
    uvicorn examples.beanie.main:app --reload
"""

from __future__ import annotations

from beanie import Document
from fastapi import FastAPI, HTTPException

from fastapi_pymongo import MongoSettings
from fastapi_pymongo.beanie import beanie_lifespan

settings = MongoSettings()


class Item(Document):
    name: str
    price: float

    class Settings:
        name = "items"


app = FastAPI(lifespan=beanie_lifespan(settings, document_models=[Item]))


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    return await item.insert()


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = await Item.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items", response_model=list[Item])
async def list_items():
    return await Item.find_all().to_list()


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    item = await Item.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()
    return {"deleted": True}
