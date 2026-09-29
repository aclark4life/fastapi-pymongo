"""FastAPI app that enqueues Celery tasks and reads results back with the async client.

This is the sync-worker / async-app split from the EDU team's feedback
(INTPYTHON-1087): the route handlers below only ever touch the async
PyMongo client; `worker.py`'s Celery task only ever touches the sync one.
Both read `MongoSettings` from the same environment, so they agree on the
URI and database name, but they are two separate clients — there is no
unified sync/async client yet.

Run (three processes):
    redis-server
    celery -A examples.celery_worker.worker worker --loglevel=info
    uvicorn examples.celery_worker.main:app --reload
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Depends, FastAPI, HTTPException
from pymongo.asynchronous.database import AsyncDatabase

from fastapi_pymongo import MongoSettings, PyObjectId, mongo_lifespan
from fastapi_pymongo.lifespan import get_database

from .worker import process_item

settings = MongoSettings()
app = FastAPI(lifespan=mongo_lifespan(settings))
db_dependency = get_database(settings)


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)
    name: str
    processed: bool = False


@app.post("/items", response_model=Item)
async def create_item(item: Item, db: AsyncDatabase = Depends(db_dependency)):
    doc = item.model_dump(by_alias=True)
    await db.items.insert_one(doc)
    return doc


@app.post("/items/{item_id}/process")
async def enqueue_processing(item_id: str, db: AsyncDatabase = Depends(db_dependency)):
    """Enqueue background processing for an item, via Celery (sync client)."""
    doc = await db.items.find_one({"_id": PyObjectId(item_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Item not found")
    process_item.delay(item_id)
    return {"queued": True}


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str, db: AsyncDatabase = Depends(db_dependency)):
    """Poll processing status, via the async client the rest of the app uses."""
    doc = await db.items.find_one({"_id": PyObjectId(item_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return doc
