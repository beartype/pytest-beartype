"""pytest-beartype - Pytest plugin to run your tests with beartype checking enabled."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: "pytest.Parser") -> None:
    # Add beartype-specific "pytest" options exposed by this plugin.
    help_msg = (
        "comma-delimited list of the fully-qualified names of "
        "all packages and modules to type-check with beartype"
    )
    skip_help_msg = (
        "comma-delimited list of the fully-qualified names of "
        "all packages and modules to SKIP type-checking with beartype"
    )

    group = parser.getgroup("beartype")
    group.addoption("--beartype-packages", action="store", help=help_msg)
    parser.addini("beartype_packages", type="args", help=help_msg)
    group.addoption("--beartype-skip-packages", action="store", help=skip_help_msg)
    parser.addini("beartype_skip_packages", type="args", help=skip_help_msg)


def pytest_configure(config: "pytest.Config") -> None:
    # Comma-delimited string listing the fully-qualified names of *ALL* packages
    # and modules to type-check with beartype, corresponding to the
    # "beartype_packages" section in the user-defined "pytest.ini" file, or the
    # "--beartype-packages" options, defined above by the pytest_addoption() hook.
    package_names = config.getini("beartype_packages")
    package_names_arg_str = config.getoption("beartype_packages", "")
    if package_names_arg_str:
        package_names += package_names_arg_str.split(",")

    packages_to_skip = config.getini("beartype_skip_packages")
    packages_to_skip_arg_str = config.getoption("beartype_skip_packages", "")
    if packages_to_skip_arg_str:
        packages_to_skip += packages_to_skip_arg_str.split(",")

    # If `--beartype-packages` is specified (and isn't just `*`),
    # and `--beartype-skip-packages` is also specified, then bail out with an error.
    if package_names and "*" not in package_names and packages_to_skip:
        pytest.exit(
            "'beartype_packages' and 'beartype_skip_packages' cannot be used together."
        )

    # If the user passed this option...
    if package_names:
        # Defer hook-specific imports. To improve "pytest" startup performance,
        # avoid performing *ANY* imports unless the user actually passed the
        # "--beartype-packages" option declared by this plugin.
        import sys
        from warnings import warn

        from beartype import BeartypeConf
        from beartype._util.text.utiltextjoin import join_delimited
        from beartype.claw import beartype_all, beartype_packages
        from beartype.roar import BeartypeWarning

        class BeartypePytestWarning(BeartypeWarning):
            """
            Beartype :mod:`pytest` warning.

            This warning is emitted at :mod:`pytest` configuration time when one or
            more packages or modules to be type-checked have already been imported
            under the active Python interpreter.
            """

        # This (and `sys.builtin_module_names`) will be used to filter out
        # already-imported modules from the warning message (about the fact that
        # some modules have already been imported and will not be checked), whenever
        # `--beartype-packages=*` or `--beartype-skip-packages` flags are used.
        stdlib_module_names = getattr(sys, "stdlib_module_names", [])

        # Tuple of the subset of these names corresponding to previously
        # imported packages and modules under the active Python interpreter.
        if "*" in package_names:
            imported_packages = sorted(
                {module.partition(".")[0] for module in sys.modules}
            )
            beartype_imported_packages = (
                "__main__",
                "beartype",
                "_pytest",
                "iniconfig",
                "pluggy",
                "py",
                "pytest",
                "pytest_beartype",
            )
            package_imported_names = tuple(
                package
                for package in imported_packages
                if (
                    package not in beartype_imported_packages
                    and package not in sys.builtin_module_names
                    and package not in stdlib_module_names
                )
            )
        else:
            package_imported_names = tuple(
                package_name
                for package_name in package_names
                if package_name in sys.modules
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
        if "*" in package_names:
            beartype_all(
                conf=BeartypeConf(claw_skip_package_names=tuple(packages_to_skip))
            )
        else:
            beartype_packages(package_names)
