# fastapi-pymongo

FastAPI integration for PyMongo:

- `PyObjectId` — a Pydantic-native `ObjectId` that validates and serializes
  to a plain string, with a correct OpenAPI/JSON schema.
- `MongoSettings` — a `pydantic-settings` base class for the Mongo URI and
  database name (subclass it to add your own app settings).
- `mongo_lifespan` / `get_client` / `get_database` — client lifecycle wired
  to FastAPI's `lifespan`, exposed to route handlers via `Depends()`.
- `beanie_lifespan` (optional, `fastapi-pymongo[beanie]`) — runs
  [Beanie](https://github.com/BeanieODM/beanie)'s `init_beanie` alongside
  the rest of `fastapi_pymongo`, for anyone who wants an ODM on top.

## Install

```bash
pip install -e ".[dev]"
```

## Examples

- [`examples/quickstart`](examples/quickstart) — a minimal CRUD app, raw PyMongo.
- [`examples/beanie`](examples/beanie) — the same CRUD app on
  [Beanie](https://github.com/BeanieODM/beanie) instead. Verified against
  a real MongoDB instance (create/list/get/delete).

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

## Spike questions

Answers to the [INTPYTHON-1087](https://jira.mongodb.org/browse/INTPYTHON-1087) definition-of-done questions, as of this repo.

**What is the minimum requirement to set up a FastAPI server that connects to MongoDB?**
An `AsyncMongoClient`, opened once in FastAPI's `lifespan` and exposed to route handlers via `Depends()` — see `mongo_lifespan`/`get_client`/`get_database` and [`examples/quickstart`](examples/quickstart).

**How can we leverage FastAPI mechanisms (such as Pydantic) to improve the experience of using MongoDB with FastAPI?**
The recurring friction is `_id`: it isn't a valid Python field name (Pydantic treats a leading underscore as private, so it needs `Field(alias="_id")`), and `ObjectId` isn't a Pydantic/JSON-native type (Pydantic can't validate, serialize, or generate an OpenAPI schema for it without help). `PyObjectId` solves the second half; `MongoSettings` (built on `pydantic-settings`) reuses the same model-based pattern for config.

**Technical feasibility for a thin wrapper on PyMongo dedicated to FastAPI (Pydantic-native ObjectId/BSON types, JSON serialization, client lifecycle via lifespan + DI, settings/config helpers)?**
Feasible — built and tested. `PyObjectId` (types + JSON serialization), `MongoSettings` (config), `mongo_lifespan`/`get_client`/`get_database` (lifecycle + DI) are all in `src/fastapi_pymongo/`, with unit tests and a working example app.

**Prototype the API surface on PyMongo Async — quickstart CRUD app.**
Done: [`examples/quickstart`](examples/quickstart). Verified — imports cleanly, generates a valid OpenAPI schema.

**Packaging: name, PyPI availability, repo location?**
Name `fastapi-pymongo`, confirmed available on PyPI and as a GitHub repo name at the time of checking. Repo: `aclark4life/fastapi-pymongo` (currently private). Not released to PyPI yet.

**Define the boundary with Beanie, or whether an ODM layer is needed.**
No first-party ODM — see `docs/source/reference.rst` for why (an ODM is a large, ongoing maintenance commitment; MongoDB's own prior attempt, PyMODM, was paused and archived). `beanie_lifespan` (optional `fastapi-pymongo[beanie]` extra) runs Beanie's `init_beanie` alongside the rest of this package for anyone who wants a full ODM on top, reusing the same client/settings. See [`examples/beanie`](examples/beanie) — verified against a real MongoDB instance. `PyObjectId` doesn't apply to Beanie models; Beanie manages its own `id` field.

**Define where to set the client metadata and how to update it.**
Not yet addressed — open item.

**Cost estimation for implementation, including a Pydantic/FastAPI version-compatibility matrix, ownership, and release cadence.**
Not yet addressed — open item.

## Related Jira tickets

- [INTPYTHON-1087](https://jira.mongodb.org/browse/INTPYTHON-1087) — [SPIKE] FastAPI integration library for MongoDB (the spike this repo exists to prototype)
- [INTPYTHON-382](https://jira.mongodb.org/browse/INTPYTHON-382) — [FastAPI] Update full stack fastapi template to match modern repo (Blocked; the official-template gap this package is an alternative path around)
- [INTPYTHON-565](https://jira.mongodb.org/browse/INTPYTHON-565) — CF: Django MongoDB Backend & Django Ninja support (Backlog; the Django-side precedent for a Pydantic-schema integration)
- [PYTHON-3372](https://jira.mongodb.org/browse/PYTHON-3372) — Alt to full-stack-fastapi-postgresql (Epic, Dev Complete)
- [PYTHON-5543](https://jira.mongodb.org/browse/PYTHON-5543) — pymongo 4.15+fastapi fails to connect to replicaset (Closed)
