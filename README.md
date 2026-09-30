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

## Related Jira tickets

- [INTPYTHON-1087](https://jira.mongodb.org/browse/INTPYTHON-1087) — [SPIKE] FastAPI integration library for MongoDB (the spike this repo exists to prototype)
- [INTPYTHON-382](https://jira.mongodb.org/browse/INTPYTHON-382) — [FastAPI] Update full stack fastapi template to match modern repo (Blocked; the official-template gap this package is an alternative path around)
- [INTPYTHON-565](https://jira.mongodb.org/browse/INTPYTHON-565) — CF: Django MongoDB Backend & Django Ninja support (Backlog; the Django-side precedent for a Pydantic-schema integration)
- [PYTHON-3372](https://jira.mongodb.org/browse/PYTHON-3372) — Alt to full-stack-fastapi-postgresql (Epic, Dev Complete)
- [PYTHON-5543](https://jira.mongodb.org/browse/PYTHON-5543) — pymongo 4.15+fastapi fails to connect to replicaset (Closed)
