# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
