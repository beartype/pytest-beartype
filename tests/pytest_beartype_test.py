from unittest import mock
import subprocess
import sys

import pytest
import pytest_beartype


def test_good_weather_no_beartype_violations() -> None:
    """Test that pytest runs successfully when there are no beartype violations."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--beartype-packages=good_weather_package",
            "-v",
            "--tb=short",
            "-c",
            "/dev/null",
            "--override-ini",
            "python_files=test_good_weather.py",
            "tests/test_good_weather.py",
        ],
        cwd=".",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"pytest failed with output: {result.stdout}\n{result.stderr}"
    )


def test_bad_weather_with_beartype_violations() -> None:
    """Test that pytest fails when there are beartype violations."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--beartype-packages=bad_weather_package",
            "-v",
            "--tb=short",
            "-c",
            "/dev/null",
            "--override-ini",
            "python_files=test_bad_weather.py",
            "tests/test_bad_weather.py",
        ],
        cwd=".",
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, (
        f"pytest should have failed but passed: {result.stdout}\n{result.stderr}"
    )


def test_pytest(pytester):
    """Test that specific test functions fail when beartype-check-tests option is used."""
    # TODO: automatically discover al the files under pytest_tests and copy them
    # we cannot really do that easily because pytester overrides everything
    # so we can't use e.g. Path.rglob :(
    pytester.copy_example("tests/pytest_tests/test_function_decoration.py")

    result = pytester.runpytest("--beartype-check-tests")

    desc = """ This means that fixture/function beartype checking inside pytest
    with --beartype-check-tests does not work correctly.
    """

    # Parse the outcomes
    outcomes = result.parseoutcomes()

    assert "failed" not in outcomes, (
        "Something failed when testing pytest while running pytest inside of pytest... test-ception?"
        + desc
    )
    assert "error" not in outcomes, (
        "Oh-oh, internal pytest error in the plugin - "
        "something pretty bad happened, maybe new pytest veresion?" + desc
    )
