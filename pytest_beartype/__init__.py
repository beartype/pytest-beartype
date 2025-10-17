#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
`pytest-beartype`.

`pytest` plugin type-checking fixtures, tests, and tested code with beartype.
'''

# ....................{ TODO                               }....................
#FIXME: Refactor for maintainability by splitting this overly verbose submodule
#into multiple smaller submodules. Verily, the time has come. \o/

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
def pytest_addoption(parser: 'pytest.Parser') -> None:
    '''
    Hook programmatically adding new plugin-specific options to both the
    `pytest` command-line interface (CLI) *and* top-level configuration files
    (e.g., `"pyproject.toml"`, `"pytest.ini"`).

    Parameters
    ----------
    parser: pytest.Parser
        Pytest parser for plugin-specific options.
    '''

    # Plugin option type-checking one or more packages with an
    # beartype.claw.beartype_packages() import hook.
    _add_pytest_option_list(
        parser=parser,
        option_name_cli='--beartype-packages',
        option_name_conf='beartype_packages',
        help_message=(
            'comma-delimited list of the names of all packages and modules to '
            'type-check with beartype'
        ),
    )

    # Plugin option preventing one or more packages from being type-checked by a
    # beartype.claw.beartype_packages() import hook.
    _add_pytest_option_list(
        parser=parser,
        option_name_cli='--beartype-skip-packages',
        option_name_conf='beartype_skip_packages',
        help_message=(
            'comma-delimited list of the names of all packages and modules to '
            'avoid type-checking with beartype'
        ),
    )

    # Plugin option type-checking pytest tests.
    _add_pytest_option_bool(
        parser=parser,
        option_name_cli='--beartype-tests',
        option_name_conf='beartype_tests',
        help_message='type-check pytest test functions with beartype',
    )

    # Plugin option type-checking pytest fixtures.
    _add_pytest_option_bool(
        parser=parser,
        option_name_cli='--beartype-fixtures',
        option_name_conf='beartype_fixtures',
        help_message='type-check pytest fixture functions with beartype',
    )


def pytest_configure(config: 'pytest.Config') -> None:
    '''
    Hook programmatically handling new plugin-specific options previously added
    by the :func:`.pytest_addoption` hook.

    Parameters
    ----------
    config : pytest.Config
        **Pytest configuration** (i.e., object encapsulating all user-defined
        pytest options both passed at the command line *and* set in the
        the ``pyproject.toml`` and/or ``pytest.ini`` files).
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
        config=config, option_name='beartype_packages')

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
            config=config, option_name='beartype_skip_packages')

        # Register a new "beartype.claw" import hook automatically type-checking
        # these packages and modules (excluding these packages and modules to be
        # skipped) subsequently imported during pytest test execution.
        _beartype_packages(
            package_names=package_names, skip_package_names=skip_package_names)


def pytest_collection_modifyitems(
    config: 'pytest.Config', items: list['pytest.Item']) -> None:
    '''
    Conditionally decorate *all* collected test functions by the
    :func:`beartype.beartype` decorator if instructed to do so by the user
    (e.g., if passed the ``--beartype-tests`` command-line option).
    '''

    # If *NOT* instructed by the user to type-check tests, reduce to a noop.
    if not _is_pytest_option_bool(config=config, option_name='beartype_tests'):
        return
    # Else, the user instructed this plugin to type-check tests.

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

    # If either...
    if (
        # *NOT* instructed by the user to type-check fixtures *OR*...
        not _is_pytest_option_bool(
            config=request.config, option_name='beartype_fixtures') or
        # This fixture has already been type-checked...
        hasattr(fixturedef, '_beartype_decorated')
    ):
        # Then silently reduce to a noop.
        return
    # Else, the user instructed this plugin to type-check tests *AND* this
    # fixture has yet to be type-checked.

    # Defer heavyweight imports.
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


