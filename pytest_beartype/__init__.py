#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
`pytest-beartype`.

`pytest` plugin type-checking fixtures, tests, and tested code with beartype.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAUTION: Avoid importing from *ANY* packages at global scope to improve pytest
# startup performance. The sole exception is the "pytest" package itself. Since
# pytest has presumably already imported and run this plugin, the "pytest"
# package has presumably already been imported. Ergo, importing from that
# package yet again incurs no further costs.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import pytest

# ....................{ GLOBALS                            }....................
__version__ = '0.3.0'
'''
Human-readable package version as a ``.``-delimited string.

For :pep:`8` compliance, this specifier has the canonical name ``__version__``
rather than that of a typical global (e.g., ``VERSION_STR``).

Note that this is the canonical version specifier for this package. Indeed, the
top-level ``pyproject.toml`` file dynamically derives its own ``version`` string
from this string global.

See Also
--------
pyproject.toml
   The Hatch-specific ``[tool.hatch.version]`` subsection of the top-level
   ``pyproject.toml`` file, which parses its version from this string global.
'''

# ....................{ HOOKS ~ option                     }....................
def pytest_addoption(parser: "pytest.Parser") -> None:
    '''
    Hook programmatically adding new plugin-specific options to both the
    `pytest` command-line interface (CLI) *and* top-level configuration files
    (e.g., `"pyproject.toml"`, `"pytest.ini"`).
    '''

    # ....................{ CONSTANTS                      }....................
    # Human-readable messages documenting plugin-specific options added below.
    HELP_MSG = (
        'comma-delimited list of the fully-qualified names of '
        'all packages and modules to type-check with beartype'
    )
    SKIP_HELP_MSG = (
        'comma-delimited list of the fully-qualified names of '
        'all packages and modules to SKIP type-checking with beartype'
    )
    FUNCTIONS_HELP_MSG = (
        'disable beartype type-checking on '
        'test functions and fixtures themselves'
    )

    # ....................{ OPTIONS                        }....................
    # Add one pair of CLI and file options for each configuration setting
    # exposed by this plugin.

    # Plugin-specific group of options.
    group = parser.getgroup('beartype')

    # Plugin option registering one or more beartype.claw.beartype_packages()
    # import hooks.
    group.addoption('--beartype-packages', action='store', help=HELP_MSG)
    parser.addini('beartype_packages', type='args', help=HELP_MSG)

    # Plugin option configuring the
    # "beartype.BeartypeConf.claw_skip_package_names" option.
    group.addoption(
        '--beartype-skip-packages', action='store', help=SKIP_HELP_MSG)
    parser.addini('beartype_skip_packages', type='args', help=SKIP_HELP_MSG)

    # Plugin option disabling type-checking of pytest tests and fixtures.
    group.addoption(
        '--beartype-ignore-tests', action='store_true', help=FUNCTIONS_HELP_MSG)
    parser.addini('beartype_ignore_tests', type='bool', help=FUNCTIONS_HELP_MSG)


def pytest_configure(config: 'pytest.Config') -> None:
    '''
    Hook programmatically handling new plugin-specific options previously added
    by the :func:`.pytest_addoption` hook.

    Parameters
    ----------
    config : pytest.Config
        **Pytest configuration** (i.e., object encapsulating all user-defined
        pytest options both passed at the command line *and* set in the
        the ``pyproject.toml`` and/or ``pytest.ini`` files.
    '''
    # print('In pytest_configure()...')

    # Comma-delimited string listing the fully-qualified names of *ALL* packages
    # and modules to be type-checked by beartype, corresponding to either:
    # * The "--beartype-packages" option passed to the "pytest" command.
    # * The "beartype_packages" option in user-defined "pyproject.toml" and
    #   "pytest.ini" files.
    #
    # See the pytest_addoption() hook defined above.
    package_names = _get_pytest_option_list(
        config=config,
        option_name_cli='beartype_packages',
        option_name_conf='beartype_packages',
    )

    # If the user passed this option...
    if package_names:
        # Comma-delimited string listing the fully-qualified names of *ALL*
        # packages and modules to *NOT* be type-checked by beartype,
        # corresponding to either:
        # * The "--beartype-skip-packages" option passed to the "pytest"
        #   command.
        # * The "beartype_skip_packages" option in user-defined "pyproject.toml"
        #   and "pytest.ini" files.
        #
        # See the pytest_addoption() hook defined above.
        skip_package_names = _get_pytest_option_list(
            config=config,
            option_name_cli='beartype_skip_packages',
            option_name_conf='beartype_packages',
        )

        # Register a new "beartype.claw" import hook automatically type-checking
        # these packages and modules (excluding these packages and modules to be
        # skipped) subsequently imported during pytest test execution.
        _beartype_packages(
            package_names=package_names, skip_package_names=skip_package_names)


