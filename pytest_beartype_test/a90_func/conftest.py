#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Test subpackage configuration** (i.e., :mod:`pytest`-specific configuration
guaranteed to be implicitly imported by :mod:`pytest` into *all* sibling and
child submodules of the test subpackage containing this :mod:`pytest` plugin).
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ FIXTURES                           }....................
@pytest.fixture(scope='session')
def path_test_pytester_option_beartype_fixtures() -> 'pathlib.Path':
    '''
    Session-scoped fixture providing the **path** (i.e., :class:`pathlib.Path`
    objects) of the
    ``pytest_beartype_test.a90_func.data.test_pytester_option_beartype_fixtures``
    submodule.

    Note that the standard ``pytester`` plugin implicitly conflicts with the
    test filename inspection performed by this fixture, due to that plugin
    copying test paths to a temporary directory (typically, ``/tmp/``). This
    test filename inspection is thus intentionally performed at an earlier time
    as the body of this fixture.
    '''

    # Defer fixture-specific imports.
    from pathlib import Path

    # Return this list by globbing these paths with shell-like syntax.
    return Path('pytest_beartype_test/a90_func/data/test_pytester_option_beartype_fixtures.py')


@pytest.fixture(scope='session')
def path_test_pytester_option_beartype_tests() -> 'pathlib.Path':
    '''
    Session-scoped fixture providing the **path** (i.e., :class:`pathlib.Path`
    objects) of the
    ``pytest_beartype_test.a90_func.data.test_pytester_option_beartype_tests``
    submodule.

    See Also
    --------
    :func:`.path_test_pytester_option_beartype_tests`
        Further details.
    '''

    # Defer fixture-specific imports.
    from pathlib import Path

    # Return this list by globbing these paths with shell-like syntax.
    return Path('pytest_beartype_test/a90_func/data/test_pytester_option_beartype_tests.py')
