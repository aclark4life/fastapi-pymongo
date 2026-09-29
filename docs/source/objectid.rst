PyObjectId
==========

.. currentmodule:: fastapi_pymongo

.. autoclass:: PyObjectId
   :members:
   :show-inheritance:

Why this exists
----------------

MongoDB's ``ObjectId`` isn't a Pydantic- or JSON-native type. Passed
directly as a field type, Pydantic can't validate it, serialize it to
JSON, or generate a sane OpenAPI schema for it — the single most common
first-hour complaint in the FastAPI + MongoDB community (see
`fastapi#1515 <https://github.com/fastapi/fastapi/issues/1515>`_).

``PyObjectId`` is a thin ``bson.ObjectId`` subclass that:

- validates from either a real ``ObjectId`` instance or a valid hex string,
- serializes to a plain string wherever Pydantic serializes the model
  (``.model_dump_json()``, FastAPI responses, etc.), and
- reports ``{"type": "string"}`` in the generated JSON Schema / OpenAPI
  docs.

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
  supplying ``_id`` yourself — ``default_factory=PyObjectId`` generates
  one.
- ``alias="_id"`` makes ``model_dump(by_alias=True)`` produce a document
  with the ``_id`` key MongoDB expects.

To look up a document by its id from a route's string path parameter:

.. code-block:: python

   doc = await db.items.find_one({"_id": PyObjectId(item_id)})

``PyObjectId(item_id)`` raises ``bson.errors.InvalidId`` if ``item_id``
isn't a valid ObjectId string — consider catching that and returning a 404
or 422 rather than a 500.

Relationship to PYTHON-4192
-----------------------------

MongoDB's driver team has a proof of concept
(`NoahStapp/mongo-python-driver#6 <https://github.com/NoahStapp/mongo-python-driver/pull/6>`_,
tracked as `PYTHON-4192 <https://jira.mongodb.org/browse/PYTHON-4192>`_)
that teaches PyMongo's ``document_class`` to decode BSON directly into a
Pydantic v2 model at the driver level. ``PyObjectId`` is a standalone way
to get similar day-to-day ergonomics today, without depending on a patched
driver. If PYTHON-4192 ships, this module may shrink or defer to it.