def pytest_collection_modifyitems(
    config: 'pytest.Config', items: list['pytest.Item']) -> None:
    '''
    Apply the beartype decorator to all collected test functions unless
    the ``--beartype-ignore-tests`` option is passed.
    '''

    if not _is_pytest_config_beartype_check_tests(config):
        return

    # Import beartype only when needed to avoid performance impact
    from beartype import beartype

    # Apply beartype decorator to all collected test functions
    for item in items:
        if isinstance(item, pytest.Function):
            # Wrap the test function with beartype
            item.obj = beartype(item.obj)


def pytest_fixture_setup(
    fixturedef: 'pytest.FixtureDef[object]',
    request: 'pytest.FixtureRequest',
) -> None:
    '''
    Apply beartype decoration to fixtures unless the ``--beartype-ignore-tests``
    option is passed.

    Pytest calls this plugin hook *before* fixture setup execution.

    The idea for type-checking fixtures is quite simple: we replace the fixtures
    with our sentinel if we detect them failing, so that later we can intercept
    it. The main reason for doing so, instead of just wrapping the thing into
    :func:`beartype.beartype` is such that we don't fail *inside* of pytest
    internals (which produces unreadable error logs), but so that we can fail
    outside of pytest internals, leading to a decent error log and the test
    classified as "fail" instead of "error" (which usually indicates an internal
    pytest error, which is wrong in this case).
    '''
    if (
        not _is_pytest_config_beartype_check_tests(request.config) or
        hasattr(fixturedef, '_beartype_decorated')
    ):
        return

    # Import beartype and inspect only when needed
    from beartype import beartype
    from beartype.roar import BeartypeException
    from functools import wraps
    from inspect import isgeneratorfunction

    # Low-level pure-Python function implementing this high-level fixture.
    fixture_func = fixturedef.func

    # Skip generator functions for now. See also:
    #     https://github.com/beartype/beartype/issues/423
    # TODO: force tiny cub @knyazer or Bear God @leycec to fix this when something is done with it
    # This also should not really happen, like ever, since I don't understand what it means.

    #FIXME: Comment us up, please. *sigh*
    if isgeneratorfunction(fixturedef.func):
        #FIXME: Should work, but doesn't. No idea. Let's just noop out for the
        #moment, huh?
        # @wraps(fixture_func)
        # def _beartype_fixture_generator(*args, **kwargs):
        #     yield from fixture_func(*args, **kwargs)
        #
        # fixture_func = _beartype_fixture_generator

        #FIXME: Even emitting non-fatal warnings is dangerous here. Why? Because
        #pytest test suites are commonly configured to treat non-fatal warnings
        #emitted by tests as test failures. If those test suites then contain
        #one or more generator functions, then this plugin erroneously blows up
        #the entire test suite. Silence is preferable, sadly.
        # # The monkeypatch check is wonderful: monkeypatch is an internal pytest fixture that is,
        # # in fact, a generator. Wow. We don't want to emit warnings all the time, so we just ignore it.
        # if fixturedef.argname != "monkeypatch":
        #     # Defer heavyweight imports to optimize pytest startup.
        #     from warnings import warn
        #
        #     warn(
        #         f'Generator fixture '{fixturedef.argname}' skipped for beartype checking '
        #         'due to known limitation (see https://github.com/beartype/beartype/issues/423). '
        #         'Please check that the PR is still open, and if it's not you should call '
        #         'upon the Bear God @leycec to rescue you.',
        #         UserWarning,
        #         stacklevel=1,
        #     )

        # Preserve this fixture as is and silently reduce to a noop.
        return

    try:
        # Apply beartype decoration here at fixture definition time.
        beartype_decorated = beartype(fixture_func)

        # Create a wrapper that catches beartype errors
        @wraps(fixture_func)
        def _beartype_fixture_wrapper(*args, **kwargs):
            try:
                return beartype_decorated(*args, **kwargs)
            except BeartypeException as exception:
                # Return sentinel object instead of raising
                return _BeartypeFixtureFailure(fixturedef.argname, exception)
    except BeartypeException as exception:
        # Create a wrapper that returns a sentinel object encapsulating this
        # early @beartype decorator-time exception.
        #
        # Note that this exception is intentionally passed as a hidden optional
        # "__beartype_exception__" parameter to this fixture wrapper. Why?
        # Because if we *DON'T* do that, then CPython complains about that the
        # "exception" attribute is inaccessible to the body of this closure.
        # Why? No idea. Closure mechanics frighten me, honestly:
        #     NameError: cannot access free variable 'exception' where it is not
        #     associated with a value in enclosing scope
        @wraps(fixture_func)
        def _beartype_fixture_wrapper(*args, exception=exception, **kwargs):
            # Return sentinel object instead of raising
            return _BeartypeFixtureFailure(fixturedef.argname, exception)

    # Replace the fixture function with our wrapper
    fixturedef.func = _beartype_fixture_wrapper  # type: ignore[misc]
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
            # Defer global imports to improve "pytest" startup performance.
            from traceback import format_tb

            failure_message_traceback = ''
            failure_traceback = getattr(
                fixture_value.fixture_exception, '__traceback__', None)

            # Include traceback in the error message for better debugging
            if failure_traceback:
                failure_traceback_formatted = format_tb(failure_traceback)
                failure_message_traceback = (
                    f'\n{"".join(failure_traceback_formatted)}')

            failure_message = (
                f'Fixture "{fixture_value.fixture_name}" failed '
                f'beartype validation: '
                f'{fixture_value.fixture_exception}'
                f'{failure_message_traceback}'
            )

            pytest.fail(failure_message, pytrace=False)

    # Return None to let pytest call the function normally
    return None

