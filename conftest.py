#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Root test configuration** (i.e., early-time configuration guaranteed to be
run by :mod:`pytest` *before* passed command-line arguments are parsed) for
this test suite.

Caveats
-------
For safety, this configuration should contain *only* early-time hooks absolutely
required by :mod:`pytest` design to be defined in this configuration. Hooks for
which this is the case (e.g., :func:`pytest_addoption`) are explicitly annotated
as such in official :mod:`pytest` documentation with a note resembling:

    Note

    This function should be implemented only in plugins or ``conftest.py`` files
    situated at the tests root directory due to how pytest discovers plugins
    during startup.

This file is the aforementioned ``conftest.py`` file "...situated at the tests
root directory."
'''

# ....................{ IMPORTS                            }....................
from pathlib import Path
import pytest
import sys

# ....................{ GLOBALS                            }....................
# We prohibit generation of the bytecode because the pytester
# copies the files under /tmp and if /tmp and /home are on different
# devices, or, possibly, different architectures Python starts to spew out
# tons of warnings/errors about bytecode inconsistency, because it still fetches
# the old bytecode while executing the /tmp copy of the codebase
sys.dont_write_bytecode = True

pytest_plugins = 'pytester'

# ....................{ FIXTURES                           }....................
@pytest.fixture(scope='session')
def beartype_pytest_tests() -> list[Path]:
    '''
    Discover all test files under pytest_tests directory.
    '''

    return list(Path('tests/pytest_tests').rglob('*.py'))
