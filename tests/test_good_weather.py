"""Test file that imports and uses the good weather package correctly."""

from good_weather_package.module import main, helper_function


def test_good_weather_usage() -> None:
    # This should not cause any beartype violations
    result = main([1, 2, 3, 4])
    assert result == 10

    text_result = helper_function("hello")
    assert text_result == "HELLO"
