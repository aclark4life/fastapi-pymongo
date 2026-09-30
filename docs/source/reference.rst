Reference
=========

Why a thin wrapper, not an ODM
--------------------------------

``fastapi-pymongo`` does not persist objects, build queries, or manage
relationships — that is squarely what full ODMs like
`Beanie <https://github.com/roman-right/beanie>`_ do, and do well.
This package covers only the narrow, recurring friction points at the
FastAPI ↔ PyMongo boundary itself:

- ``ObjectId`` not being a Pydantic/JSON-native type, and
- wiring a client into FastAPI's lifespan and dependency injection.

If you need querying, relationships, or schema migrations, reach for an
ODM on top of this — or Beanie directly. See :doc:`beanie` for how the
two compose: :func:`fastapi_pymongo.beanie.beanie_lifespan` runs Beanie's
own initialization alongside the rest of ``fastapi_pymongo``, reusing the
same client and settings.

Related Jira tickets
-----------------------

- `INTPYTHON-1087 <https://jira.mongodb.org/browse/INTPYTHON-1087>`_ —
  [SPIKE] FastAPI integration library for MongoDB (the spike this repo
  exists to prototype)
- `INTPYTHON-382 <https://jira.mongodb.org/browse/INTPYTHON-382>`_ —
  [FastAPI] Update full stack fastapi template to match modern repo
  (Blocked)
- `INTPYTHON-565 <https://jira.mongodb.org/browse/INTPYTHON-565>`_ — CF:
  Django MongoDB Backend & Django Ninja support (Backlog)
- `PYTHON-3372 <https://jira.mongodb.org/browse/PYTHON-3372>`_ — Alt to
  full-stack-fastapi-postgresql (Epic, Dev Complete)
- `PYTHON-5543 <https://jira.mongodb.org/browse/PYTHON-5543>`_ — pymongo
  4.15+fastapi fails to connect to replicaset (Closed)
