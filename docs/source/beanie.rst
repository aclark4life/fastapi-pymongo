Beanie integration
====================

This walks through
`examples/beanie <https://github.com/aclark4life/fastapi-pymongo/tree/main/examples/beanie>`_,
the same CRUD app as :doc:`quickstart`, built on
`Beanie <https://github.com/BeanieODM/beanie>`_ instead of raw PyMongo.

``fastapi_pymongo`` does not implement an ODM (see :doc:`reference`).
This module is the lifespan wiring to run Beanie's own initialization
(``init_beanie``) alongside the rest of ``fastapi_pymongo``, reusing the
same client and settings. Nothing more.

.. currentmodule:: fastapi_pymongo.beanie

.. autofunction:: beanie_lifespan

Install
-------

.. code-block:: bash

   pip install "fastapi-pymongo[beanie]"

Usage
-----

Define a document as a ``beanie.Document``, a Pydantic model with an
auto-managed ``id`` field (Beanie's own ``PydanticObjectId``, not
:class:`fastapi_pymongo.PyObjectId`. See below):

.. code-block:: python

   from beanie import Document

   class Item(Document):
       name: str
       price: float

       class Settings:
           name = "items"

Wire it up with :func:`beanie_lifespan` instead of
:func:`fastapi_pymongo.mongo_lifespan`:

.. code-block:: python

   from fastapi import FastAPI
   from fastapi_pymongo import MongoSettings
   from fastapi_pymongo.beanie import beanie_lifespan

   settings = MongoSettings()
   app = FastAPI(lifespan=beanie_lifespan(settings, document_models=[Item]))

Route handlers use Beanie's document API directly. No manual
``model_dump``/``find_one`` calls:

.. code-block:: python

   @app.post("/items", response_model=Item)
   async def create_item(item: Item):
       return await item.insert()

   @app.get("/items/{item_id}", response_model=Item)
   async def get_item(item_id: str):
       item = await Item.get(item_id)
       if item is None:
           raise HTTPException(status_code=404, detail="Item not found")
       return item

Run it:

.. code-block:: bash

   uvicorn examples.beanie.main:app --reload

Verified end to end against a real MongoDB instance: create, list, get,
and delete all round-trip correctly, including a 404 after delete.

Where PyObjectId fits
------------------------

It doesn't, for Beanie models. Beanie ships its own ``PydanticObjectId``
and manages the ``id`` field itself. :class:`fastapi_pymongo.PyObjectId`
is for the raw-PyMongo path (see :doc:`quickstart` and :doc:`objectid`),
not for documents defined as ``beanie.Document`` subclasses.

Using both in the same app
-----------------------------

:func:`beanie_lifespan` stores the client on ``app.state`` the same way
:func:`fastapi_pymongo.mongo_lifespan` does, so
:func:`fastapi_pymongo.lifespan.get_client` and
:func:`fastapi_pymongo.lifespan.get_database` keep working for any route
that wants the raw PyMongo database alongside Beanie document classes.
Use one lifespan (``beanie_lifespan``, since it also runs
``init_beanie``), not both.
