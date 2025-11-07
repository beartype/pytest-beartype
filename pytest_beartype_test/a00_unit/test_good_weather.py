#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test file that imports and uses the good weather package correctly.
'''

# ....................{ TESTS                              }....................
def test_good_weather_usage() -> None:

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
