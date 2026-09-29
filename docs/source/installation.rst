Installation
============

.. code-block:: bash

   pip install fastapi-pymongo

To run the :doc:`Celery example <celery>` too:

.. code-block:: bash

   pip install "fastapi-pymongo[examples]"

For local development (tests, the quickstart app):

.. code-block:: bash

   git clone https://github.com/aclark4life/fastapi-pymongo
   cd fastapi-pymongo
   pip install -e ".[dev]"
   pytest

Requirements
------------

- Python 3.10+
- FastAPI 0.110+
- Pydantic 2.0+
- PyMongo 4.9+ (for the async client)
