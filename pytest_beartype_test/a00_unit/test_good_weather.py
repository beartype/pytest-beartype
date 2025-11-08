#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Good weather unit tests** asserting that sample functions correctly annotated
by hints satisfying :mod:`beartype` behave as expected.
'''

# ....................{ TESTS                              }....................
def test_good_weather_usage() -> None:
    '''
    **Good weather unit test** asserting that sample functions correctly annotated by
    hints satisfying :mod:`beartype` behave as expected.
    '''

    # Defer test-specific imports.
    from pytest_beartype_test.a00_unit.data.good_weather.module import (
        helper_function,
        main,
    )

    # This should not cause any beartype violations
    result = main([1, 2, 3, 4])
    assert result == 10

    text_result = helper_function('hello')
    assert text_result == 'HELLO'
