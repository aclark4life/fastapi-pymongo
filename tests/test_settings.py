import pytest

from fastapi_pymongo import MongoSettings


def test_reads_mongodb_uri_from_env(monkeypatch):
    monkeypatch.setenv("MONGODB_URI", "mongodb://example.com:27017")
    monkeypatch.setenv("MONGODB_DATABASE", "prod")
    settings = MongoSettings()
    assert settings.uri == "mongodb://example.com:27017"
    assert settings.database == "prod"


def test_defaults():
    settings = MongoSettings(uri="mongodb://localhost:27017", database="test_db")
    assert settings.uri == "mongodb://localhost:27017"
    assert settings.database == "test_db"


def test_direct_init_overrides_env(monkeypatch):
    monkeypatch.setenv("MONGODB_URI", "mongodb://example.com:27017")
    settings = MongoSettings(uri="mongodb://other:27017")
    assert settings.uri == "mongodb://other:27017"
