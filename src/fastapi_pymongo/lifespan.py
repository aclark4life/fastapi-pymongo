"""Client lifecycle wired to FastAPI's lifespan, exposed via dependency injection."""

from __future__ import annotations

from contextlib import asynccontextmanager
from importlib.metadata import version
from typing import AsyncIterator

from fastapi import FastAPI, Request
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.driver_info import DriverInfo

from fastapi_pymongo.settings import MongoSettings

_STATE_KEY = "fastapi_pymongo_client"

# Internal: tags clients this package creates, for server-side logs and
# $currentOp.clientMetadata.driver.name. Not exposed to library consumers.
# Set via the `driver` argument at construction (see beanie.py for why:
# metadata set after construction, e.g. via append_metadata, doesn't
# reliably reach the server).
_DRIVER_METADATA = DriverInfo(name="fastapi-pymongo", version=version("fastapi-pymongo"))


def mongo_lifespan(settings: MongoSettings):
    """Build a FastAPI ``lifespan`` that opens the client on startup and closes it on shutdown.

    Usage::

        settings = MongoSettings()
        app = FastAPI(lifespan=mongo_lifespan(settings))
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        client = AsyncMongoClient(settings.uri, driver=_DRIVER_METADATA)
        setattr(app.state, _STATE_KEY, client)
        try:
            yield
        finally:
            await client.close()

    return lifespan


def get_client(request: Request) -> AsyncMongoClient:
    """FastAPI dependency returning the client opened by :func:`mongo_lifespan`.

    Usage::

        @app.get("/items")
        async def list_items(client: AsyncMongoClient = Depends(get_client)):
            ...
    """
    client = getattr(request.app.state, _STATE_KEY, None)
    if client is None:
        raise RuntimeError(
            "No MongoDB client on app.state. Did you set lifespan=mongo_lifespan(settings)?"
        )
    return client


def get_database(settings: MongoSettings):
    """FastAPI dependency returning the configured database on the shared client."""

    def _get_database(request: Request) -> AsyncDatabase:
        return get_client(request)[settings.database]

    return _get_database
