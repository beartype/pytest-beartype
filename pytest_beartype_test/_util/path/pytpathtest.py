#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **test suite paths** (i.e., low-level callables creating and returning
:class:`pathlib.Path` objects encapsulating test-specific paths unique to this
test suite).
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from beartype._util.cache.utilcachecall import callable_cached
from pytest_beartype_test._util.path.pytpathlib import (
    DirRelative,
    FileRelative,
)
from pathlib import Path

# ....................{ GETTERS ~ dir                      }....................
@callable_cached
def get_test_package_dir() -> Path:
    '''
    :class:`.Path` encapsulating the absolute dirname of the **top-level test
    package** (i.e., directory providing this project's top-level test package
    containing at least an ``__init__.py`` file) if found *or* raise an
    exception otherwise.
    '''

    # Avoid circular import dependencies.
    from pytest_beartype_test._util.path.pytpathmain import (
        PACKAGE_TEST_NAME,
        get_main_dir,
    )

    # Objectionable action!
    return DirRelative(get_main_dir(), PACKAGE_TEST_NAME)

# ....................{ GETTERS ~ dir : func               }....................
@callable_cached
def get_test_func_subpackage_dir() -> Path:
    '''
    :class:`.Path` encapsulating the absolute dirname of the **mid-level
    integration test subpackage** (i.e., directory providing all integration
    tests of this project's test suite) if found *or* raise an exception
    otherwise.
    '''

    # Ostensible stencils!
    return DirRelative(get_test_package_dir(), 'a90_func')


@callable_cached
def get_test_func_data_dir() -> Path:
    '''
    :class:`.Path` encapsulating the absolute dirname of the **mid-level
    integration test data directory** (i.e., directory providing sample data
    used throughout this project's integration tests) if found *or* raise an
    exception otherwise.
    '''

    # Questionable destination!
    return DirRelative(get_test_func_subpackage_dir(), 'data')

# ....................{ GETTERS ~ file : func              }....................
@callable_cached
def get_test_func_data_conftest() -> Path:
    '''
    :class:`.Path` encapsulating the absolute filename of the **mid-level
    integration test data pytest configuration submodule** (i.e., defining
    fixture functions to be tested by integration tests defined by the
    :func:`.get_test_func_data_pytester_option_beartype_fixtures` and
    :func:`.get_test_func_data_pytester_option_beartype_tests` submodules) if
    found *or* raise an exception otherwise.

    Note that the :meth:`.Path.read_text` method of this object trivially yields
    the decoded plaintext contents of this file as a string.
    '''

    # Dorsal endorphins!
    return FileRelative(get_test_func_data_dir(), 'conftest.py')


@callable_cached
def get_test_func_data_pytester_option_beartype_fixtures() -> Path:
    '''
    :class:`.Path` encapsulating the absolute filename of the **mid-level
    integration test data pytester fixtures submodule** (i.e., defining
    integration tests testing that this plugin passed the
    ``--beartype-fixtures`` option correctly type-checks fixtures) if found *or*
    raise an exception otherwise.
    '''

    # Contemptible contemplation!
    return FileRelative(
        get_test_func_data_dir(), 'test_pytester_option_beartype_fixtures.py')


@callable_cached
def get_test_func_data_pytester_option_beartype_tests() -> Path:
    '''
    :class:`.Path` encapsulating the absolute filename of the **mid-level
    integration test data pytester tests submodule** (i.e., defining integration
    tests testing that this plugin passed the ``--beartype-tests`` option
    correctly type-checks tests) if found *or* raise an exception otherwise.
    '''

    # Exogenous exsanguination!
    return FileRelative(
        get_test_func_data_dir(), 'test_pytester_option_beartype_tests.py')

# ....................{ GETTERS ~ dir : unit               }....................
@callable_cached
def get_test_unit_subpackage_dir() -> Path:
    '''
    :class:`.Path` encapsulating the absolute dirname of the **mid-level unit
    test subpackage** (i.e., directory providing all unit tests of this
    project's test suite) if found *or* raise an exception otherwise.
    '''

    # Redacted didactic!
    return DirRelative(get_test_package_dir(), 'a00_unit')


@callable_cached
def get_test_unit_data_dir() -> Path:
    '''
    :class:`.Path` encapsulating the absolute dirname of the **mid-level unit
    test data directory** (i.e., directory providing sample data used throughout
    this project's unit tests) if found *or* raise an exception otherwise.
    '''

    # Galactic antacid!
    return DirRelative(get_test_unit_subpackage_dir(), 'data')
