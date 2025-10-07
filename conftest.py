from pathlib import Path
import pytest

pytest_plugins = "pytester"


@pytest.fixture(scope="session")
def beartype_pytest_tests() -> list[Path]:
    """Discover all test files under pytest_tests directory."""
    return list(Path("tests/pytest_tests").rglob("*.py"))
