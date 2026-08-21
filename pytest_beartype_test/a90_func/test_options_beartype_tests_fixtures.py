#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Integration test validating both the ``--beartype-tests`` and
``--beartype-test-fixtures`` command-line options accepted by this plugin.
'''

# ....................{ TESTS                              }....................
def test_option_beartype_tests(tmp_path: 'pathlib.Path') -> None:
    '''
    Integration test validating that the ``--beartype-tests`` option accepted by
    this plugin correctly type-checks *all* pytest test functions.

    Parameters
    ----------
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to this test.
    '''

    # Defer test-specific imports.
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_func_data_pytester_option_beartype_tests)
    from pytest_beartype_test._util.pytcmdrun import run_pytest_plugin_test

    # "subprocess.CompletedProcess" object encapsulating the result of running
    # a shell command forking the active Python interpreter as a subprocess
    # executing the "pytest" package installed under that interpreter passed
    # this plugin-specific option, which then collects and executes this test
    # submodule subject to this option.
    command_result = run_pytest_plugin_test(
        test_submodule_file=(
            get_test_func_data_pytester_option_beartype_tests()),
        tmp_path=tmp_path,
        pytest_options=(
            # Instruct the third-party "pytest-asyncio" plugin to implicitly
            # collect and execute *ALL* asynchronous tests in this test
            # submodule. By default, that plugin only collects and executes
            # asynchronous tests explicitly decorated by the
            # "@pytest.mark.asyncio" marker.
            '--override-ini', 'asyncio_mode=auto',

            '--beartype-tests',
        ),
    )

    # Assert this command succeeded by returning zero exit status.
    #
    # Note this assertion *MUST* be directly performed by this test rather
    # than the run_pytest_plugin_test() utility function called above.
    # Why? Pytest rewrites assertions via abstract syntax tree (AST)
    # transformations applied by non-trivial import hooks, which *ONLY*
    # apply to collected tests. (Non-trivial. It is what it is.)
    assert command_result.returncode == 0, (
        f'Integration test "test_option_beartype_tests" '
        f'"pytest" subprocess exit status {command_result.returncode} != 0:'
        f'\n\n[standard output]\n{command_result.stdout}'
        f'\n\n[standard error]\n{command_result.stderr}'
    )


def test_option_beartype_fixtures(tmp_path: 'pathlib.Path') -> None:
    '''
    Integration test validating that the ``--beartype-test-fixtures`` option
    accepted by this plugin correctly type-checks *all* pytest fixtures.

    Parameters
    ----------
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to this test.
    '''

    # Defer test-specific imports.
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_func_data_pytester_option_beartype_fixtures,
        get_test_package_dir,
    )
    from pytest_beartype_test._util.pytcmdrun import run_pytest_plugin_test

    # "subprocess.CompletedProcess" object encapsulating the result of running
    # a shell command forking the active Python interpreter as a subprocess
    # executing the "pytest" package installed under that interpreter passed
    # this plugin-specific option, which then collects and executes this test
    # submodule subject to this option.
    command_result = run_pytest_plugin_test(
        test_submodule_file=(
            get_test_func_data_pytester_option_beartype_fixtures()),
        tmp_path=tmp_path,
        pytest_options=(
            # Force the "pytest" subprocess to treat this test suite's package
            # directory as its root directory, as this plugin *ONLY*
            # type-checks fixtures defined under the root directory of the
            # current test suite. By default, that subprocess would instead
            # treat the temporary directory containing the empty "pytest.ini"
            # file created by run_pytest_plugin_test() as its root directory --
            # in which case this plugin would silently preserve *ALL* fixtures
            # as is rather than type-checking these fixtures.
            #
            # Note that this root directory is intentionally the test suite's
            # package directory rather than this project's root directory. Why?
            # Because this project's root directory typically contains a
            # virtual environment (e.g., ".venv", ".tox") physically containing
            # the third-party "pytest-asyncio" plugin, whose fixtures would
            # then reside under that root directory and thus be type-checked by
            # this plugin -- unresolvable "typing.TYPE_CHECKING"-guarded
            # annotations and all. See also pull request #27.
            '--rootdir', str(get_test_package_dir()),

            # Instruct the third-party "pytest-asyncio" plugin to implicitly
            # collect and execute *ALL* asynchronous tests in this test
            # submodule. By default, that plugin only collects and executes
            # asynchronous tests explicitly decorated by the
            # "@pytest.mark.asyncio" marker.
            '--override-ini', 'asyncio_mode=auto',

            '--beartype-test-fixtures',
        ),
    )

    # Assert this command succeeded by returning zero exit status.
    #
    # Note this assertion *MUST* be directly performed by this test rather
    # than the run_pytest_plugin_test() utility function called above.
    # Why? Pytest rewrites assertions via abstract syntax tree (AST)
    # transformations applied by non-trivial import hooks, which *ONLY*
    # apply to collected tests. (Non-trivial. It is what it is.)
    assert command_result.returncode == 0, (
        f'Integration test "test_option_beartype_fixtures" '
        f'"pytest" subprocess exit status {command_result.returncode} != 0:'
        f'\n\n[standard output]\n{command_result.stdout}'
        f'\n\n[standard error]\n{command_result.stderr}'
    )
