#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin **option utilities** (i.e., low-level callables inspecting :mod:`pytest`
options in a general-purpose manner transparently supporting both command-line
*and* configuration file options).
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

# ....................{ TESTERS                            }....................
#FIXME: Unit test us up, please. *sigh*
def is_pytest_option_bool(
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

# ....................{ GETTERS                            }....................
#FIXME: Unit test us up, please. *sigh*
def get_pytest_option_tuple_strs(
    config: 'pytest.Config', option_name: str) -> tuple[str, ...]:
    '''
    Tuple of the zero or more strings corresponding to the concatenation of
    both:

    * All comma-delimited substrings passed by the user as the command-line
      option with the passed name.
    * All TOML- or INI-formatted substrings configured by the user for the
      option with the passed name in the user-defined ``pyproject.toml`` or
      ``pytest.ini`` configuration files. Note that the former assumes
      precedence over the latter.

    Note that this getter intentionally returns an immutable (and thus hashable)
    tuple rather than a mutable (and thus unhashable) list of strings. The
    former is substantially more useful than the latter within the context of
    the :mod:`beartype` codebase, whose deep memoization commonly requires
    immutable rather than mutable containers.

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
    tuple[str, ...]
        Tuple of the zero or more strings passed by the user for this option.
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

    # Tuple to be returned, coerced from this list.
    option_tuple_strs = tuple(option_list)

    # Sanity test this list *BEFORE* proceeding down a dark road of pain.
    assert isinstance(option_tuple_strs, tuple)
    assert all(
        isinstance(option_item, str) for option_item in option_tuple_strs)

    # Return this tuple.
    return option_tuple_strs

# ....................{ PRIVATE ~ options : adders         }....................
#FIXME: Unit test us up, please. *sigh*
def add_pytest_option_bool(
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
    add_pytest_option(
        parser=parser,
        option_name_cli=option_name_cli,
        option_type_cli='store_true',
        option_name_conf=option_name_conf,
        option_type_conf='bool',
        help_message=help_message,
    )


#FIXME: Unit test us up, please. *sigh*
def add_pytest_option_list(
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
    add_pytest_option(
        parser=parser,
        option_name_cli=option_name_cli,
        option_type_cli='store',
        option_name_conf=option_name_conf,
        option_type_conf='args',
        help_message=help_message,
    )


#FIXME: Unit test us up, please. *sigh*
def add_pytest_option(
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
