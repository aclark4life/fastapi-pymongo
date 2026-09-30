Quickstart
==========

This walks through the full example at
`examples/quickstart/main.py <https://github.com/aclark4life/fastapi-pymongo/blob/main/examples/quickstart/main.py>`_,
a minimal CRUD app.

1. Configure settings and lifespan
-----------------------------------

.. code-block:: python

   from fastapi import FastAPI
   from fastapi_pymongo import MongoSettings, mongo_lifespan
   from fastapi_pymongo.lifespan import get_database

   settings = MongoSettings()
   app = FastAPI(lifespan=mongo_lifespan(settings))
   db_dependency = get_database(settings)

``MongoSettings`` reads ``MONGO_URI`` and ``MONGO_DATABASE`` from the
environment (or a ``.env`` file), defaulting to
``mongodb://localhost:27017`` and ``app``. See :doc:`settings` to add
your own fields.

``mongo_lifespan(settings)`` opens an ``AsyncMongoClient`` on startup and
closes it on shutdown, storing it on ``app.state``. See :doc:`lifespan`
for details.

2. Define a model with a Pydantic-native ObjectId
--------------------------------------------------

.. code-block:: python

   from pydantic import BaseModel, ConfigDict, Field
   from fastapi_pymongo import PyObjectId

   class Item(BaseModel):
       model_config = ConfigDict(populate_by_name=True)

       id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)
       name: str
       price: float

``PyObjectId`` validates from either a real ``ObjectId`` or a hex string,
and serializes to a plain string, so it round-trips through MongoDB
documents and shows up correctly in OpenAPI/Swagger. See :doc:`objectid`.

3. Write route handlers
------------------------

.. code-block:: python

   from fastapi import Depends, HTTPException
   from pymongo.asynchronous.database import AsyncDatabase

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

4. Run it
---------

.. code-block:: bash

   uvicorn examples.quickstart.main:app --reload

Then open ``http://localhost:8000/docs`` for the interactive Swagger UI.

Next steps
----------

- Full API reference: :doc:`api`.
