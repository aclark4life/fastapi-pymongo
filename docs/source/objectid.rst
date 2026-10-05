PyObjectId
==========

.. currentmodule:: fastapi_pymongo

.. autoclass:: PyObjectId
   :members:
   :show-inheritance:

Why
----------------

MongoDB's ``ObjectId`` isn't a Pydantic- or JSON-native type. Pydantic
can't validate it, serialize it to JSON, or generate an OpenAPI schema
for it directly. This is the most common first-hour complaint in the
FastAPI + MongoDB community (see
`fastapi#9074 <https://github.com/fastapi/fastapi/discussions/9074>`_).

``PyObjectId`` is a thin ``bson.ObjectId`` subclass that:

- validates from either a real ``ObjectId`` instance or a valid hex string,
- serializes to a plain string wherever Pydantic serializes the model
  (``.model_dump_json()``, FastAPI responses, etc.), and
- reports ``{"type": "string"}`` in the generated JSON Schema / OpenAPI
  docs.

Why not ``pydantic_extra_types.MongoObjectId``
--------------------------------------------------

`pydantic-extra-types <https://github.com/pydantic/pydantic-extra-types>`_
ships a ``MongoObjectId`` with the same goal. Differences:

- it subclasses ``str`` while validating to ``ObjectId`` instances, so
  ``isinstance`` checks and direct use in PyMongo queries (``{"_id": item.id}``)
  are less predictable,
- it serializes with ``when_used="json"``, so ``.model_dump()`` yields an
  ``ObjectId`` while ``.model_dump(mode="json")`` yields a string — two
  shapes depending on mode, and
- it adds a dependency for ~30 lines this package already owns and tests.

``PyObjectId`` subclasses ``bson.ObjectId`` directly: it is an ``ObjectId``,
always serializes to a plain string, and needs no extra dependency.

Why not ``beanie.PydanticObjectId``
--------------------------------------------------

`Beanie <https://github.com/BeanieODM/beanie>`_'s ``PydanticObjectId``
solves the same problem, well — but it requires installing Beanie, a full
ODM, to get one field type. If you are already using Beanie, use
``beanie.PydanticObjectId`` (see :doc:`beanie`). If you are on raw PyMongo,
``PyObjectId`` gives you the field without the ODM.

Usage
-----

.. code-block:: python

   from pydantic import BaseModel, ConfigDict, Field
   from fastapi_pymongo import PyObjectId

   class Item(BaseModel):
       model_config = ConfigDict(populate_by_name=True)

       id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)
       name: str

- ``populate_by_name=True`` lets you construct ``Item(name=...)`` without
  supplying ``_id``. ``default_factory=PyObjectId`` generates one.
- ``alias="_id"`` makes ``model_dump(by_alias=True)`` produce a document
  with the ``_id`` key MongoDB expects.

To look up a document by its id from a route's string path parameter:

.. code-block:: python

   doc = await db.items.find_one({"_id": PyObjectId(item_id)})

``PyObjectId(item_id)`` raises ``bson.errors.InvalidId`` if ``item_id``
isn't a valid ObjectId string. Consider catching that and returning a 404
or 422 rather than a 500.
