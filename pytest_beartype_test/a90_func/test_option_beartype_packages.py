#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Integration test validating the ``--beartype-packages`` command-line option
accepted by this plugin.
'''

# ....................{ TODO                               }....................
#FIXME: This and the sibling "test_options_beartype_tests_fixtures" submodule
#test pytest plugin command-line option passing with two completely different
#mechanisms, which doesn't particularly make *ANY* sense whatsoever. Testing
#pytest plugin command-line option passing is sufficiently non-trivial that both
#of these submodules should be refactored to leverage the same exact approach.
#The question then becomes, "Which is better?" Both work. It's thus *NOT* a
#question of working. The only valid questions left are:
#
#* "Which produces more readable output?" If both produce equally readable
#  output *OR* can be configured to produce equally readable output (which is
#  probably the case), then the only remaining question is...
#* "Which is easier to maintain?"
#
#Honestly, the "pytester"-based solution implemented by the sibling
#"test_options_beartype_tests_fixtures" submodule seems to handily win out on
#maintainability, readability, and debuggability. There is a reason that the
#standard "pytester" plugin exists. It may be poorly documented, but it still
#beats the manual subprocess shenanigans employed by the
#run_pytest_plugin_test() function defined by the
#"pytest_beartype_test._util.pytcmdrun" submodule. *shrug*
#FIXME: *WAIT*. Actually, the "pytester"-based solution is *PROBABLY* deficient.
#Why? Because it doesn't support a package structure. You can't actually import
#anything from the "conftest" file. In fact, "__package__" is empty! This means
#that, if you go with a "pytester"-based solution, you literally have to embed
#*EVERY* single fixture you need into a single "conftest" file. Honestly, what a
#nightmare. "pytester" is a huge fail. No idea why anyone would prefer that over
#just forking "pytest" subprocesses like below. *shrug*

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

    # Defer test-specific imports.
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_unit_subpackage_dir)
    from pytest_beartype_test._util.pytcmdrun import run_pytest_plugin_test

    # Temporarily export an environment variable accessible to the "pytest"
    # subprocesses forked by the run_pytest_plugin_test() function called
    # below, notifying the subordinate test_bad_weather_usage() unit
    # test invoked by these subprocesses that the data submodule it imports has
    # been type-checked by "beartype.claw" import hooks.
    monkeypatch.setenv('BEARTYPE_PACKAGES_OPTION_PASSED', '1')

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
        ('good_weather', 0),
        ('bad_weather', 0),
    )

    # For the unqualified basename of each of these data subpackages *AND* the
    # 0-based exit status expected to be returned by calling the sample
    # functions defined by this data subpackage...
    for data_subpackage_basename, command_code_expected in SUBTEST_METADATA:
        # Unqualified basename (sans ".py" suffix) of the test submodule
        # defining one or more tests to be run.
        test_module_basename = f'test_{data_subpackage_basename}'

        # Fully-qualified name of this test submodule.
        test_module_name = (
            f'pytest_beartype_test.a00_unit.{test_module_basename}')

        # Path object encapsulating the absolute filename of the test submodule
        # with this basename.
        test_submodule_file = (
            get_test_unit_subpackage_dir() / f'{test_module_basename}.py')

        # "subprocess.CompletedProcess" object encapsulating the result of
        # running a shell command forking the active Python interpreter as a
        # subprocess executing the "pytest" package installed under that
        # interpreter against the subset of this test suite applicable to this
        # integration test.
        command_result = run_pytest_plugin_test(
            test_submodule_file=test_submodule_file,
            tmp_path=tmp_path,
            pytest_options=(
                # Register a "beartype.claw" import hook type-checking all
                # callables and types defined by all submodules in this data
                # subpackage.
                (
                    '--beartype-packages='
                    f'"pytest_beartype_test.a00_unit.data.'
                    f'{data_subpackage_basename}"'
                ),
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
            f'subordinate unit test "{test_module_name}" '
            f'exit status {command_result.returncode} != '
            f'{command_code_expected}:'
            f'\n\n[standard output]\n{command_result.stdout}'
            f'\n\n[standard error]\n{command_result.stderr}'
        )
