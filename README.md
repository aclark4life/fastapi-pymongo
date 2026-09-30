# fastapi-pymongo

FastAPI integration for PyMongo:

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
```

## Examples

- [`examples/quickstart`](examples/quickstart) — a minimal CRUD app.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Documentation

Sphinx docs (furo theme) live under `docs/source`:

```bash
pip install -e ".[docs]"
sphinx-build -b html docs/source docs/build
open docs/build/index.html
```

## Related Jira tickets

- [INTPYTHON-1087](https://jira.mongodb.org/browse/INTPYTHON-1087) — [SPIKE] FastAPI integration library for MongoDB (the spike this repo exists to prototype)
- [PYTHON-4192](https://jira.mongodb.org/browse/PYTHON-4192) — Support data validation classes (dataclass, pydantic, custom class...) as `document_class` (Noah Stapp's PoC; see Background above)
- [INTPYTHON-382](https://jira.mongodb.org/browse/INTPYTHON-382) — [FastAPI] Update full stack fastapi template to match modern repo (Blocked; the official-template gap this package is an alternative path around)
- [INTPYTHON-565](https://jira.mongodb.org/browse/INTPYTHON-565) — CF: Django MongoDB Backend & Django Ninja support (Backlog; the Django-side precedent for a Pydantic-schema integration)
- [PYTHON-3372](https://jira.mongodb.org/browse/PYTHON-3372) — Alt to full-stack-fastapi-postgresql (Epic, Dev Complete)
- [PYTHON-5543](https://jira.mongodb.org/browse/PYTHON-5543) — pymongo 4.15+fastapi fails to connect to replicaset (Closed)
