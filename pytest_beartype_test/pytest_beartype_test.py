#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

# ....................{ TODO                               }....................
#FIXME: Tests defined by this submodule succeed under the "tox" command but fail
#under the "pytest" command, presumably because the former ensures that this
#package is installed as a valid "pytest" plugin whereas the latter does not.
#Consider skipping these tests if running directly under "pytest", please.

# ....................{ TESTS ~ fork                       }....................
def test_beartype_packages_pass(tmp_path: 'pathlib.Path') -> None:
    '''
    Test that pytest runs successfully when there are no beartype violations.

    Parameters
    ----------
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to this test.
    '''

    # "subprocess.CompletedProcess" object encapsulating the result of running a
    # shell command forking the active Python interpreter as a subprocess
    # executing the "pytest" package installed under that interpreter against
    # the subset of this test suite applicable to this integration test.
    command_result = _run_pytest_plugin_test(
        test_module_basename='test_good_weather',
        data_subpackage_basename='good_weather_package',
        tmp_path=tmp_path,
    )

    # Assert this command succeeded by returning non-zero exit status.
    assert command_result.returncode == 0, (
        f'pytest failed with output: '
        f'{command_result.stdout}\n{command_result.stderr}'
    )


def test_beartype_packages_fail(tmp_path: 'pathlib.Path') -> None:
    '''
    Test that pytest fails when there are beartype violations.

    Parameters
    ----------
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to this test.
    '''

    # "subprocess.CompletedProcess" object encapsulating the result of running a
    # shell command forking the active Python interpreter as a subprocess
    # executing the "pytest" package installed under that interpreter against
    # the subset of this test suite applicable to this integration test.
    command_result = _run_pytest_plugin_test(
        test_module_basename='test_bad_weather',
        data_subpackage_basename='bad_weather_package',
        tmp_path=tmp_path,
    )

    # Assert this command failed by returning non-zero exit status.
    assert command_result.returncode != 0, (
        f'pytest should have failed but passed: '
        f'{command_result.stdout}\n{command_result.stderr}'
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
        function. This data submodule must be imported by the passed test
        submodule.
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to this test.

    Returns
    -------
    subprocess.CompletedProcess
        Object encapsulating the result of running this shell command.
    '''

    # Defer test-specific imports.
    from pathlib import Path
    from subprocess import run
    from sys import executable

    # Validate passed parameters.
    assert isinstance(test_module_basename, str), (
        f'{repr(test_module_basename)} not string.')
    assert isinstance(data_subpackage_basename, str), (
        f'{repr(data_subpackage_basename)} not string.')
    assert isinstance(tmp_path, Path), f'{repr(tmp_path)} not "pathlib" path.'

    # Pathlib path encapsulating the absolute filename of an empty "pytest.ini"
    # file residing in the temporary directory uniquely isolated to this test.
    pytest_config_file_empty = tmp_path / 'pytest.ini'

    # Ensure this file exists as a 0-byte empty file.
    pytest_config_file_empty.touch()

    # List of the one or more POSIX-compliant words comprising the shell command
    # forking the active Python interpreter as a subprocess executing the
    # "pytest" package installed under that interpreter against the subset of
    # this test suite applicable to all tests defined by the test submodule with
    # this basename.
    command_words = [
        executable,
        '-m',
        'pytest',

        #FIXME: *UNCOMMENT THIS TO DEBUG WHEN SOMETHING GOES PEAR-SHAPED.*
        # Prevent pytest from capturing (i.e., squelching) both standard
        # output and error by default.
        '--capture=no',

        # Force pytest to default to its default configuration by directing
        # pytest to use the empty "pytest.ini" file created above.
        f'--config-file={str(pytest_config_file_empty)}',

        '--tb=short',
        '--verbose',

        # Register a "beartype.claw" import hook type-checking all callables
        # and types defined by all submodules in this data subpackage.
        # f'--beartype-packages={data_subpackage_basename}',
        (
            '--beartype-packages='
            f'"pytest_beartype_test.{data_subpackage_basename}"'
        ),

        '--override-ini', f'python_files={test_module_basename}.py',
        f'pytest_beartype_test/{test_module_basename}.py',
    ]

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
    )

    # Return this result.
    return command_result

# ....................{ TESTS ~ pytester                   }....................
def test_pytest(pytester, beartype_pytest_tests):
    '''
    Test that specific test functions fail when beartype checking is enabled
    (default behavior).
    '''

    for test_file in beartype_pytest_tests:
        pytester.copy_example(str(test_file))

    result = pytester.runpytest()

    desc = ''' This means that fixture/function beartype checking inside pytest
    does not work correctly.
    '''

    # Parse the outcomes
    outcomes = result.parseoutcomes()

    # Note that "xfailed" in the outcomes is fine: it can be interpreted as
    # "the test failed as expected" -> so all is good
    assert 'failed' not in outcomes, (
        f'Something failed when testing pytest while running '
        f'pytest inside of pytest... test-ception?{desc}'
    )
    assert 'error' not in outcomes, (
        f'Oh-oh, internal pytest error in the plugin - '
        f'something pretty bad happened, maybe new pytest version?{desc}'
    )
