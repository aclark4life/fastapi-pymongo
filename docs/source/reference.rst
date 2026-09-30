Reference
=========

Why a thin wrapper, not an ODM
--------------------------------

``fastapi-pymongo`` does not persist objects, build queries, or manage
relationships. That's what full ODMs like
`Beanie <https://github.com/BeanieODM/beanie>`_ do, and do well. This
package covers only two narrow, recurring friction points at the
FastAPI/PyMongo boundary:

- ``ObjectId`` not being a Pydantic/JSON-native type, and
- wiring a client into FastAPI's lifespan and dependency injection.

For querying, relationships, or schema migrations, reach for an ODM on
top of this, or Beanie directly. See :doc:`beanie`:
:func:`fastapi_pymongo.beanie.beanie_lifespan` runs Beanie's own
initialization alongside the rest of ``fastapi_pymongo``, reusing the
same client and settings.

See the repo `README <https://github.com/aclark4life/fastapi-pymongo#related-jira-tickets>`_
for related Jira tickets.
