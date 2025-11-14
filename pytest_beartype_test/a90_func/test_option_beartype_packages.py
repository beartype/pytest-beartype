#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Integration test validating the ``--beartype-packages`` command-line option
accepted by this plugin.
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

    # Temporarily export an environment variable accessible to the "pytest"
    # subprocesses forked by the private _run_pytest_plugin_test() function
    # called below, notifying the subordinate test_bad_weather_usage() unit
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

        # "subprocess.CompletedProcess" object encapsulating the result of
        # running a shell command forking the active Python interpreter as a
        # subprocess executing the "pytest" package installed under that
        # interpreter against the subset of this test suite applicable to this
        # integration test.
        command_result = _run_pytest_plugin_test(
            test_module_basename=test_module_basename,
            data_subpackage_basename=data_subpackage_basename,
            tmp_path=tmp_path,
        )

        # Assert this command succeeded by returning non-zero exit status.
        #
        # Note this assertion *MUST* be directly performed by this test rather
        # than the private _run_pytest_plugin_test() utility function called
        # above. Why? Pytest rewrites assertions via abstract syntax tree (AST)
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

# ....................{ PRIVATE ~ runners                  }....................
def _run_pytest_plugin_test(
    test_module_basename: str,
    data_subpackage_basename: str,
    tmp_path: 'pathlib.Path',
) -> 'subprocess.CompletedProcess':
    '''
    Run a shell command forking the active Python interpreter as a subprocess
    executing the :mod:`pytest` package installed under that interpreter against
    the subset of this test suite applicable to all tests defined by the test
    submodule with the passed basename *and* return a
    :class:`subprocess.CompletedProcess` object encapsulating the result.

    Parameters
    ----------
    test_module_basename : str
        Unqualified basename (sans ``".py"`` suffix) of the test submodule
        defining one or more tests to be run.
    data_subpackage_basename : str
        Unqualified basename of the data subpackage containing at least one
        data submodule defining one or more callables and types to be
        type-checked by a :mod:`beartype.claw` import hook configured by passing
        the ``--beartype-packages`` option to the ``pytest`` command run by this
        function.
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to this test.

    Returns
    -------
    subprocess.CompletedProcess
        Object encapsulating the result of running this shell command.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer test-specific imports.
    from pathlib import Path
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_unit_subpackage_dir)
    from subprocess import run
    from sys import executable

    # Validate passed parameters *AFTER* importing requisite types above.
    assert isinstance(test_module_basename, str), (
        f'{repr(test_module_basename)} not string.')
    assert isinstance(data_subpackage_basename, str), (
        f'{repr(data_subpackage_basename)} not string.')
    assert isinstance(tmp_path, Path), f'{repr(tmp_path)} not "pathlib" path.'

    # ....................{ LOCALS ~ test submodule        }....................
    # Path object encapsulating the absolute filename of the test submodule with
    # the passed basename.
    test_submodule_file = (
        get_test_unit_subpackage_dir() / f'{test_module_basename}.py')

    #FIXME: *NON-PORTABLE.* Ideally, this should be shell-quoted for safety. The
    #main @beartype codebase has private utilities for this, but we'd rather not
    #make this any more fragile than this needs to be. When needed, copy-paste
    #over the shell_quote() utility function from @beartype here. *sigh*
    # Absolute filename of the test submodule with the passed basename.
    test_submodule_filename = str(test_submodule_file)

    # ....................{ LOCALS ~ pytest config         }....................
    # Path object encapsulating the absolute filename of an empty "pytest.ini"
    # file residing in the temporary directory uniquely isolated to this test.
    pytest_config_empty_file = tmp_path / 'pytest.ini'

    # Ensure this file exists as a 0-byte empty file.
    pytest_config_empty_file.touch()

    #FIXME: *NON-PORTABLE.* Ideally, this should be shell-quoted for safety. The
    #main @beartype codebase has private utilities for this, but we'd rather not
    #make this any more fragile than this needs to be. When needed, copy-paste
    #over the shell_quote() utility function from @beartype here. *sigh*
    # Absolute filename of an empty "pytest.ini" file residing in the temporary
    # directory uniquely isolated to this test.
    pytest_config_empty_filename = str(pytest_config_empty_file)

    # ....................{ LOCALS ~ command               }....................
    # List of the one or more POSIX-compliant words comprising the shell command
    # forking the active Python interpreter as a subprocess executing the
    # "pytest" package installed under that interpreter against the subset of
    # this test suite applicable to all tests defined by the test submodule with
    # this basename.
    command_words = [
        executable,
        '-m',
        'pytest',

        # Prevent pytest from capturing (i.e., squelching) both standard
        # output and error by default.
        '--capture=no',

        # Force pytest to default to its default configuration by directing
        # pytest to use the empty "pytest.ini" file created above.
        f'--config-file={pytest_config_empty_filename}',

        '--tb=short',
        '--verbose',

        # Register a "beartype.claw" import hook type-checking all callables
        # and types defined by all submodules in this data subpackage.
        # f'--beartype-packages={data_subpackage_basename}',
        (
            '--beartype-packages='
            f'"pytest_beartype_test.a00_unit.data.{data_subpackage_basename}"'
        ),

        '--override-ini', f'python_files={test_module_basename}.py',
        f'{test_submodule_filename}',
    ]

    # ....................{ RUN                            }....................
    # "CompletedProcess" object encapsulating the result of running the shell
    # command forking the active Python interpreter as a subprocess executing
    # the "pytest" package installed under that interpreter against the subset
    # of this test suite applicable to all tests defined by the test submodule
    # with this basename.
    command_result = run(
        command_words,
        cwd='.',
        capture_output=True,
        text=True,

        # Prefer the integration test calling this utility function to assert
        # the success or failure of this command. Doing so substantially
        # improves debugabbility. Enabling "check=True" does so little that it's
        # questionable why Python even defines this optional parameter.
        check=False,
    )

    # Return this result.
    return command_result
