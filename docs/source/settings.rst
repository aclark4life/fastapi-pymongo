Settings
========

.. currentmodule:: fastapi_pymongo

.. autoclass:: MongoSettings
   :members:
   :show-inheritance:

Why
---

FastAPI apps commonly read config from the environment, with different
values per deployment (local, staging, production). ``MongoSettings``
gives the Mongo connection the same treatment, using
`pydantic-settings <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>`_
so connection settings validate and type-check like the rest of the app's
configuration, instead of ad-hoc ``os.environ`` reads scattered through the code.

Usage
-----

By default, ``MongoSettings`` reads from the environment (or a ``.env``
file in the current directory):

.. list-table::
   :header-rows: 1

   * - Field
     - Env var
     - Default
   * - ``uri``
     - ``MONGO_URI``
     - ``mongodb://localhost:27017``
   * - ``database``
     - ``MONGO_DATABASE``
     - ``app``

.. code-block:: python

   from fastapi_pymongo import MongoSettings

   settings = MongoSettings()

Adding your own settings
--------------------------

Subclass ``MongoSettings`` to add application-specific fields alongside
the Mongo connection settings. They share the same ``.env`` file and
prefix handling:

.. code-block:: python

   from fastapi_pymongo import MongoSettings

   class Settings(MongoSettings):
       jwt_secret: str
       debug: bool = False

   settings = Settings()

Overriding for tests
----------------------

Pass fields directly to skip the environment/``.env`` file, e.g. to point
tests at an ephemeral database:

.. code-block:: python

   settings = MongoSettings(uri="mongodb://localhost:27017", database="test_db")
