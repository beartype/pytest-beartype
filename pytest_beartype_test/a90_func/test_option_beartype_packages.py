#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin **package type-checking integration tests** (i.e., tests validating the
``--beartype-packages`` command-line option accepted by this plugin).
'''

# ....................{ TESTS                              }....................
def test_option_beartype_packages(
    monkeypatch: 'MonkeyPatch', tmp_path: 'pathlib.Path') -> None:
    '''
    Integration test validating the ``--beartype-packages`` command-line option
    accepted by this plugin behaves as expected.

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        :mod:`pytest` fixture allowing various state associated with the active
        Python process to be temporarily changed for the duration of this test.
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to this test.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer test-specific imports.
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_unit_func_subpackage_dir)
    from pytest_beartype_test._util.pytcmdrun import run_pytest_plugin_test

    # ....................{ LOCALS                         }....................
    # Tuple of 2-tuples "(data_subpackage_basename, command_code_expected)",
    # where:
    # * "data_subpackage_basename" is the unqualified basename of a data
    #   subpackage containing at least one data submodule defining one or more
    #   callables and types to be type-checked by a "beartype.claw" import hook
    #   configured by passing the "--beartype-packages" option to the "pytest"
    #   command.
    # * "command_code_expected" is the 0-based exit status expected to be
    #   returned by calling the sample functions defined by this subpackage.
    SUBTEST_METADATA: tuple[tuple[str, int], ...] = (
        ('weather_good', 0),
        ('weather_bad', 0),
    )

    # Fully-qualified name of the test subpackage containing both this data
    # subpackage *AND* the corresponding unit tests.
    TEST_SUBPACKAGE_NAME = 'pytest_beartype_test.a00_unit.a90_func'

    # "Path" object encapsulating the absolute dirname of the unit-functional
    # test integration subpackage (i.e., directory providing all unit tests
    # intended to be run only from integration tests).
    TEST_UNIT_FUNC_SUBPACKAGE_DIR = get_test_unit_func_subpackage_dir()

    # ....................{ PATCHES                        }....................
    # Temporarily export an environment variable accessible to the "pytest"
    # subprocesses forked by the run_pytest_plugin_test() function called
    # below, notifying the subordinate test_bad_weather_usage() unit
    # test invoked by these subprocesses that the data submodule it imports has
    # been type-checked by "beartype.claw" import hooks.
    monkeypatch.setenv('BEARTYPE_PACKAGES_OPTION_PASSED', '1')

    # ....................{ SUBPROCESSES                   }....................
    # For the unqualified basename of each of these data subpackages *AND* the
    # 0-based exit status expected to be returned by calling the sample
    # functions defined by this data subpackage...
    for data_subpackage_basename, command_code_expected in SUBTEST_METADATA:
        # Fully-qualified name of this data subpackage.
        data_subpackage_name = (
            f'{TEST_SUBPACKAGE_NAME}.data.{data_subpackage_basename}')

        # Unqualified basename (sans ".py" suffix) of the test submodule
        # defining one or more tests to be run.
        test_submodule_basename = f'test_{data_subpackage_basename}'

        # Fully-qualified name of this test submodule.
        test_submodule_name = (
            f'{TEST_SUBPACKAGE_NAME}.{test_submodule_basename}')

        # Path object encapsulating the absolute filename of the test submodule
        # with this basename.
        test_submodule_file = (
            TEST_UNIT_FUNC_SUBPACKAGE_DIR / f'{test_submodule_basename}.py')

        # "subprocess.CompletedProcess" object encapsulating the result of
        # running a shell command forking the active Python interpreter as a
        # subprocess executing the "pytest" package installed under that
        # interpreter against the subset of this test suite applicable to this
        # integration test.
        command_result = run_pytest_plugin_test(
            test_submodule_file=test_submodule_file,
            tmp_path=tmp_path,
            pytest_options=(
                # Register a "beartype.claw" import hook type-checking *ALL*
                # submodules transitively residing in this data subpackage.
                f'--beartype-packages="{data_subpackage_name}"',
            ),
        )

        # Assert this command succeeded by returning non-zero exit status.
        #
        # Note this assertion *MUST* be directly performed by this test rather
        # than the run_pytest_plugin_test() utility function called above.
        # Why? Pytest rewrites assertions via abstract syntax tree (AST)
        # transformations applied by non-trivial import hooks, which *ONLY*
        # apply to collected tests. (Non-trivial. It is what it is.)
        assert command_result.returncode == command_code_expected, (
            f'Integration test "test_option_beartype_packages" '
            f'subordinate unit test "{test_submodule_name}" '
            f'exit status {command_result.returncode} != '
            f'{command_code_expected}:'
            f'\n\n[standard output]\n{command_result.stdout}'
            f'\n\n[standard error]\n{command_result.stderr}'
        )
