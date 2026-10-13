Installation
============

.. code-block:: bash

   pip install fastapi-pymongo

For local development (tests, the quickstart app):

.. code-block:: bash

   git clone https://github.com/aclark4life/fastapi-pymongo
   cd fastapi-pymongo
   pip install -e ".[dev]"
   pytest

Requirements
------------

- Python 3.11+ (matching PyMongo's supported versions)
- FastAPI 0.110+
- Pydantic 2.10+
- Pydantic-settings 2.12+
- PyMongo 4.9+ (for the async client)
