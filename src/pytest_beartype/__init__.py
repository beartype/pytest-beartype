"""pytest-beartype - Pytest plugin to run your tests with beartype checking enabled."""

import pytest
from typing import Any
from warnings import warn


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
    functions_help_msg = (
        "disable beartype type-checking on test functions and fixtures themselves"
    )

    group = parser.getgroup("beartype")
    group.addoption("--beartype-packages", action="store", help=help_msg)
    parser.addini("beartype_packages", type="args", help=help_msg)
    group.addoption("--beartype-skip-packages", action="store", help=skip_help_msg)
    parser.addini("beartype_skip_packages", type="args", help=skip_help_msg)
    group.addoption(
        "--beartype-ignore-tests", action="store_true", help=functions_help_msg
    )
    parser.addini("beartype_ignore_tests", type="bool", help=functions_help_msg)


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


def _is_pytest_config_beartype_check_tests(config: "pytest.Config") -> bool:
    """Check if beartype test checking is enabled via config or command line."""
    # Tests are checked by default unless --beartype-ignore-tests is passed
    return not (
        config.getini("beartype_ignore_tests")
        or config.getoption("beartype_ignore_tests", False)
    )


def pytest_collection_modifyitems(
    config: "pytest.Config", items: list["pytest.Item"]
) -> None:
    """
    Apply the beartype decorator to all collected test functions unless --beartype-ignore-tests is passed.
    """
    if not _is_pytest_config_beartype_check_tests(config):
        return

    # Import beartype only when needed to avoid performance impact
    from beartype import beartype

    # Apply beartype decorator to all collected test functions
    for item in items:
        if isinstance(item, pytest.Function):
            # Wrap the test function with beartype
            item.obj = beartype(item.obj)


class _BeartypeFixtureFailure:
    """Sentinel class to mark that a fixture failed due to beartype violation."""

    def __init__(self, fixture_name: str, error: Exception):
        self.fixture_name = fixture_name
        self.error = error


def pytest_fixture_setup(
    fixturedef: "pytest.FixtureDef[Any]", request: "pytest.FixtureRequest"
) -> None:
    """
    Apply beartype decoration to fixtures unless --beartype-ignore-tests is passed.

    This is called before fixture setup execution.

    The idea for fixtures is quite simple: we replace the fixtures with our sentinel if we
    detect them failing, so that later we can intercept it. The main reason for doing so,
    instead of just wrapping the thing into beartype() is such that we don't fail _inside_
    of the pytest (which produces unreadable error logs), but so that we can fail outside
    of the pytest internals, leading to a decent error log and the test classified as "fail"
    instead of "error" (which usually indicates an internal pytest error, which is wrong
    in this case).
    """
    if not _is_pytest_config_beartype_check_tests(request.config):
        return

    # Import beartype and inspect only when needed
    from beartype import beartype
    from beartype.roar import BeartypeException
    import inspect
    import functools

    # Only decorate fixtures that haven't been decorated yet
    if hasattr(fixturedef, "_beartype_decorated"):
        return

    # Skip generator functions for now due to beartype/beartype#423
    # TODO: force tiny cub @knyazer or Bear God @leycec to fix this when something is done with it
    # This also should not really happen, like ever, since I don't understand what it means.
    if inspect.isgeneratorfunction(fixturedef.func):
        # The monkeypatch check is wonderful: monkeypatch is an internal pytest fixture that is,
        # in fact, a generator. Wow. We don't want to emit warnings all the time, so we just ignore it.
        if fixturedef.argname != "monkeypatch":
            warn(
                f"Generator fixture '{fixturedef.argname}' skipped for beartype checking "
                "due to known limitation (see https://github.com/beartype/beartype/issues/423). "
                "Please check that the PR is still open, and if it's not you should call "
                "upon the Bear God @leycec to rescue you.",
                UserWarning,
                stacklevel=1,
            )
        return

    original_func = fixturedef.func
    try:
        # Apply beartype decoration here at fixture definition time.
        beartype_decorated = beartype(original_func)

        # Create a wrapper that catches beartype errors
        @functools.wraps(original_func)
        def beartype_fixture_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return beartype_decorated(*args, **kwargs)
            except BeartypeException as e:
                # Return sentinel object instead of raising
                return _BeartypeFixtureFailure(fixturedef.argname, e)
    except BeartypeException as e:
        # Create a wrapper that returns a sentinel object encapsulating this
        # early @beartype decorator-time exception.
        @functools.wraps(original_func)
        def beartype_fixture_wrapper(*args: Any, **kwargs: Any) -> Any:
            # Return sentinel object instead of raising
            return _BeartypeFixtureFailure(fixturedef.argname, e)

    # Replace the fixture function with our wrapper
    fixturedef.func = beartype_fixture_wrapper  # type: ignore[misc]
    # Mark as decorated to avoid double decoration
    fixturedef._beartype_decorated = True  # type: ignore[attr-defined]


def pytest_pyfunc_call(pyfuncitem: "pytest.Function") -> bool | None:
    """
    Intercept test function calls to check for beartype fixture failures.

    This hook runs during the actual test execution, allowing us to fail
    the test (not the setup) when beartype fixture violations are detected.
    """
    if not _is_pytest_config_beartype_check_tests(pyfuncitem.config):
        return None

    # Check all fixture values for beartype failures before calling the test
    for argname in pyfuncitem.fixturenames:
        fixture_value = pyfuncitem._request.getfixturevalue(argname)
        if isinstance(fixture_value, _BeartypeFixtureFailure):
            # Include traceback in the error message for better debugging
            import traceback

            tb_str = ""
            if hasattr(fixture_value.error, "__traceback__"):
                tb_lines = traceback.format_tb(fixture_value.error.__traceback__)
                tb_str = "\r\n" + "".join(tb_lines)
            pytest.fail(
                f"Fixture '{fixture_value.fixture_name}' failed beartype validation: {fixture_value.error}{tb_str}",
                pytrace=False,
            )

    # Return None to let pytest call the function normally
    return None
