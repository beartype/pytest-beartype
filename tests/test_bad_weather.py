# type: ignore
"""Test file that imports and uses the bad weather package with type violations."""

from bad_weather_package.module import main, helper_function


def test_bad_weather_usage() -> None:
    # This should cause beartype violations when beartype is enabled
    # The return type was annotated incorrectly as "str"
    result = main([1, 2, 3, 4])
    assert result == 10

    # Same here, the return type was annotated as "int"
    text_result = helper_function("hello")
    assert text_result == "HELLO"