# ....................{ PRIVATE ~ globals                  }....................
_PACKAGE_NAMES_IGNORABLE = frozenset((
    '__main__',
    'beartype',
    '_pytest',
    'iniconfig',
    'pluggy',
    'py',
    'pytest',
    'pytest_beartype',
    'sys',
    'typing',
    'warnings',
))
'''
Frozen set of the names of all **ignorable packages** (i.e., packages to be
ignored by the :func:`beartype.claw.beartype_all` import hook invoked by a user
passing the ``--beartype-packages='*'`` command-line option).
'''

# ....................{ PRIVATE ~ classes                  }....................
class _BeartypeFixtureFailure(object):
    '''
    **Fixture failure** (i.e., sentinel class marking how, why, when, and where
    a fixture violated beartype-based type-checking).
    '''

    def __init__(self, fixture_name: str, fixture_exception: Exception) -> None:
        '''
        Initialize this fixture failure.

        Parameters
        ----------
        fixture_name : str
            Fully-qualified name of the fixture that failed.
        fixture_exception : Exception
            Exception raised by beartype-based type-checking of this fixture.
        '''

        # Classify all passed parameters.
        self.fixture_name = fixture_name
        self.fixture_exception = fixture_exception

# ....................{ PRIVATE ~ testers                  }....................
def _is_pytest_config_beartype_check_tests(config: 'pytest.Config') -> bool:
    '''
    Check if beartype test checking is enabled via config or command line.
    '''

    # Tests are checked by default unless --beartype-ignore-tests is passed
    return not (
        config.getini('beartype_ignore_tests') or
        config.getoption('beartype_ignore_tests', False)
    )

# ....................{ PRIVATE ~ getters                  }....................
def _get_pytest_option_list(
    config: 'pytest.Config',
    option_name_cli: str,
    option_name_conf: str,
) -> list[str]:
    '''
    List of one or more substrings corresponding to the concatenation of both:

    * The comma-delimited substrings passed by the user as the command-line
      option with the passed name.
    * The TOML- or INI-formatted substrings configured by the user for the
      option with the passed name in the user-defined ``pyproject.toml`` and/or
      ``pytest.ini`` files.

    Parameters
    ----------
    config : pytest.Config
        **Pytest configuration** (i.e., object encapsulating all user-defined
        pytest options both passed at the command line *and* set in the
        the ``pyproject.toml`` and/or ``pytest.ini`` files.
    option_name_cli : str
        Name of the command-line option unique to this plugin previously added
        by the :func:`.pytest_addoption` hook.
    option_name_conf : str
        Name of the configuration option unique to this plugin previously added
        by the :func:`.pytest_addoption` hook.
    '''
    assert isinstance(option_name_cli, str), (
        f'{repr(option_name_cli)} not string.')
    assert isinstance(option_name_conf, str), (
        f'{repr(option_name_conf)} not string.')

    # List of the one or more TOML- or INI-formatted substrings configured by
    # the user for the option with this name in the user-defined
    # "pyproject.toml" and/or "pytest.ini" files.
    option_list = config.getini(option_name_conf)

    # String list of the one or more comma-delimited substrings passed by the
    # user as the command-line option with this name.
    option_list_str = config.getoption(option_name_cli, '')

    # If the user passed this command-line option, extend this list by the list
    # of comma-delimited substrings passed as this option.
    if option_list_str:
        option_list.extend(option_list_str.split(','))
    # Else, the user did *NOT* pass this command-line option.

    # Return this list.
    return option_list

