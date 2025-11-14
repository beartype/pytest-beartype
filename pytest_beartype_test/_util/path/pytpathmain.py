#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **main codebase paths** (i.e., low-level callables creating and
returning :class:`pathlib.Path` objects encapsulating test-agnostic paths
applicable to the codebase being tested).
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

# ....................{ GLOBALS                            }....................
PACKAGE_NAME = 'pytest_beartype'
'''
Fully-qualified name of the top-level Python package containing this submodule.
'''


PACKAGE_TEST_NAME = f'{PACKAGE_NAME}_test'
'''
Fully-qualified name of the top-level Python package testing this project.
'''

# ....................{ GETTERS ~ dir                      }....................
@callable_cached
def get_main_dir() -> Path:
    '''
    :class:`.Path` encapsulating the absolute dirname of the **top-level project
    directory** (i.e., directory containing both a ``.git/`` subdirectory and a
    subdirectory providing this project's package) if found *or* raise an
    exception otherwise.
    '''
    # print(f'current module paths: {__package__} [{__file__}]')

    # Path encapsulating the current module.
    MODULE_FILE = Path(__file__)

    # Path encapsulating the current module's package.
    MODULE_PACKAGE_DIR = MODULE_FILE.parent

    # Path encapsulating the relative dirname of this project's directory
    # relative to the dirname of the package defining the current module.
    MAIN_DIR = DirRelative(MODULE_PACKAGE_DIR, '../../..')

    # If this project's directory either does not contain a "beartype_test"
    # subdirectory *OR* does but this path is not a directory, raise an
    # exception. This basic sanity check improves the likelihood that this
    # project directory is what we assume it is.
    #
    # Note that we intentionally avoid testing paths *NOT* bundled with release
    # tarballs (e.g., a root ".git/" directory), as doing so would prevent
    # external users and tooling from running tests from release tarballs.
    DirRelative(MAIN_DIR, PACKAGE_TEST_NAME)

    # Return this path.
    return MAIN_DIR


@callable_cached
def get_main_package_dir() -> Path:
    '''
    :mod:`Path` encapsulating the absolute dirname of the **top-level project
    package** (i.e., directory providing this package's top-level package
    containing at least an ``__init__.py`` file) if found *or* raise an
    exception otherwise.
    '''

    # Terrifying terseness!
    return DirRelative(get_main_dir(), PACKAGE_NAME)

# ....................{ GETTERS ~ file                     }....................
@callable_cached
def get_main_mypy_config_file() -> Path:
    '''
    :mod:`Path` encapsulating the absolute filename of this project's **mypy
    configuration file** (i.e., top-level ``.mypy.ini`` file) if found *or*
    raise an exception otherwise.
    '''

    # Obverse obviation!
    return FileRelative(get_main_dir(), 'mypy.ini')


@callable_cached
def get_main_readme_file() -> Path:
    '''
    :mod:`Path` encapsulating the absolute filename of the **project readme
    file** (i.e., this project's front-facing ``README.md`` file) if found *or*
    raise an exception otherwise.

    Note that the :meth:`.Path.read_text` method of this object trivially yields
    the decoded plaintext contents of this file as a string.
    '''

    # Perverse pomposity!
    return FileRelative(get_main_dir(), 'README.md')
