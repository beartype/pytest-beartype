from unittest import mock
import subprocess
import sys

import pytest
import pytest_beartype


def test_pytest_addoption() -> None:
    """
    Assert that the "pytest_addoption" hook declared by this plugin adds the
    "--beartype-packages" option to the "beartype" group.
    """
    with mock.patch.object(pytest.OptionGroup, "addoption") as mock_addoption:
        pytest_beartype.pytest_addoption(pytest.Parser())

    assert mock_addoption.call_count == 2
    mock_addoption.assert_has_calls(
        [
            mock.call(
                "--beartype-packages",
                action="store",
                help=mock.ANY,
            ),
            mock.call(
                "--beartype-skip-packages",
                action="store",
                help=mock.ANY,
            ),
        ]
    )


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
