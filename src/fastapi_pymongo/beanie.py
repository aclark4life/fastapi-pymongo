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

from fastapi_pymongo.lifespan import _STATE_KEY
from fastapi_pymongo.settings import MongoSettings

if TYPE_CHECKING:
    from beanie import Document, UnionDoc, View


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
        client = AsyncMongoClient(settings.uri)
        setattr(app.state, _STATE_KEY, client)
        try:
            await init_beanie(
                database=client[settings.database], document_models=document_models
            )
            yield
        finally:
            await client.close()

    return lifespan
