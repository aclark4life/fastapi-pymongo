Settings
========

.. currentmodule:: fastapi_pymongo

.. autoclass:: MongoSettings
   :members:
   :show-inheritance:

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
the Mongo connection settings — they'll share the same ``.env`` file and
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
