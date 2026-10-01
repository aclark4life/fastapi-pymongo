# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- `beanie_lifespan` now tags its client as `fastapi-pymongo[beanie]` in
  `$currentOp.clientMetadata.driver.name`, distinct from `mongo_lifespan`'s
  `fastapi-pymongo`.

## [0.1.0a0] - 2026-10-01

Alpha release to reserve the package name on PyPI.
