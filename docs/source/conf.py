from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "fastapi-pymongo"
copyright = "2026, Alex Clark"
author = "Alex Clark"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_member_order = "bysource"
autodoc_typehints = "description"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
}

html_theme = "furo"
html_static_path = ["_static"]
html_title = "fastapi-pymongo"
