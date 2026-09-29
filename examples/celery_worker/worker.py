"""Celery worker sharing MongoSettings with the FastAPI app.

Celery has no async support, so its tasks use the *sync* PyMongo client
(``pymongo.MongoClient``) while the FastAPI app uses the async one
(``pymongo.AsyncMongoClient``, via ``mongo_lifespan``). This is the two
separate PyMongo clients pattern from the EDU team's feedback
(INTPYTHON-1087) — sharing configuration (``MongoSettings``), not a
connection. There is no unified sync/async client today; see the fork
question in fastapi-pymongo#1 in this repo's DoD notes.

Run:
    celery -A examples.celery_worker.worker worker --loglevel=info
"""

from __future__ import annotations

from celery import Celery
from pymongo import MongoClient

from fastapi_pymongo import MongoSettings, PyObjectId

settings = MongoSettings()
celery_app = Celery("fastapi_pymongo_example", broker="redis://localhost:6379/0")

# One sync client per worker process, built lazily so importing this module
# (e.g. from the FastAPI app, to call .delay()) never opens a connection.
_client: MongoClient | None = None


def _get_sync_database():
    global _client
    if _client is None:
        _client = MongoClient(settings.uri)
    return _client[settings.database]


@celery_app.task(name="process_item")
def process_item(item_id: str) -> str:
    """Mark an item as processed. Runs in the Celery worker, via the sync client."""
    db = _get_sync_database()
    db.items.update_one({"_id": PyObjectId(item_id)}, {"$set": {"processed": True}})
    return item_id
