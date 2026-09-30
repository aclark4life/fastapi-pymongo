"""Pydantic-native BSON types."""

from __future__ import annotations

from typing import Any

from bson import ObjectId as _ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


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
