"""Test file with incorrectly typed test functions for beartype function decoration."""

import pytest


@pytest.mark.skip
def test_function_with_type_violation() -> None:
    # This does not cause beartype violation, because, ehhh, that is like impossible to check
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


# Tests that should fail:


@pytest.mark.xfail(strict=True)
def test_using_bad_fixture_correct_annotation(bad_fixture: str): ...


@pytest.mark.xfail(strict=True)
def test_using_good_fixture_wrong_annotation(good_fixture: str): ...


@pytest.mark.xfail(strict=True)
def test_using_bad_fixture_wrong_annotation(bad_fixture: tuple): ...


# Tests that should succeed:


def test_using_good_fixture_good_annotation(good_fixture: int): ...
