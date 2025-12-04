#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin-specific **test type-checking** (i.e., :mod:`pytest` hook functions
generalizing the runtime behaviour of :mod:`pytest` to type-check collected
user-defined :mod:`pytest` tests with :mod:`beartype`).
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAUTION: Avoid importing from *ANY* packages at global scope to improve pytest
# startup performance. The sole exception is the "pytest" package itself. Since
# pytest has presumably already imported and run this plugin, the "pytest"
# package has presumably already been imported. Ergo, importing from that
# package yet again incurs no further costs.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import pytest

# ....................{ HOOKS ~ tests                      }....................
def pytest_collection_modifyitems(
    config: 'pytest.Config', items: list['pytest.Item']) -> None:
    '''
    Conditionally decorate *all* collected test functions by the
    :func:`beartype.beartype` decorator if instructed to do so by the user
    (e.g., if passed the ``--beartype-tests`` command-line option).
    '''

    # Defer hook-specific imports.
    from pytest_beartype._util.utilopt import is_pytest_option_bool

    # If *NOT* instructed by the user to type-check tests, reduce to a noop.
    if not is_pytest_option_bool(config=config, option_name='beartype_tests'):
        return
    # Else, the user instructed this plugin to type-check tests.

    # Defer beartype-specific imports as late as feasible to minimize all
    # startup costs associated with this plugin.
    from beartype import beartype

    # For each collected user-defined test function...
    for item in items:
        if isinstance(item, pytest.Function):
            # Type-check this test function with beartype.
            item.obj = beartype(item.obj)