def pytest_pyfunc_call(pyfuncitem: 'pytest.Function') -> bool | None:
    '''
    Expose type-checked fixture failures (as previously recorded during fixture
    collection by the :func:`.pytest_fixture_setup` hook) during each call to a
    test parametrized by that fixture.

    Pytest runs this hook during test execution, enabling this plugin to
    gracefully propagate prior fixture failures into a current test failure.
    Pytest is test-centric. Pytest is *not* fixture-centric. Pytest only has a
    means of reporting test failures. Pytest has *no* means of reporting fixture
    failures. The only means of reporting fixture failures is to coerce fixture
    failures into test failures.
    '''

    # If *NOT* instructed by the user to type-check tests, reduce to a noop. See
    # below for further commentary on why "None" is returned. *sigh*
    if not _is_pytest_option_bool(
        config=pyfuncitem.config, option_name='beartype_tests'):
        return None
    # Else, the user instructed this plugin to type-check tests.

    # Check all fixture values for beartype failures before calling the test
    for argname in pyfuncitem.fixturenames:
        fixture_value = pyfuncitem._request.getfixturevalue(argname)
        if isinstance(fixture_value, _BeartypeFixtureFailure):
            # Defer global imports to improve pytest startup performance.
            from traceback import format_tb

            failure_message_traceback = ''
            failure_traceback = getattr(
                fixture_value.fixture_exception, '__traceback__', None)

            # Include traceback in the error message for better debugging.
            if failure_traceback:
                failure_traceback_formatted = format_tb(failure_traceback)
                failure_message_traceback = (
                    f'\n{"".join(failure_traceback_formatted)}')

            # Message to be emitted as the cause of the failure of this test.
            failure_message = (
                f'Fixture "{fixture_value.fixture_name}" failed '
                f'beartype type-checking: '
                f'{fixture_value.fixture_exception}'
                f'{failure_message_traceback}'
            )

            # Mark this test as a failure with this failure message.
            pytest.fail(failure_message, pytrace=False)

    # Return "None", instructing pytest to call this test as it normally would.
    # Look. We don't make the rules. We just shrug our shoulders as others make
    # bad rules that make no sense whatsoever. Welcome to Planet Python.
    return None

