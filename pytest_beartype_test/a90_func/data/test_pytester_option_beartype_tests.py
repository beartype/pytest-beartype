#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **test integration test** (i.e., integration tests testing that this
plugin passed the ``--beartype-tests`` option correctly type-checks tests)
submodule.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ TESTS                              }....................
@pytest.mark.xfail(strict=True)
def test_function_with_type_violation() -> None:
    '''
    Test annotated by an incorrect return hint.
    '''

    def helper_func(x: str) -> int:
        '''
        Closure intentionally annotated by an incorrect return hint.

        Currently, this plugin does *not* type-check closures embedded in tests.
        Doing so should be feasible, but is left as an exercise to the reader.
        '''

        return x


    # Call and return the value returned by the above closure.
    return helper_func('test')

# ....................{ TESTS ~ fixture                    }....................
@pytest.mark.xfail(strict=True)
def test_arg_bad_fixture_hint_return_good(
    fixture_hint_return_good: str) -> None:
    '''
    Test requiring a fixture annotated by a different (and thus incorrect)
    parameter hint from the return hint annotating that fixture.
    '''

    pass
