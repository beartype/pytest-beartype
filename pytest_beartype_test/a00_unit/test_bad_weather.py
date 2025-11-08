#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Bad weather unit tests** asserting that sample functions incorrectly annotated
by hints violating :mod:`beartype` behave as expected.
'''

# ....................{ TESTS                              }....................
def test_bad_weather_usage() -> None:
    '''
    **Bad weather unit test** asserting that sample functions incorrectly
    annotated by hints violating :mod:`beartype` behave as expected.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer test-specific imports.
    from os import environ
    from beartype.roar import BeartypeCallHintReturnViolation
    from pytest import raises
    from pytest_beartype_test.a00_unit.data.bad_weather.module import (
        sum_numbers,
        upper_string,
    )

    # ....................{ LOCALS                         }....................
    # List of integers parameter to be passed to sample functions below.
    ARG_LIST_OF_INTS = [len("The quavering thunder thereupon had ceas'd,"),]

    # Summation of all integers in this same list.
    ARG_LIST_OF_INTS_SUM = 43

    # String parameter to be passed to sample functions below.
    ARG_STR =       'His voice leapt out, despite of godlike curb,'

    # This same string upper-cased.
    ARG_STR_UPPER = 'HIS VOICE LEAPT OUT, DESPITE OF GODLIKE CURB,'

    # String value of the shell environment variable with the passed name if the
    # parent shell defines this variable *or* "None" otherwise. This variable
    # should be "None" *UNLESS* this unit test is invoked by the parent
    # test_option_beartype_packages() integration test.
    IS_BEARTYPE_PACKAGES_OPTION_PASSED = environ.get(
        'BEARTYPE_PACKAGES_OPTION_PASSED')

    # ....................{ ASSERTS                        }....................
    # If this unit test is invoked by a subprocess of the parent
    # test_option_beartype_packages() integration test...
    if IS_BEARTYPE_PACKAGES_OPTION_PASSED:
        # Assert that a function annotated by incorrect hints raises the
        # expected exception, validating that the parent
        # test_option_beartype_packages() integration test successfully applied
        # the @beartype decorator to this function via a "beartype.claw" import
        # hook registered by this pytest plugin.
        with raises(BeartypeCallHintReturnViolation):
            sum_numbers(ARG_LIST_OF_INTS)

        # Ditto.
        with raises(BeartypeCallHintReturnViolation):
            upper_string(ARG_STR)
    # Else, this unit test is invoked by this test suite as a standard test.
    else:
        # Assert that a function annotated by incorrect hints but *NOT*
        # decorated by @beartype returns the expected value (rather than raising
        # a type-checking violation).
        assert sum_numbers(ARG_LIST_OF_INTS) == ARG_LIST_OF_INTS_SUM

        # Ditto.
        assert upper_string(ARG_STR) == ARG_STR_UPPER
