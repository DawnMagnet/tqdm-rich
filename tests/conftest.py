"""
Pytest configuration and fixtures for tqdm_rich tests.
"""

import time
from typing import Generator

import pytest


@pytest.fixture
def slow_iterable() -> Generator[int, None, None]:
    """
    A slow iterable that simulates work.

    Yields:
        Numbers from 0 to 9 with a small delay between each
    """
    for i in range(10):
        time.sleep(0.01)
        yield i


@pytest.fixture
def fast_iterable():
    """
    A fast iterable for quick tests.

    Returns:
        Range of 100 numbers
    """
    return range(100)
