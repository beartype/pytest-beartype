#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **test suite subprocess runners** (i.e., low-level callables forking
the active Python interpreter as a subprocess executing the :mod:`pytest`
package installed under that interpreter against some subset of this test
suite).
'''

# ....................{ RUNNERS                            }....................
def run_pytest_plugin_test(
    # Mandatory parameters.
    test_submodule_file: 'pathlib.Path',
    tmp_path: 'pathlib.Path',

    # Optional parameters.
    pytest_options: 'collections.abc.Sequence[str]' = (),
) -> 'subprocess.CompletedProcess':
    '''
    Run a shell command forking the active Python interpreter as a subprocess
    executing the :mod:`pytest` package installed under that interpreter against
    all tests defined by the test submodule with the passed filename *and*
    return a :class:`subprocess.CompletedProcess` object encapsulating the
    result.

    Parameters
    ----------
    test_submodule_file : pathlib.Path
        :class:`pathlib.Path` object encapsulating the absolute filename of the
        test submodule defining one or more tests to be run.
    tmp_path: pathlib.Path
        Temporary directory uniquely isolated to the current test.
    pytest_options : collections.abc.Sequence[str], optional
        Sequence of zero or more command-line options to be passed to the
        ``pytest`` command run by this function -- typically including one or
        more plugin-specific options (e.g., ``--beartype-packages=...``) under
        test by the current test. Defaults to the empty tuple.

    Returns
    -------
    subprocess.CompletedProcess
        Object encapsulating the result of running this shell command.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer function-specific imports.
    from pathlib import Path
    from subprocess import run
    from sys import executable

    # Validate passed parameters *AFTER* importing requisite types above.
    assert isinstance(test_submodule_file, Path), (
        f'{repr(test_submodule_file)} not "pathlib" path.')
    assert isinstance(tmp_path, Path), f'{repr(tmp_path)} not "pathlib" path.'

    # ....................{ LOCALS ~ test submodule        }....................
    # Unqualified basename (sans ".py" suffix) of this test submodule.
    test_module_basename = test_submodule_file.stem

    # Absolute filename of this test submodule. test_submodule_file is a Path,
    # so this approach should be portable. We currently only use it as a
    # subprocess argument with shell=False (the default), so we shouldn't have
    # to further quote it. If that changes, we should probably do any necessary
    # quoting in close proximity to the subprocess call site.
    test_submodule_filename = str(test_submodule_file)

    # ....................{ LOCALS ~ pytest config         }....................
    # Path object encapsulating the absolute filename of an empty "pytest.ini"
    # file residing in the temporary directory uniquely isolated to this test.
    pytest_config_empty_file = tmp_path / 'pytest.ini'

    # Ensure this file exists as a 0-byte empty file.
    pytest_config_empty_file.touch()

    # Absolute filename of an empty "pytest.ini" file residing in the temporary
    # directory uniquely isolated to this test. Similar to test_submodule_file
    # above, pytest_config_empty_file is a Path, so this should be portable.
    pytest_config_empty_filename = str(pytest_config_empty_file)

    # ....................{ LOCALS ~ command               }....................
    # List of the one or more POSIX-compliant words comprising the shell command
    # forking the active Python interpreter as a subprocess executing the
    # "pytest" package installed under that interpreter against all tests
    # defined by this test submodule.
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

        # Pass all caller-specific options (e.g., plugin-specific options under
        # test by the current test) as is.
        *pytest_options,

        '--override-ini', f'python_files={test_module_basename}.py',
        f'{test_submodule_filename}',
    ]

    # ....................{ RUN                            }....................
    # "CompletedProcess" object encapsulating the result of running the shell
    # command forking the active Python interpreter as a subprocess executing
    # the "pytest" package installed under that interpreter against all tests
    # defined by this test submodule.
    command_result = run(
        command_words,
        cwd='.',
        capture_output=True,
        text=True,

        # This is the default, but we're making it explicit because we're
        # we're passing Path-derived, but not shell-quoted arguments
        # (constructed above).
        shell=False,

        # Prefer the test calling this utility function to assert the success
        # or failure of this command. Doing so substantially improves
        # debuggability. Enabling "check=True" does so little that it's
        # questionable why Python even defines this optional parameter.
        check=False,
    )

    # Return this result.
    return command_result
