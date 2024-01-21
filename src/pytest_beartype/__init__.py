"""pytest-beartype - Pytest plugin to run your tests with beartype checking enabled."""
from __future__ import annotations

import pytest


def pytest_addoption(parser: "pytest.Parser") -> None:
    # Add beartype-specific "pytest" options exposed by this plugin.
    group = parser.getgroup("beartype")
    group.addoption(
        "--beartype-packages",
        action="store",
        help=(
            "comma-delimited list of the fully-qualified names of "
            "all packages and modules to type-check with beartype"
        ),
    )


def pytest_configure(config: "pytest.Config") -> None:
    # Comma-delimited string listing the fully-qualified names of *ALL* packages
    # and modules to type-check with beartype, corresponding to the
    # "--beartype-packages" option defined above by the pytest_addoption() hook.
    package_names_str = config.getoption("beartype_packages")

    # If the user passed this option...
    if package_names_str:
        # Defer hook-specific imports. To improve "pytest" startup performance,
        # avoid performing *ANY* imports unless the user actually passed the
        # "--beartype-packages" option declared by this plugin.
        from beartype.roar import BeartypeWarning
        from beartype.claw import beartype_packages
        from beartype._util.text.utiltextjoin import join_delimited
        from sys import modules
        from warnings import warn

        class BeartypePytestWarning(BeartypeWarning):
            """
            Beartype :mod:`pytest` warning.

            This warning is emitted at :mod:`pytest` configuration time when one or
            more packages or modules to be type-checked have already been imported
            under the active Python interpreter.
            """

        # Tuple of the fully-qualified names of these packages and modules.
        package_names = tuple(
            package_name_str.strip()
            for package_name_str in package_names_str.split(",")
        )

        # Tuple of the subset of these names corresponding to previously
        # imported packages and modules under the active Python interpreter.
        package_imported_names = tuple(
            package_name for package_name in package_names if package_name in modules
        )

        # If at least one of these packages or modules has already been
        # imported...
        if package_imported_names:
            # Comma-delimited double-quoted string listing these packages. Yeah!
            package_imported_names_str = join_delimited(
                strs=package_imported_names,
                delimiter_if_two=" and ",
                delimiter_if_three_or_more_nonlast=", ",
                delimiter_if_three_or_more_last=", and ",
                is_double_quoted=True,
            )

            # Emit a non-fatal warning informing the user.
            warn(
                (
                    f"Previously imported packages "
                    f"{package_imported_names_str} not checkable by beartype."
                ),
                BeartypePytestWarning,
                stacklevel=1,  # <-- dark magic glistens dangerously
            )

        # Install an import hook type-checking these packages and modules.
        beartype_packages(package_names)
