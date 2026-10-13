"""Performance overhead test for PyObjectId, per the ODM performance-benchmark
guidelines (10gen/odm-guidelines: warm-up, iterations, median, comparison
against a raw-driver baseline). fastapi-pymongo adds no query-path code; the
only measurable overhead is ObjectId validation and serialization.

Not run in normal CI (per the guidelines, long-running benchmarks do not
belong on every PR). Run explicitly with:

    pytest -m perf
"""

import time
from statistics import median

import pytest
from bson import ObjectId
from pydantic import BaseModel

from fastapi_pymongo import PyObjectId

pytestmark = pytest.mark.perf

HEX_IDS = [str(ObjectId()) for _ in range(1000)]

# Generous regression bounds, not performance targets. Median per-operation
# cost of one hex validation was well under 10 microseconds at time of
# writing; these bounds exist to catch order-of-magnitude regressions.
VALIDATE_BOUND_SECONDS = 50e-6
DUMP_JSON_BOUND_SECONDS = 50e-6


class Item(BaseModel):
    id: PyObjectId


def _measure(fn, *, warmup=3, iterations=10):
    """Median wall time of one fn() call, after warm-up. Modeled on the
    benchmarking spec: enough calls per iteration that the operation
    dominates timing code, median for outlier robustness."""
    for _ in range(warmup):
        fn()
    timings = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        timings.append((time.perf_counter() - start) / len(HEX_IDS))
    return median(timings)


def _baseline_roundtrip():
    for hex_id in HEX_IDS:
        ObjectId(hex_id)


def _validate():
    for hex_id in HEX_IDS:
        Item(id=hex_id)


def _dump_json():
    for hex_id in HEX_IDS:
        Item(id=hex_id).model_dump_json()


def test_overhead_versus_raw_objectid(capsys):
    baseline = _measure(_baseline_roundtrip)
    validate = _measure(_validate)
    dump_json = _measure(_dump_json)

    with capsys.disabled():
        print(f"\nraw ObjectId():            {baseline * 1e6:8.2f} us/op")
        print(f"Item(id=hex):              {validate * 1e6:8.2f} us/op")
        print(f"Item.model_dump_json():    {dump_json * 1e6:8.2f} us/op")

    assert validate < VALIDATE_BOUND_SECONDS
    assert dump_json < DUMP_JSON_BOUND_SECONDS
