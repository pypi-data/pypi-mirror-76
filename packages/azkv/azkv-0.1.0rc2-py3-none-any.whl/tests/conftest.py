# -*- coding: utf-8 -*-
"""Module defines common test fixtures."""
from cement import fs
from logging import getLogger

import pytest


@pytest.fixture(scope="session")
def logger():
    """Provide logger instance."""
    logger = getLogger(__name__)

    return logger


@pytest.fixture(scope="function")
def tmp(request):
    """
    Create a `tmp` object that generates a unique temporary directory, and file
    for each test function that requires it.
    """
    t = fs.Tmp()
    yield t
    t.remove()
