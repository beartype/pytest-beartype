#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Plugin initializiation** (i.e., :mod:`pytest` hook functions initializing the
``pytest-beartype`` plugin, including those registering plugin-specific options
accessible to users as both command-line options and configuration file
settings).
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

# ....................{ HOOKS ~ option                     }....................
def pytest_addoption(parser: 'pytest.Parser') -> None:
    '''
    Hook programmatically adding new plugin-specific options to both the
    ``pytest`` command-line interface (CLI) *and* top-level configuration files
    (e.g., ``"pyproject.toml"``, ``"pytest.ini"``).

    Parameters
    ----------
    parser: pytest.Parser
        Pytest parser for plugin-specific options.
    '''

    # Defer hook-specific imports.
    from pytest_beartype._util.utilopt import (
        add_pytest_option_list,
        add_pytest_option_bool,
    )

    # Plugin option type-checking one or more packages with an
    # beartype.claw.beartype_packages() import hook.
    add_pytest_option_list(
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
    add_pytest_option_list(
        parser=parser,
        option_name_cli='--beartype-skip-packages',
        option_name_conf='beartype_skip_packages',
        help_message=(
            'comma-delimited list of the names of all packages and modules to '
            'avoid type-checking with beartype'
        ),
    )

    # Plugin option type-checking pytest tests.
    add_pytest_option_bool(
        parser=parser,
        option_name_cli='--beartype-tests',
        option_name_conf='beartype_tests',
        help_message='type-check pytest test functions with beartype',
    )

    # Plugin option type-checking pytest fixtures.
    add_pytest_option_bool(
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

    # Defer hook-specific imports.
    from pytest_beartype._util.utilopt import get_pytest_option_list

    # print('In pytest_configure()...')

    # Comma-delimited string listing the fully-qualified names of *ALL* packages
    # and modules to be type-checked by beartype, corresponding to either:
    # * The "--beartype-packages" option passed to the "pytest" command.
    # * The "beartype_packages" option in user-defined "pyproject.toml" and
    #   "pytest.ini" files.
    #
    # See the pytest_addoption() hook defined above.
    package_names = get_pytest_option_list(
        config=config, option_name='beartype_packages')

    # If the user passed this option...
    if package_names:
        # Defer beartype-specific imports as late as feasible to minimize all
        # startup costs associated with this plugin.
        from pytest_beartype._bear.bearclaw import check_packages_on_import

        # Comma-delimited string listing the fully-qualified names of *ALL*
        # packages and modules to *NOT* be type-checked by beartype,
        # corresponding to either:
        # * The "--beartype-skip-packages" option passed to the "pytest"
        #   command.
        # * The "beartype_skip_packages" option in user-defined "pyproject.toml"
        #   and "pytest.ini" files.
        #
        # See the pytest_addoption() hook defined above.
        skip_package_names = get_pytest_option_list(
            config=config, option_name='beartype_skip_packages')

        # Register a new "beartype.claw" import hook automatically type-checking
        # these packages and modules (excluding these packages and modules to be
        # skipped) subsequently imported during pytest test execution.
        check_packages_on_import(
            package_names=package_names, skip_package_names=skip_package_names)
    # Else, the user did *NOT* pass this option...
