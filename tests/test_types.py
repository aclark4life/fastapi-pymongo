import json

import pytest
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from fastapi_pymongo import PyObjectId


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)
    name: str


def test_validates_from_objectid():
    oid = ObjectId()
    item = Item(_id=oid, name="widget")
    assert item.id == oid


def test_validates_from_string():
    oid = ObjectId()
    item = Item(_id=str(oid), name="widget")
    assert item.id == oid


def test_rejects_invalid_string():
    with pytest.raises(ValueError):
        Item(_id="not-an-object-id", name="widget")


def test_serializes_to_string_in_json():
    oid = ObjectId()
    item = Item(_id=oid, name="widget")
    payload = json.loads(item.model_dump_json(by_alias=True))
    assert payload["_id"] == str(oid)
    assert isinstance(payload["_id"], str)


def test_json_schema_is_string():
    schema = Item.model_json_schema()
    assert schema["properties"]["_id"] == {
        "type": "string",
        "minLength": 24,
        "maxLength": 24,
        "pattern": "^[0-9a-f]{24}$",
        "example": "507f1f77bcf86cd799439011",
        "title": "Id",
    }
