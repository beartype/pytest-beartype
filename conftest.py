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
import pytest
import sys

# ....................{ GLOBALS                            }....................
# Implicitly enable the standard "pytester" plugin required to test pytest
# plugins (namely, this one) from within a pytest test suite.
pytest_plugins = 'pytester'

# Prohibit generation of bytecode. Why? Because the standard "pytester" plugin
# enabled below copies the files under "/tmp". If "/tmp" and "/home" reside on
# different devices, or, possibly, different architectures Python starts to spew
# out tons of warnings/errors about bytecode inconsistency. Why? Because
# "pytester" still fetches the old bytecode while executing the "/tmp" copy of
# the codebase.
sys.dont_write_bytecode = True

# ....................{ FIXTURES                           }....................
@pytest.fixture(scope='session')
def beartype_pytest_tests() -> list['pathlib.Path']:
    '''
    Session-scoped fixture listing the **paths** (i.e., :class:`pathlib.Path`
    objects) of all test files residing under the
    ``pytest_beartype_test/pytest_tests/`` subdirectory.
    '''

    # Defer fixture-specific imports.
    from pathlib import Path

    return list(Path('pytest_beartype_test/pytest_tests').rglob('*.py'))
