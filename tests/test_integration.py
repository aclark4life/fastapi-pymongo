"""Integration tests: round-trip through a real MongoDB deployment.

Requires a running server. Set MONGODB_URI (default mongodb://localhost:27017).
Skip these locally with: pytest -m "not integration".
"""

import asyncio
from uuid import uuid4

import pytest
from bson import ObjectId
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from fastapi_pymongo import MongoSettings, PyObjectId, get_client, mongo_lifespan
from fastapi_pymongo.lifespan import get_database

pytestmark = pytest.mark.integration


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)
    name: str


@pytest.fixture
def app_and_db():
    settings = MongoSettings(database=f"test_{uuid4().hex}")
    app = FastAPI(lifespan=mongo_lifespan(settings))
    db_dependency = get_database(settings)

    @app.post("/items", response_model=Item)
    async def create_item(item: Item, db: AsyncDatabase = Depends(db_dependency)):
        doc = item.model_dump(by_alias=True)
        await db.items.insert_one(doc)
        return doc

    @app.get("/items/{item_id}", response_model=Item)
    async def get_item(item_id: str, db: AsyncDatabase = Depends(db_dependency)):
        if not PyObjectId.is_valid(item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        doc = await db.items.find_one({"_id": PyObjectId(item_id)})
        if doc is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return doc

    yield app, settings.database

    async def _drop():
        async with AsyncMongoClient(settings.uri) as cleanup:
            await cleanup.drop_database(settings.database)

    asyncio.run(_drop())


@pytest.fixture
def client(app_and_db):
    app, _ = app_and_db
    with TestClient(app) as test_client:
        yield test_client


def test_create_returns_24_hex_string_id(client):
    response = client.post("/items", json={"name": "widget"})
    assert response.status_code == 200
    item_id = response.json()["_id"]
    assert isinstance(item_id, str)
    assert ObjectId.is_valid(item_id)


def test_round_trip_id_survives_database_and_response(client):
    response = client.post("/items", json={"name": "widget"})
    item_id = response.json()["_id"]

    fetched = client.get(f"/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["_id"] == item_id
    assert fetched.json()["name"] == "widget"


def test_malformed_id_returns_404_not_500(client):
    assert client.get("/items/not-an-object-id").status_code == 404
    assert client.get("/items/507f1f77bcf86cd79943901z").status_code == 404


def test_unknown_id_returns_404(client):
    unknown = str(ObjectId())
    assert client.get(f"/items/{unknown}").status_code == 404


def test_stored_id_is_objectid_not_string(client, app_and_db):
    """Python-mode dumps insert a real ObjectId, so reads by id do not 404."""
    _, database = app_and_db
    item_id = client.post("/items", json={"name": "widget"}).json()["_id"]
    uri = MongoSettings().uri

    async def _read():
        async with AsyncMongoClient(uri) as raw:
            return await raw[database].items.find_one({"_id": ObjectId(item_id)})

    doc = asyncio.run(_read())
    assert doc is not None
    assert isinstance(doc["_id"], ObjectId)
    assert doc["_id"] == ObjectId(item_id)


def test_get_client_without_lifespan_raises():
    from fastapi import Request

    request = Request({"type": "http", "app": FastAPI()})
    with pytest.raises(RuntimeError, match="lifespan=mongo_lifespan"):
        get_client(request)


def test_handshake_driver_name_reaches_server(client):
    """Atlas must be able to attribute the connection: driver.name."""
    uri = MongoSettings().uri

    async def _driver_names():
        async with AsyncMongoClient(uri) as probe:
            ops = await probe.admin.command(
                "aggregate",
                1,
                pipeline=[
                    {"$currentOp": {"idleConnections": True}},
                    {"$match": {"clientMetadata.driver.name": {"$exists": True}}},
                ],
                cursor={},
            )
            return {op["clientMetadata"]["driver"]["name"] for op in ops["cursor"]["firstBatch"]}

    names = asyncio.run(_driver_names())
    # Report what the server saw, to diagnose handshake attribution gaps.
    assert any("fastapi-pymongo" in name for name in names), sorted(names)
