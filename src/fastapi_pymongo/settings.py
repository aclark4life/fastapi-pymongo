from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    """MongoDB connection settings, loadable from the environment or a ``.env`` file.

    Subclass to add application-specific settings alongside these::

        class Settings(MongoSettings):
            jwt_secret: str
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)

    uri: str = Field(default="mongodb://localhost:27017", validation_alias="MONGODB_URI")
    database: str = Field(default="app", validation_alias="MONGODB_DATABASE")
