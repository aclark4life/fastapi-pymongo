"""Optional Beanie integration.

Beanie (https://github.com/BeanieODM/beanie) is a full ODM: schema
validation, a query builder, and document relationships, all on top of
Pydantic. ``fastapi_pymongo`` doesn't provide any of that (see the
"Why a thin wrapper, not an ODM" note in the docs). This module is just
the lifespan wiring to run ``init_beanie`` alongside the rest of
``fastapi_pymongo``, reusing the same client and settings.

Requires the ``beanie`` extra: ``pip install fastapi-pymongo[beanie]``.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, AsyncIterator, Sequence

from beanie import init_beanie
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from pymongo.driver_info import DriverInfo

from fastapi_pymongo.lifespan import _DRIVER_METADATA, _STATE_KEY
from fastapi_pymongo.settings import MongoSettings

if TYPE_CHECKING:
    from beanie import Document, UnionDoc, View

# Distinguishes this lifespan from mongo_lifespan's in $currentOp.clientMetadata.driver.name.
_BEANIE_DRIVER_METADATA = DriverInfo(
    name="fastapi-pymongo[beanie]", version=_DRIVER_METADATA.version
)


def beanie_lifespan(
    settings: MongoSettings,
    document_models: Sequence[type["Document"] | type["UnionDoc"] | type["View"] | str],
):
    """Build a FastAPI ``lifespan`` that opens the client, runs ``init_beanie``, and closes on shutdown.

    This replaces :func:`fastapi_pymongo.mongo_lifespan`. Use one or the
    other, not both. The client it opens is stored the same way, so
    :func:`fastapi_pymongo.get_client` and
    :func:`fastapi_pymongo.lifespan.get_database` keep working unchanged
    for any route that wants the raw PyMongo database alongside Beanie
    document classes.

    Usage::

        settings = MongoSettings()
        app = FastAPI(lifespan=beanie_lifespan(settings, document_models=[Item]))
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # init_beanie also calls database.client.append_metadata(name="beanie").
        # That doesn't reliably reach the server: it misses each server's
        # monitor pool, which performs the actual hello handshake (see the
        # comment on _DRIVER_METADATA in lifespan.py). Only the driver=
        # argument at client construction, below, is verified to work. So
        # only "fastapi-pymongo[beanie]" is guaranteed to show up
        # server-side, not "beanie" as well.
        client = AsyncMongoClient(settings.uri, driver=_BEANIE_DRIVER_METADATA)
        setattr(app.state, _STATE_KEY, client)
        try:
            await init_beanie(
                database=client[settings.database], document_models=document_models
            )
            yield
        finally:
            await client.close()

    return lifespan
