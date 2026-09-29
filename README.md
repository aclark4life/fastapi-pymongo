# fastapi-pymongo

Thin FastAPI integration for PyMongo. No ODM, no code generator — just the
minimum glue to use MongoDB from FastAPI comfortably:

- `PyObjectId` — a Pydantic-native `ObjectId` that validates and serializes
  to a plain string, with a correct OpenAPI/JSON schema.
- `MongoSettings` — a `pydantic-settings` base class for the Mongo URI and
  database name (subclass it to add your own app settings).
- `mongo_lifespan` / `get_client` / `get_database` — client lifecycle wired
  to FastAPI's `lifespan`, exposed to route handlers via `Depends()`.

## Status

Early scaffold (see [INTPYTHON-1087](https://jira.mongodb.org/browse/INTPYTHON-1087)).
Not released to PyPI yet.

## Background

MongoDB's own driver team has a proof of concept
([NoahStapp/mongo-python-driver#6](https://github.com/NoahStapp/mongo-python-driver/pull/6),
tracked as [PYTHON-4192](https://jira.mongodb.org/browse/PYTHON-4192)) that
teaches PyMongo's `document_class` to decode straight into a Pydantic v2
model or dataclass. That patch lives deep in the driver's sync/async
collection, database, and bulk-write code paths — it isn't a
`pip install`-able add-on today, and the ticket is unresolved.

This package takes a different, dependency-free path: a wrapper layer that
gets the same day-to-day ergonomics (Pydantic-native `ObjectId`, clean
FastAPI wiring) on top of stock PyMongo. If PYTHON-4192 ships, the `types`
module can shrink or defer to it — see the module docstring for the exact
boundary.

## Install

```bash
pip install -e ".[dev]"
# to run the Celery example too:
pip install -e ".[dev,examples]"
```

## Examples

- [`examples/quickstart`](examples/quickstart) — a minimal CRUD app.
- [`examples/celery_worker`](examples/celery_worker) — a FastAPI app that
  enqueues Celery tasks. Celery has no async support, so the worker uses a
  sync PyMongo client while the app uses the async one, both built from the
  same `MongoSettings`. This is the sync/async client-duplication pain
  point named in the EDU team's feedback on
  [INTPYTHON-1087](https://jira.mongodb.org/browse/INTPYTHON-1087) — there
  is no unified sync/async client yet, so this example shows the two
  clients sharing configuration rather than a connection.

## Development

```bash
pip install -e ".[dev]"
pytest
```
