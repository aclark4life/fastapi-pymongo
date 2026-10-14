# fastapi-pymongo

FastAPI integration for PyMongo:

- `PyObjectId`: Pydantic-native `ObjectId`. Validates from `ObjectId` or hex string, serializes to a string in JSON mode (Python-mode dumps keep the `ObjectId`, so documents round-trip through `insert_one`), correct OpenAPI/JSON schema.
- `MongoSettings`: `pydantic-settings` base class for Mongo URI and database name. Subclass to add app settings.
- `mongo_lifespan` / `get_client` / `get_database`: client lifecycle wired to FastAPI's `lifespan`, exposed via `Depends()`.
- `beanie_lifespan` (optional, `fastapi-pymongo[beanie]`): runs [Beanie](https://github.com/BeanieODM/beanie)'s `init_beanie` alongside the rest of `fastapi_pymongo`, for an ODM on top.

## Install

```bash
pip install fastapi-pymongo
```

Optional Beanie integration:

```bash
pip install "fastapi-pymongo[beanie]"
```

## Examples

- [`examples/quickstart`](https://github.com/aclark4life/fastapi-pymongo/tree/main/examples/quickstart): minimal CRUD app, raw PyMongo.
- [`examples/beanie`](https://github.com/aclark4life/fastapi-pymongo/tree/main/examples/beanie): same CRUD app on Beanie. Verified against a real MongoDB instance (create/list/get/delete).

## Development

```bash
pip install -e ".[dev]"
pytest            # unit tests (integration and perf are deselected by default)
pytest -m perf    # PyObjectId overhead benchmarks
ruff check src tests examples
mypy src
```

Integration tests need a running MongoDB; set `MONGODB_URI` (default
`mongodb://localhost:27017`). Run the full suite with a local server, for
example via `mongodb-runner start --topology standalone`.

## Documentation

Sphinx docs (furo theme) under `docs/source`:

```bash
pip install -e ".[docs]"
sphinx-build -b html docs/source docs/build
open docs/build/index.html
```
