import subprocess
import sys

#FIXME: Tests defined by this submodule succeed under the "tox" command but fail
#under the "pytest" command, presumably because the former ensures that this
#package is installed as a valid "pytest" plugin whereas the latter does not.
#Consider skipping these tests if 


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


def test_pytest(pytester, beartype_pytest_tests):
    """Test that specific test functions fail when beartype checking is enabled (default behavior)."""
    for test_file in beartype_pytest_tests:
        pytester.copy_example(str(test_file))

    result = pytester.runpytest()

    desc = """ This means that fixture/function beartype checking inside pytest
    does not work correctly.
    """

    # Parse the outcomes
    outcomes = result.parseoutcomes()

    # Note that "xfailed" in the outcomes is fine: it can be interpreted as
    # "the test failed as expected" -> so all is good
    assert "failed" not in outcomes, (
        "Something failed when testing pytest while running pytest inside of pytest... test-ception?"
        + desc
    )
    assert "error" not in outcomes, (
        "Oh-oh, internal pytest error in the plugin - "
        "something pretty bad happened, maybe new pytest version?" + desc
    )
