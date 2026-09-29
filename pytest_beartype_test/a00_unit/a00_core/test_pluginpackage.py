#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin-wide **package utility** unit tests.

This submodule unit tests the public API of the :mod:`pytest_beartype` package
itself as implemented by the :mod:`pytest_beartype.__init__` submodule.
'''

# ....................{ TESTS                              }....................
def test_pytest_beartype_package() -> None:
    '''
    Test the public API of the :mod:`pytest_beartype` package itself.
    '''

    # Defer test-specific imports.
    import pytest_beartype

    # Assert this package's public attributes to be of the expected types.
    assert isinstance(pytest_beartype.__version__, str)
    assert isinstance(pytest_beartype.__version_info__, tuple)
