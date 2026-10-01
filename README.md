# fastapi-pymongo

FastAPI integration for PyMongo:

- `PyObjectId`: Pydantic-native `ObjectId`. Validates and serializes to a string, correct OpenAPI/JSON schema.
- `MongoSettings`: `pydantic-settings` base class for Mongo URI and database name. Subclass to add app settings.
- `mongo_lifespan` / `get_client` / `get_database`: client lifecycle wired to FastAPI's `lifespan`, exposed via `Depends()`.
- `beanie_lifespan` (optional, `fastapi-pymongo[beanie]`): runs [Beanie](https://github.com/BeanieODM/beanie)'s `init_beanie` alongside the rest of `fastapi_pymongo`, for an ODM on top.

## Install

```bash
pip install -e ".[dev]"
```

## Examples

- [`examples/quickstart`](examples/quickstart): minimal CRUD app, raw PyMongo.
- [`examples/beanie`](examples/beanie): same CRUD app on Beanie. Verified against a real MongoDB instance (create/list/get/delete).

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Documentation

Sphinx docs (furo theme) under `docs/source`:

```bash
pip install -e ".[docs]"
sphinx-build -b html docs/source docs/build
open docs/build/index.html
```

## References

- [INTPYTHON-1087](https://jira.mongodb.org/browse/INTPYTHON-1087): [SPIKE] FastAPI integration library for MongoDB. This repo is the prototype. DoD answers:
  - **Minimum setup?** `AsyncMongoClient` via FastAPI `lifespan` and `Depends()`. See `mongo_lifespan`/`get_client`/`get_database`, [`examples/quickstart`](examples/quickstart).
  - **Leverage FastAPI/Pydantic?** `_id` isn't a valid Python field name or a Pydantic/JSON-native type. `PyObjectId` fixes serialization and schema. `MongoSettings` reuses the same model pattern for config.
  - **Thin wrapper feasible?** Yes. Built and tested: `PyObjectId`, `MongoSettings`, `mongo_lifespan`/`get_client`/`get_database`.
  - **Quickstart CRUD prototype?** Done. [`examples/quickstart`](examples/quickstart).
  - **Packaging?** Name `fastapi-pymongo`, [reserved on PyPI](https://pypi.org/project/fastapi-pymongo/).
  - **Beanie boundary?** No first-party ODM. See `docs/source/reference.rst` for why (MongoDB's PyMODM precedent was paused and archived). `beanie_lifespan` runs Beanie's `init_beanie` alongside this package for anyone who wants one. See [`examples/beanie`](examples/beanie), verified against real MongoDB. `PyObjectId` doesn't apply to Beanie models — `Document` already provides its own ObjectId field (`beanie.PydanticObjectId`).
  - **Client metadata?** Set at client construction via `AsyncMongoClient(uri, driver=DriverInfo(name="fastapi-pymongo", version=...))` in `mongo_lifespan`/`beanie_lifespan`. Verified against a real server (`$currentOp.clientMetadata.driver.name`). PyMongo's `client.append_metadata(...)` for an already-open client does not reliably reach the per-server monitor pool, filed as [PYTHON-6130](https://jira.mongodb.org/browse/PYTHON-6130); closed, Works as Designed. Don't rely on it for monitor connections; set metadata at construction instead.
  - **Cost estimate?** 0. The prototype already covers the DoD: `PyObjectId`, `MongoSettings`, `mongo_lifespan`/`get_client`/`get_database`, the Beanie boundary, client metadata, and a published alpha (`0.1.0a0` on PyPI).
- [INTPYTHON-382](https://jira.mongodb.org/browse/INTPYTHON-382): [FastAPI] Update full stack fastapi template to match modern repo. Blocked. The official-template gap this package is an alternative path around.
- [INTPYTHON-565](https://jira.mongodb.org/browse/INTPYTHON-565): CF: Django MongoDB Backend and Django Ninja support. Backlog. The Django-side precedent for a Pydantic-schema integration.
- [PYTHON-3372](https://jira.mongodb.org/browse/PYTHON-3372): Alt to full-stack-fastapi-postgresql. Epic, dev complete.
- [PYTHON-5543](https://jira.mongodb.org/browse/PYTHON-5543): pymongo 4.15+fastapi fails to connect to replicaset. Closed.
