from pathlib import Path
import pytest
import sys

# We prohibit generation of the bytecode because the pytester
# copies the files under /tmp and if /tmp and /home are on different
# devices, or, possibly, different architectures Python starts to spew out
# tons of warnings/errors about bytecode inconsistency, because it still fetches
# the old bytecode while executing the /tmp copy of the codebase
sys.dont_write_bytecode = True

pytest_plugins = "pytester"


@pytest.fixture(scope="session")
def beartype_pytest_tests() -> list[Path]:
    """Discover all test files under pytest_tests directory."""
    return list(Path("tests/pytest_tests").rglob("*.py"))
