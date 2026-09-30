"""Pydantic-native BSON types."""

from __future__ import annotations

from typing import Any

from bson import ObjectId as _ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

# Relationship to PYTHON-4192 (NoahStapp/mongo-python-driver#6): that PoC
# teaches PyMongo's document_class to decode BSON directly into a Pydantic
# v2 model or dataclass. That's the driver boundary (BSON <-> Python
# object, inside insert_one/find_one). PyObjectId operates at a different
# boundary: Python object <-> JSON, where FastAPI turns a Pydantic model
# into an HTTP response body and an OpenAPI schema. Not competing
# solutions to the same problem:
#
# - Native document_class support removes per-route model_dump/model_validate
#   boilerplate and covers the whole driver surface (bulk_write, find,
#   aggregate, change streams, GridFS), for every PyMongo consumer, not
#   just FastAPI apps.
# - PyObjectId still has to exist either way. Native document_class support
#   doesn't teach Pydantic how to render ObjectId as a JSON string or
#   describe it in an OpenAPI schema, so an `id: PyObjectId` field keeps
#   needing this serializer/schema regardless. No driver-version coupling,
#   works on any currently supported PyMongo.
#
# Net effect if PYTHON-4192 ships: the manual model_dump/model_validate glue
# at each route shrinks. Not this module.


class PyObjectId(_ObjectId):
    """``bson.ObjectId`` that validates from and serializes to a plain string.

    Use it as a field type on any Pydantic model that round-trips through
    MongoDB documents, e.g.::

        class Item(BaseModel):
            id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)
            model_config = ConfigDict(populate_by_name=True)
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def _validate(cls, value: Any) -> PyObjectId:
        if isinstance(value, _ObjectId):
            return cls(value)
        if isinstance(value, str) and _ObjectId.is_valid(value):
            return cls(value)
        raise ValueError(f"{value!r} is not a valid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "example": "507f1f77bcf86cd799439011"}
