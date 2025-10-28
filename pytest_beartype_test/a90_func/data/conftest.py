#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **integration test fixture data** (i.e., fixture functions to be
tested by integration tests defined elsewhere) submodule.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ FIXTURES ~ root                    }....................
@pytest.fixture
def fixture_hint_return_bad() -> int:
    '''
    Fixture annotated by an incorrect return type.
    '''

    # This returns a string but is annotated to return int
    return 'not an int'  # This should trigger beartype error


@pytest.fixture
def fixture_hint_return_good() -> int:
    '''
    Fixture annotated by a correct return type.
    '''

    return 42

# ....................{ FIXTURES ~ leaf                    }....................
# Leaf fixtures requiring one or more other fixtures.

@pytest.fixture
def fixture_needs_fixture_hint_return_bad(fixture_hint_return_bad) -> str:
    '''
    Fixture requiring another fixture annotated by an incorrect return hint.
    '''

    return 'From stately nave to nave, from vault to vault,'


@pytest.fixture
def fixture_hint_return_bad_needs_fixture_hint_return_good(
    fixture_hint_return_good: int) -> int:
    '''
    Fixture annotated by a bad return hint, despite requiring another fixture
    annotated by the same (and thus correct) parameter type as the return hint
    annotating that fixture.
    '''

    return 'Through bowers of fragrant and enwreathed light,'


@pytest.fixture
def fixture_hint_return_good_needs_fixture_hint_return_good(
    fixture_hint_return_good: int) -> int:
    '''
    Fixture requiring another fixture annotated by the same (and thus correct)
    parameter type as the return hint annotating that fixture.
    '''

    return fixture_hint_return_good
