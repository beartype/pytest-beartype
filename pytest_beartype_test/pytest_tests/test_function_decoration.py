#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test file with incorrectly typed test functions for beartype function
decoration.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ TESTS                              }....................
@pytest.mark.skip
def test_function_with_type_violation() -> None:
    # This does not cause beartype violation, because, ehhh, that is like
    # impossible to check
    #
    # Don't do that :) please...
    def helper_func(x: str) -> int:
        return x

    helper_func("test")


@pytest.fixture
def bad_fixture() -> int:
    """A fixture with incorrect return type."""
    # This returns a string but is annotated to return int
    return "not an int"  # This should trigger beartype error


@pytest.fixture
def good_fixture() -> int:
    """A fixture with correct return type."""
    return 42


@pytest.fixture
def bad_recursive_fixture_first(bad_fixture) -> str:
    return "banana"


@pytest.fixture
def bad_recursive_fixture_second(good_fixture: int) -> int:
    return "banana"


@pytest.fixture
def good_recursive_fixture(good_fixture: int) -> int:
    return good_fixture


# Tests that should fail:


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


# Tests that should succeed:


def test_deep_success(good_recursive_fixture: int): ...


def test_using_good_fixture_good_annotation(good_fixture: int): ...