# ....................{ PRIVATE ~ import hooks             }....................
def _beartype_packages(
    package_names: list[str], skip_package_names: list[str]) -> None:
    '''
    Register a new :mod:`beartype.claw` import hook automatically type-checking
    *all* of the packages and modules with the passed names (excluding *all* of
    the skipped packages and modules with the passed names) subsequently
    imported during :mod:`pytest` test execution with :func:`beartype.beartype`.

    Parameters
    ----------
    package_names : list[str]
        Comma-delimited string listing the fully-qualified names of *all*
        packages and modules to be type-checked, corresponding to
        either:

        * The ``--beartype-packages`` option passed to the ``pytest`` command.
        * The ``beartype_packages`` option in user-defined ``pyproject.toml``
          and ``pytest.ini`` files.
    skip_package_names : list[str]
        Comma-delimited string listing the fully-qualified names of *all*
        packages and modules to *not* be type-checked by beartype,
        corresponding to either:

        * The ``--beartype-skip-packages`` option passed to the ``pytest``
          command.
        * The ``beartype_skip_packages`` option in user-defined ``pyproject.toml``
          and ``pytest.ini`` files.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer global imports to improve "pytest" startup performance.
    from beartype import BeartypeConf
    from beartype._util.text.utiltextjoin import join_delimited
    from beartype.claw import beartype_all, beartype_packages
    from beartype.roar import BeartypeWarning

    # Standard lists of module names, used to filter out already-imported
    # modules from the warning message (about the fact that some modules have
    # already been imported and will not be checked) if the user passes one or
    # both of the "--beartype-packages='*'" or "--beartype-skip-packages=..."
    # command-line options.
    from sys import (
        builtin_module_names as module_names_builtin,
        modules              as module_names_imported,
        stdlib_module_names  as module_names_stdlib,
    )

    # ....................{ CLASSES                        }....................
    class BeartypePytestWarning(BeartypeWarning):
        '''
        Beartype :mod:`pytest` warning.

        This warning is emitted at :mod:`pytest` configuration time when one
        or more packages or modules to be type-checked have already been
        imported under the active Python interpreter.
        '''

    # ....................{ IMPORTED                       }....................
    # Tuple of the subset of these names corresponding to previously
    # imported packages and modules under the active Python interpreter.
    if '*' in package_names:
        package_names_ignorable = (
            _PACKAGE_NAMES_IGNORABLE |
            # Note that:
            # * The standard "sys.stdlib_module_names" global is a frozenset.
            # * The standard "sys.builtin_module_names" global is a *TUPLE*
            #   rather than a frozenset. Why? No idea. Both globals should have
            #   been defined to be frozensets. Thanks a lot, Python interpreter.
            module_names_stdlib |
            frozenset(module_names_builtin)
        )

        package_names_imported = sorted({
            module.partition('.')[0] for module in module_names_imported})

        package_imported_names = tuple(
            package_name_imported
            for package_name_imported in package_names_imported
            if package_name_imported not in package_names_ignorable
        )
    else:
        package_imported_names = tuple(
            package_name
            for package_name in package_names
            if package_name in module_names_imported
        )

    # If one or more of these packages have already been imported...
    if package_imported_names:
        # Defer global imports to improve "pytest" startup performance.
        from warnings import warn

        # Comma-delimited double-quoted string listing these packages. Yeah!
        package_imported_names_str = join_delimited(
            strs=package_imported_names,
            delimiter_if_two=' and ',
            delimiter_if_three_or_more_nonlast=', ',
            delimiter_if_three_or_more_last=', and ',
            is_double_quoted=True,
        )

        # Emit a non-fatal warning informing the user.
        warn(
            (
                f'Previously imported packages '
                f'{package_imported_names_str} not checkable by beartype.'
            ),
            BeartypePytestWarning,
            stacklevel=1,  # <-- dark magic glistens dangerously
        )
    # Else, none of these packages have already been imported.

    # ....................{ IMPORT HOOK                    }....................
    #FIXME: Is the coercion to "tuple" really necessary here? *sigh*
    beartype_conf = BeartypeConf(
        claw_skip_package_names=tuple(skip_package_names))
    # print(f'Hooking packages {repr(package_names)} (skipping {repr(skip_package_names)})...')

    # Install an import hook type-checking these packages and modules.
    if '*' in package_names:
        beartype_all(conf=beartype_conf)
    else:
        beartype_packages(package_names, conf=beartype_conf)
