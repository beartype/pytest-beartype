#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **test integration test** (i.e., integration tests testing that this
plugin passed the ``--beartype-tests`` option correctly type-checks tests)
submodule.

This submodule is *not* intended to be directly collected by the root
:mod:`pytest` process. This submodule is *only* collected by the leaf
:mod:`pytest` subprocess implicitly spawned by the :mod:`pytest.pytester`
fixture required by the parent ``test_pytester_option_beartype_tests`` test.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ TESTS                              }....................
def test_pytester_option_beartype_tests_sync() -> str:
    '''
    Synchronous test annotated by a correct return hint.
    '''

    # Return an object satisfying the return hint annotating this test.
    return 'O spectres busy in a cold, cold gloom!'


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_tests_sync_bad() -> None:
    '''
    Synchronous test annotated by an incorrect return hint.
    '''

    def to_this_result(o_dreams_of_day_and_night: str) -> int:
        '''
        Synchronous closure intentionally annotated by an incorrect return hint.

        Currently, this plugin does *not* type-check closures embedded in tests.
        Doing so should be feasible, but is left as an exercise to the reader.
        '''

        return o_dreams_of_day_and_night


    # Return an object violating the return hint annotating this test by
    # returning the value returned by calling the above closure.
    return to_this_result('To this result: "O dreams of day and night!"')

# ....................{ TESTS ~ fixture : sync : non-gener }....................
def test_pytester_option_beartype_tests_sync_needs_fixtures_sync_nongenerator(
    fixture_sync_nongenerator: str,
    fixture_sync_nongenerator_needs_fixture: str,
) -> None:
    '''
    Synchronous test requiring one or more synchronous non-generator fixtures
    annotated by the same parameter hints as the return hints annotating those
    fixtures.
    '''

    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_tests_sync_bad_needs_fixtures_sync_nongenerator(
    # Parent fixture that is correctly annotated.
    fixture_sync_nongenerator: str,

    # Parent fixture that is intentionally incorrectly annotated.
    fixture_sync_nongenerator_needs_fixture: int,
) -> None:
    '''
    Synchronous test requiring one or more synchronous non-generator fixtures
    annotated by different parameter hints from the return hints annotating
    those fixtures.
    '''

    pass

# ....................{ TESTS ~ fixture : sync : generator }....................
def test_pytester_option_beartype_tests_sync_needs_fixtures_sync_generator(
    fixture_sync_generator: str,
    fixture_sync_generator_needs_fixture: str,
) -> None:
    '''
    Synchronous test requiring one or more synchronous generator fixtures
    annotated by the same parameter hints as the return hints annotating those
    fixtures.
    '''

    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_tests_sync_bad_needs_fixtures_sync_generator(
    # Parent fixture that is correctly annotated.
    fixture_sync_generator: str,

    # Parent fixture that is intentionally incorrectly annotated.
    fixture_sync_generator_needs_fixture: int,
) -> None:
    '''
    Synchronous test requiring one or more synchronous generator fixtures
    annotated by different parameter hints from the return hints annotating
    those fixtures.
    '''

    pass
