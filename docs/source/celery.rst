Celery worker
=============

This walks through
`examples/celery_worker <https://github.com/aclark4life/fastapi-pymongo/tree/main/examples/celery_worker>`_ —
a FastAPI app that enqueues Celery tasks.

The problem
------------

Celery has no async support. If your FastAPI app also runs Celery tasks
(e.g. for background jobs), those tasks need a *synchronous* PyMongo
client, while the rest of your app uses the *async* one. This is a
real-world pain point: an internal MongoDB team running FastAPI + Celery +
MongoDB in production named exactly this as their one significant friction
point — maintaining two separate PyMongo clients.

There is no unified sync/async PyMongo client today. This example does not
solve that; it shows the two clients sharing configuration cleanly instead.

The pattern
------------

Both the app and the worker read the same :class:`~fastapi_pymongo.MongoSettings`,
so they agree on the URI and database — but they open two separate clients.

``worker.py`` — the Celery task, using the sync client:

.. code-block:: python

   from celery import Celery
   from pymongo import MongoClient
   from fastapi_pymongo import MongoSettings, PyObjectId

   settings = MongoSettings()
   celery_app = Celery("fastapi_pymongo_example", broker="redis://localhost:6379/0")

   _client: MongoClient | None = None

   def _get_sync_database():
       global _client
       if _client is None:
           _client = MongoClient(settings.uri)
       return _client[settings.database]

   @celery_app.task(name="process_item")
   def process_item(item_id: str) -> str:
       db = _get_sync_database()
       db.items.update_one({"_id": PyObjectId(item_id)}, {"$set": {"processed": True}})
       return item_id

The client is built lazily, on first use inside the task — not at import
time — so importing ``worker`` from the FastAPI app (to call ``.delay()``)
never opens a connection from the web process.

``main.py`` — the FastAPI route, using the async client:

.. code-block:: python

   from fastapi_pymongo import MongoSettings, mongo_lifespan
   from fastapi_pymongo.lifespan import get_database
   from .worker import process_item

   settings = MongoSettings()
   app = FastAPI(lifespan=mongo_lifespan(settings))
   db_dependency = get_database(settings)

   @app.post("/items/{item_id}/process")
   async def enqueue_processing(item_id: str, db=Depends(db_dependency)):
       doc = await db.items.find_one({"_id": PyObjectId(item_id)})
       if doc is None:
           raise HTTPException(status_code=404, detail="Item not found")
       process_item.delay(item_id)
       return {"queued": True}

Running it
-----------

Three processes:

.. code-block:: bash

   redis-server
   celery -A examples.celery_worker.worker worker --loglevel=info
   uvicorn examples.celery_worker.main:app --reload

Install the extra dependencies first:

.. code-block:: bash

   pip install "fastapi-pymongo[dev,examples]"
