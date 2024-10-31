from unittest import mock

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