# ....................{ PRIVATE ~ globals                  }....................
_PACKAGE_NAMES_IGNORABLE = frozenset((
    '__main__',
    '_pytest',
    'beartype',
    'cmd',
    'code',
    'codeop',
    'iniconfig',
    'pluggy',
    'py',
    'pytest',
    'pytest_beartype',
    'rlcompleter',
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

# ....................{ PRIVATE ~ options : adders         }....................
#FIXME: Unit test us up, please. *sigh*
def _add_pytest_option_bool(
    parser: 'pytest.Parser',
    option_name_cli: str,
    option_name_conf: str,
    help_message: str,
) -> None:
    '''
    Add a new plugin-specific :mod:`pytest` **boolean option** (i.e., option
    accepting no value, defaulting to :data:`False` and settable to :data:`True`
    merely by being passed) configurable by users either passing a command-line
    option with the passed name *or* setting an option with the passed name in a
    user-defined ``pyproject.toml`` or ``pytest.ini`` file.

    Parameters
    ----------
    parser: pytest.Parser
        Pytest parser for plugin-specific options.
    option_name_cli : str
        Name of the command-line option unique to this plugin to be added.
    option_name_conf : str
        Name of the configuration file option unique to this plugin to be added.
    help_message : str
        Human-readable string displayed to users requesting help with either of
        these command-line or configuration file options.
    '''

    # Defer to this lower-level option adder.
    _add_pytest_option(
        parser=parser,
        option_name_cli=option_name_cli,
        option_type_cli='store_true',
        option_name_conf=option_name_conf,
        option_type_conf='bool',
        help_message=help_message,
    )


#FIXME: Unit test us up, please. *sigh*
def _add_pytest_option_list(
    parser: 'pytest.Parser',
    option_name_cli: str,
    option_name_conf: str,
    help_message: str,
) -> None:
    '''
    Add a new plugin-specific :mod:`pytest` **list option** (i.e., comma- or
    whitespace-delimited list of strings) configurable by users either passing a
    command-line option with the passed name *or* setting an option with the
    passed name in a user-defined ``pyproject.toml`` or ``pytest.ini`` file.

    Parameters
    ----------
    parser: pytest.Parser
        Pytest parser for plugin-specific options.
    option_name_cli : str
        Name of the command-line option unique to this plugin to be added.
    option_name_conf : str
        Name of the configuration file option unique to this plugin to be added.
    help_message : str
        Human-readable string displayed to users requesting help with either of
        these command-line or configuration file options.
    '''

    # Defer to this lower-level option adder.
    _add_pytest_option(
        parser=parser,
        option_name_cli=option_name_cli,
        option_type_cli='store',
        option_name_conf=option_name_conf,
        option_type_conf='args',
        help_message=help_message,
    )


#FIXME: Unit test us up, please. *sigh*
def _add_pytest_option(
    parser: 'pytest.Parser',
    option_name_cli: str,
    option_type_cli: str,
    option_name_conf: str,
    option_type_conf: str,
    help_message: str,
) -> None:
    '''
    Add a new plugin-specific :mod:`pytest` option configurable by users either
    passing a command-line option with the passed name *or* setting an option
    with the passed name in a user-defined ``pyproject.toml`` or ``pytest.ini``
    file.

    Parameters
    ----------
    parser: pytest.Parser
        Pytest parser for plugin-specific options.
    option_name_cli : str
        Name of the command-line option unique to this plugin to be added.
    option_type_cli : str
        Enumeration member defined as a machine-readable string describing the
        type of this command-line option.
    option_name_conf : str
        Name of the configuration file option unique to this plugin to be added.
    option_type_conf : str
        Enumeration member defined as a machine-readable string describing the
        type of this configuration file option.
    help_message : str
        Human-readable string displayed to users requesting help with either of
        these command-line or configuration file options.

    See Also
    --------
    https://docs.pytest.org/en/stable/reference/reference.html#pytest.Parser.addini
        Upstream documentation describing all possible types of configuration
        file options.
    '''
    assert isinstance(option_name_cli, str), (
        f'{repr(option_name_cli)} not string.')
    assert isinstance(option_type_cli, str), (
        f'{repr(option_type_cli)} not string.')
    assert isinstance(option_name_conf, str), (
        f'{repr(option_name_conf)} not string.')
    assert isinstance(option_type_conf, str), (
        f'{repr(option_type_conf)} not string.')
    assert isinstance(help_message, str), (
        f'{repr(help_message)} not string.')

    # Plugin-specific group of command-line options.
    option_group = parser.getgroup('beartype')

    # Add this command-line option.
    option_group.addoption(
        option_name_cli, action=option_type_cli, help=help_message)

    # Add this configuration file option.
    parser.addini(option_name_conf, type=option_type_conf, help=help_message)  # type: ignore[arg-type]

# ....................{ PRIVATE ~ options : testers        }....................
#FIXME: Unit test us up, please. *sigh*
def _is_pytest_option_bool(
    config: 'pytest.Config', option_name: str) -> bool:
    '''
    :data:`True` only if the user either passed a command-line option with the
    passed name *or* defined an option with the passed name in the user-defined
    ``pyproject.toml`` or ``pytest.ini`` configuration files.

    Parameters
    ----------
    config : pytest.Config
        **Pytest configuration** (i.e., object encapsulating all user-defined
        pytest options both passed at the command line *and* set in the
        the ``pyproject.toml`` and/or ``pytest.ini`` files).
    option_name : str
        Snakecase-formatted name of both the command-line *and* configuration
        file options previously added by the :func:`.pytest_addoption` hook.
        Note that pytest expects this name to be **snakecase** (i.e., consisting
        only of alphanumeric characters as well as the underscore).

    Returns
    -------
    bool
        :data:`True` only if the user either passed or defined this option.
    '''
    assert isinstance(option_name, str), f'{repr(option_name)} not string.'

    # Return true only if the user either...
    return (
        # Defined an option with this name in a user-defined configuration file
        # *OR*...
        #
        # Note that *ONLY* the Config.getoption() method called below accepts an
        # optional default. The Config.getini() method called here accepts *NO*
        # such parameter. Ergo, Config.getini() must be called *BEFORE*
        # Config.getoption() is called.
        config.getini(option_name) or
        # Passed a command-line option with this name.
        config.getoption(option_name, False)
    )

# ....................{ PRIVATE ~ options : getters        }....................
#FIXME: Unit test us up, please. *sigh*
def _get_pytest_option_list(
    config: 'pytest.Config', option_name: str) -> list[str]:
    '''
    List of the zero or more strings corresponding to the concatenation of both:

    * All comma-delimited substrings passed by the user as the command-line
      option with the passed name.
    * All TOML- or INI-formatted substrings configured by the user for the
      option with the passed name in the user-defined ``pyproject.toml`` or
      ``pytest.ini`` configuration files. Note that the former assumes
      precedence over the latter.

    Parameters
    ----------
    config : pytest.Config
        **Pytest configuration** (i.e., object encapsulating all user-defined
        pytest options both passed at the command line *and* set in the
        the ``pyproject.toml`` and/or ``pytest.ini`` files).
    option_name : str
        Snakecase-formatted name of both the command-line *and* configuration
        file options previously added by the :func:`.pytest_addoption` hook.
        Note that pytest expects this name to be **snakecase** (i.e., consisting
        only of alphanumeric characters as well as the underscore).

    Returns
    -------
    list[str]
        List of the zero or more strings passed by the user for this option.
    '''
    assert isinstance(option_name, str), f'{repr(option_name)} not string.'

    # List of the one or more TOML- or INI-formatted substrings configured by
    # the user for the option with this name in the user-defined
    # "pyproject.toml" and/or "pytest.ini" files.
    option_list: list[str] = config.getini(option_name)

    # String list of the one or more comma-delimited substrings passed by the
    # user as the command-line option with this name.
    option_list_str = config.getoption(option_name, '')

    # If the user passed this command-line option...
    if option_list_str:
        # Strip this option of all prefixing and suffixing single and double
        # quotes for compliance with GNU-style long option values (e.g.,
        # --beartype-packages="muh_package,muh_other_package"). Ideally, the
        # config.getoption() called above should have already done this. The
        # config.getoption() called above does not, presumably due to laziness.
        option_list_str_stripped = option_list_str.strip('"').strip("'")

        # Extend this list by the list of comma-delimited substrings passed as
        # this option.
        option_list.extend(option_list_str_stripped.split(','))
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
