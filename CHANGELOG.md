# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
