# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0a3] - 2026-10-13

### Changed

- Dependency floors corrected to versions verified against a live MongoDB:
  `pydantic>=2.10`, `pydantic-settings>=2.12`, Python 3.11+ (matching
  PyMongo). Pydantic-settings below 2.12 silently lets the environment
  override keyword arguments when a `validation_alias` is set; Pydantic
  below 2.10 renders the wrong OpenAPI title.
- CI now runs version-floor jobs (core and Beanie extra), a weekly
  dependency pre-release job, weekly `pip-audit`, and ruff plus mypy.
- Releases publish on tag push: the workflow builds, publishes to PyPI via
  trusted publishing, and creates the GitHub release with the dist
  artifacts and a CycloneDX SBOM attached.

### Added

- `pytest -m perf` measures `PyObjectId` validation and serialization
  overhead against a raw `ObjectId` baseline. Excluded from normal runs.
- Docs: verified comparison sections for `pydantic_extra_types.MongoObjectId`,
  `beanie.PydanticObjectId`, and the `pyobjectid` PyPI package.

## [0.1.0a2] - 2026-10-08

### Fixed

- `PyObjectId` serializes to a string only in JSON mode. `model_dump()` now
  yields the `ObjectId` itself, so `model_dump(by_alias=True)` produces a
  document with a BSON `_id` that round-trips: `insert_one` and
  `find_one`/`delete_one` agree on the id type.
- The quickstart app returns 404 instead of 500 for an invalid id path
  parameter, via a `PyObjectId.is_valid` guard.

## [0.1.0a1] - 2026-10-05

### Changed

- `MongoSettings` now reads `MONGODB_URI` and `MONGODB_DATABASE` instead of
  `MONGO_URI` and `MONGO_DATABASE`, matching the conventional `MONGODB_*`
  environment-variable names.
- `PyObjectId` now emits `minLength`, `maxLength`, and `pattern` in its JSON
  schema, so OpenAPI consumers reject malformed ObjectIds from the schema
  alone.
- `beanie_lifespan` now tags its client as `fastapi-pymongo[beanie]` in
  `$currentOp.clientMetadata.driver.name`, distinct from `mongo_lifespan`'s
  `fastapi-pymongo`.

## [0.1.0a0] - 2026-10-01

Alpha release to reserve the package name on PyPI.
