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

    mock_addoption.assert_called_once_with(
        "--beartype-packages",
        action="store",
        help=mock.ANY,
    )
