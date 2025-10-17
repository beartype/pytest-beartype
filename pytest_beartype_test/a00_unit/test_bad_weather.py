#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test file that imports and uses the bad weather package with type violations.
'''

# ....................{ TESTS                              }....................
def test_bad_weather_usage() -> None:

    # Defer test-specific imports.
    from pytest_beartype_test.a00_unit.data.bad_weather.module import (
        helper_function,
        main,
    )

    # This should cause beartype violations when beartype is enabled
    # The return type was annotated incorrectly as "str"
    result = main([1, 2, 3, 4])
    assert result == 10

    # Same here, the return type was annotated as "int"
    text_result = helper_function('hello')
    assert text_result == 'HELLO'
