Client lifecycle
=================

.. currentmodule:: fastapi_pymongo.lifespan

.. autofunction:: mongo_lifespan
.. autofunction:: get_client
.. autofunction:: get_database

Why
---

FastAPI recommends opening long-lived resources like a database client
once, in the app's ``lifespan``, rather than per-request. ``mongo_lifespan``
does exactly that for an ``AsyncMongoClient``, and stores it on
``app.state`` so route handlers can reach it through a dependency instead
of a global.

Usage
-----

.. code-block:: python

   from fastapi import FastAPI
   from fastapi_pymongo import MongoSettings, mongo_lifespan
   from fastapi_pymongo.lifespan import get_client, get_database

   settings = MongoSettings()
   app = FastAPI(lifespan=mongo_lifespan(settings))

Inject the whole client:

.. code-block:: python

   from fastapi import Depends
   from pymongo import AsyncMongoClient

   @app.get("/ping")
   async def ping(client: AsyncMongoClient = Depends(get_client)):
       await client.admin.command("ping")
       return {"ok": True}

Or inject the configured database directly — the common case:

.. code-block:: python

   from pymongo.asynchronous.database import AsyncDatabase

   db_dependency = get_database(settings)

   @app.get("/items")
   async def list_items(db: AsyncDatabase = Depends(db_dependency)):
       return await db.items.find().to_list()

What this does *not* do
-------------------------

There is no connection pooling configuration, retry policy, or
multi-cluster routing here beyond what ``AsyncMongoClient(settings.uri)``
gives you by default. If you need multiple clusters, construct additional
clients and dependencies the same way, one per URI.
