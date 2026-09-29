Reference
=========

Why a thin wrapper, not an ODM
--------------------------------

``fastapi-pymongo`` does not persist objects, build queries, or manage
relationships — that is squarely what full ODMs like
`Beanie <https://github.com/roman-right/beanie>`_ do, and do well.
This package covers only the narrow, recurring friction points at the
FastAPI ↔ PyMongo boundary itself:

- ``ObjectId`` not being a Pydantic/JSON-native type,
- wiring a client into FastAPI's lifespan and dependency injection,
- and sharing connection settings between an async web app and a sync
  worker (e.g. Celery).

If you need querying, relationships, or schema migrations, reach for an
ODM on top of this — or Beanie directly.

Relationship to PYTHON-4192
-----------------------------

MongoDB's driver team has an in-progress proof of concept,
`NoahStapp/mongo-python-driver#6 <https://github.com/NoahStapp/mongo-python-driver/pull/6>`_
(tracked as `PYTHON-4192 <https://jira.mongodb.org/browse/PYTHON-4192>`_),
that teaches PyMongo's ``document_class`` to decode BSON directly into a
Pydantic v2 model or dataclass. That patch touches PyMongo's sync and
async collection, database, and bulk-write code paths directly — it isn't
a ``pip install``-able add-on today, and the ticket is still unresolved
and unowned.

This package takes a different, dependency-free path to the same
day-to-day ergonomics: :class:`~fastapi_pymongo.PyObjectId` wraps
``bson.ObjectId`` at the Pydantic layer, on top of stock PyMongo, rather
than patching the driver's decode path.

Two different boundaries
~~~~~~~~~~~~~~~~~~~~~~~~~~

It's tempting to read PYTHON-4192 and ``PyObjectId`` as two competing
solutions to the same problem. They aren't — they operate at two
different boundaries, and (assuming PYTHON-4192 has no blockers to
merging) each has advantages the other doesn't cover:

1. **BSON ↔ Python object** — the driver boundary, inside
   ``insert_one``/``find_one``, where PyMongo talks to the wire protocol.
   This is what PYTHON-4192 changes.
2. **Python object ↔ JSON** — the API boundary, where FastAPI turns a
   Pydantic model into an HTTP response body and an OpenAPI schema. This
   is what ``PyObjectId`` covers.

**What native** ``document_class`` **support would add:**

- Eliminates per-route conversion boilerplate. Today, every route
  manually does ``item.model_dump(by_alias=True)`` before
  ``insert_one``, and reconstructs a model from the raw dict
  ``find_one`` returns. With native support, real Pydantic instances
  flow in and out directly: ``coll.insert_one(item)``,
  ``item = coll.find_one(...)``.
- Uniform coverage across the entire driver surface —
  ``bulk_write``, ``find``, ``aggregate``, change streams, GridFS,
  ``client_bulk_write`` — not just the call sites application code
  happens to touch.
- Benefits every PyMongo consumer, not just FastAPI apps: scripts, other
  frameworks, and ODMs built on top (Beanie included) get it for free,
  in one place.
- Type-checked at the call boundary — ``insert_one``/``find_one``
  become properly typed against the model class, instead of flowing
  through untyped dicts.

**What** ``PyObjectId`` **still provides, regardless of PYTHON-4192's fate:**

- It solves the *other* boundary. Native ``document_class`` support
  teaches PyMongo how to decode/encode BSON into a model — it does not
  teach Pydantic how to render ``ObjectId`` as a JSON string or describe
  it correctly in an OpenAPI schema. Even with native driver support,
  an ``id: PyObjectId`` field still needs this serializer/schema
  definition for FastAPI's response body and Swagger docs to work.
- No driver-version coupling — works on any currently supported PyMongo
  today, not gated on users upgrading to whichever version ships
  PYTHON-4192.
- Keeps the "raw document ↔ validated model" boundary explicit, for
  applications that want persistence-layer dicts and API-layer models
  to stay visibly separate rather than have Pydantic models flow all
  the way down into driver internals.

**Net effect if PYTHON-4192 ships:** what shrinks is the manual
``model_dump``/``model_validate`` glue code at each route — not
:class:`~fastapi_pymongo.PyObjectId` itself, which keeps doing its job
at the API boundary either way.

Related Jira tickets
-----------------------

- `INTPYTHON-1087 <https://jira.mongodb.org/browse/INTPYTHON-1087>`_ —
  [SPIKE] FastAPI integration library for MongoDB (the spike this repo
  exists to prototype)
- `PYTHON-4192 <https://jira.mongodb.org/browse/PYTHON-4192>`_ — Support
  data validation classes (dataclass, pydantic, custom class...) as
  ``document_class``
- `INTPYTHON-382 <https://jira.mongodb.org/browse/INTPYTHON-382>`_ —
  [FastAPI] Update full stack fastapi template to match modern repo
  (Blocked)
- `INTPYTHON-565 <https://jira.mongodb.org/browse/INTPYTHON-565>`_ — CF:
  Django MongoDB Backend & Django Ninja support (Backlog)
- `PYTHON-3372 <https://jira.mongodb.org/browse/PYTHON-3372>`_ — Alt to
  full-stack-fastapi-postgresql (Epic, Dev Complete)
- `PYTHON-5543 <https://jira.mongodb.org/browse/PYTHON-5543>`_ — pymongo
  4.15+fastapi fails to connect to replicaset (Closed)
- `UP-7645 <https://jira.mongodb.org/browse/UP-7645>`_ — Migrate FastAPI
  to Containerized App on Kanopy (Epic, In Progress)
- `UP-7031 <https://jira.mongodb.org/browse/UP-7031>`_ — Migrate FastAPI
  Lambda to Containerized Application (Epic, Backlog)
- `UP-6976 <https://jira.mongodb.org/browse/UP-6976>`_ — Phase 1 Tech Spec
  for Migrate FastAPI Lambda to Kanopy (Closed)
