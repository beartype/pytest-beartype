#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test submodule defining incorrectly typed fixture functions to be decorated by
the :func:`beartype.beartype` decorator.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ FIXTURES ~ root                    }....................
# Root fixtures requiring *NO* other fixtures.

@pytest.fixture
def bad_fixture() -> int:
    '''
    A fixture with incorrect return type.
    '''

    # This returns a string but is annotated to return int
    return 'not an int'  # This should trigger beartype error


@pytest.fixture
def good_fixture() -> int:
    '''
    A fixture with correct return type.
    '''

    return 42

# ....................{ FIXTURES ~ stem                    }....................
# Stem fixtures requiring one or more other fixtures.

@pytest.fixture
def bad_recursive_fixture_first(bad_fixture) -> str:
    return 'banana'


@pytest.fixture
def bad_recursive_fixture_second(good_fixture: int) -> int:
    return 'banana'


@pytest.fixture
def good_recursive_fixture(good_fixture: int) -> int:
    return good_fixture

# ....................{ TESTS ~ pass                       }....................
# Unit tests expected to succeed.

def test_deep_success(good_recursive_fixture: int): ...
def test_using_good_fixture_good_annotation(good_fixture: int): ...

# ....................{ TESTS ~ fail                       }....................
# Unit tests expected to fail.

@pytest.mark.xfail(strict=True)
def test_using_bad_fixture_correct_annotation(bad_fixture: str): ...

@pytest.mark.xfail(strict=True)
def test_using_good_fixture_wrong_annotation(good_fixture: str): ...

@pytest.mark.xfail(strict=True)
def test_using_bad_fixture_wrong_annotation(bad_fixture: tuple): ...

@pytest.mark.xfail(strict=True)
def test_deep_fail_first(bad_recursive_fixture_first: str): ...

@pytest.mark.xfail(strict=True)
def test_deep_fail_second(bad_recursive_fixture_second: str): ...
