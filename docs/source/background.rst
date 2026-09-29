Background
==========

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
than patching the driver's decode path. If PYTHON-4192 ships, this
package's types module can shrink or defer to it.

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
