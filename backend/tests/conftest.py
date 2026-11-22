"""Shared test setup.

The public GET cache is process-wide by design, so tests that mutate the
catalog would otherwise see a payload cached by an earlier test in the same
run. Clear it around every test to keep each one independent.
"""

import pytest

from app.services.public_cache import PUBLIC_CACHE


@pytest.fixture(autouse=True)
def _clear_public_cache():
    PUBLIC_CACHE.clear()
    yield
    PUBLIC_CACHE.clear()
