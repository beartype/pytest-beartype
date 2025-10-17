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
import sys

# ....................{ GLOBALS                            }....................
# Implicitly enable the standard "pytester" plugin required to test pytest
# plugins (namely, this one) from within a pytest test suite.
pytest_plugins = 'pytester'

# Prohibit generation of bytecode. Why? Because the standard "pytester" plugin
# (subsequently required by the "pytest_beartype_test.a90_func" subpackage)
# copies paths to "/tmp". If "/tmp" and "/home" reside on different filesystems,
# Python uselessly carps about bytecode inconsistency. Why? Because "pytester"
# still fetches the old bytecode while actually executing the "/tmp"-specific
# copies of that bytecode.
sys.dont_write_bytecode = True
