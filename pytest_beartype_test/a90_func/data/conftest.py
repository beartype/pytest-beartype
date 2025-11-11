#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **integration test fixture data** (i.e., fixture functions to be
tested by integration tests defined elsewhere) submodule.
'''

# ....................{ TODO                               }....................
#FIXME: Define *AND* test in the "test_pytester_option_beartype_fixtures" *AND*
#"test_pytester_option_beartype_tests" submodules:
#* A synchronous generator fixture. This is a high priority, but also trivial.
#* A coroutine (asynchronous non-generator) fixture. This is non-trivial. Why?
#  Because testing this requires asynchronous test support, which then requires
#  we copy-paste from the @beartype test suite. Feasible, certainly. We must do
#  this, certainly. Yet, this takes time. Time is scarce! My face is tired.
#* An asynchronous non-generator fixture. Once coroutine support has been nailed
#  down, this suddenly becomes trivial. Yay! Something should be easy for once!

# ....................{ IMPORTS                            }....................
from pytest import fixture

# ....................{ FIXTURES ~ root                    }....................
@fixture
def fixture_hint_return_bad() -> int:
    '''
    Fixture annotated by an incorrect return type.
    '''

    # This returns a string but is annotated to return int
    return 'not an int'  # This should trigger beartype error


@fixture
def fixture_hint_return_good() -> int:
    '''
    Fixture annotated by a correct return type.
    '''

    return 42

# ....................{ FIXTURES ~ leaf                    }....................
# Leaf fixtures requiring one or more other fixtures.

@fixture
def fixture_needs_fixture_hint_return_bad(fixture_hint_return_bad) -> str:
    '''
    Fixture requiring another fixture violating a type-check, annotated by a
    correct return hint but *no* parameter hint.
    '''

    return 'From stately nave to nave, from vault to vault,'


@fixture
def fixture_hint_return_bad_needs_fixture_hint_return_good(
    fixture_hint_return_good: int) -> int:
    '''
    Fixture annotated by a bad return hint, despite requiring another fixture
    annotated by the same (and thus correct) parameter type as the return hint
    annotating that fixture.
    '''

    return 'Through bowers of fragrant and enwreathed light,'


@fixture
def fixture_hint_return_good_needs_fixture_hint_return_good(
    fixture_hint_return_good: int) -> int:
    '''
    Fixture requiring another fixture annotated by the same (and thus correct)
    parameter type as the return hint annotating that fixture.
    '''

    return fixture_hint_return_good
