#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Integration test validating both the ``--beartype-tests`` and
``--beartype-fixtures`` command-line options accepted by this plugin.
'''

# ....................{ TESTS                              }....................
def test_option_beartype_tests(pytester: 'pytest.pytester') -> None:
    '''
    Integration test validating that the ``--beartype-tests`` option accepted by
    this plugin correctly type-checks *all* pytest test functions.

    Parameters
    ----------
    pytester : 'pytest.pytester'
        Standard :mod:`pytest` fixture enabling plugins to be tested.
    '''

    # Defer test-specific imports.
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_func_data_pytester_option_beartype_tests)

    # Fork the active Python interpreter into a subprocess safely running a new
    # "pytest" command passed this plugin-specific option, which then collects
    # and executes this temporary file as a test file subject to this option.
    _run_pytester_plugin_test(
        pytester=pytester,
        pytest_option='--beartype-tests',
        test_submodule_path=get_test_func_data_pytester_option_beartype_tests(),
    )


def test_option_beartype_fixtures(pytester: 'pytest.pytester') -> None:
    '''
    Integration test validating that the ``--beartype-fixtures`` option accepted
    by this plugin correctly type-checks *all* pytest test functions.

    Parameters
    ----------
    pytester : 'pytest.pytester'
        Standard :mod:`pytest` fixture enabling plugins to be tested.
    '''

    # Defer test-specific imports.
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_func_data_pytester_option_beartype_fixtures)

    # Fork the active Python interpreter into a subprocess safely running a new
    # "pytest" command passed this plugin-specific option, which then collects
    # and executes this temporary file as a test file subject to this option.
    _run_pytester_plugin_test(
        pytester=pytester,
        pytest_option='--beartype-fixtures',
        test_submodule_path=(
            get_test_func_data_pytester_option_beartype_fixtures()),
    )

# ....................{ PRIVATE ~ runners                  }....................
def _run_pytester_plugin_test(
    pytester: 'pytest.pytester',
    pytest_option: str,
    test_submodule_path: 'pathlib.Path',
) -> str:
    '''
    Run a shell command forking the active Python interpreter as a subprocess
    executing the :mod:`pytest` package installed under that interpreter against
    the subset of this test suite applicable to all tests defined by the test
    submodule with the passed basename *and* return all standard output and
    error emitted by that command.

    Parameters
    ----------
    pytester : 'pytest.pytester'
        Standard :mod:`pytest` fixture enabling plugins to be tested.
    pytest_option : str
        "``--``"-prefixed name of the plugin-specific :mod:`pytest` option to be
        passed to this :mod:`pytest` command.
    test_submodule_path : 'pathlib.Path'
        :class:`pathlib.Path` object encapsulating the absolute filename of the
        test submodule to be collected and executed by this :mod:`pytest`
        command.

    Returns
    -------
    str
        All standard output and error emitted by running this shell command.

    Raises
    ------
    pytest.LookupError
        If the passed test submodule does *not* exist on the local filesystem.
    '''
    assert isinstance(pytest_option, str), f'{repr(pytest_option)} not string.'

    # ....................{ IMPORTS                        }....................
    # Defer function-specific imports.
    from pytest_beartype_test._util.path.pytpathtest import (
        get_test_func_data_conftest)

    # ....................{ PATHS                          }....................
    # Copy this test pytest configuration to a temporary file.
    #
    # Note that this call implicitly raises a "pytest.LookupError" exception if
    # this configuration does *NOT* exist. We needn't validate that manually.
    pytester.makeconftest(get_test_func_data_conftest().read_text())

    # Copy this test submodule to a temporary file.
    #
    # Note that this call implicitly raises a "pytest.LookupError" exception if
    # this test submodule does *NOT* exist. We needn't validate that manually.
    pytester.copy_example(str(test_submodule_path))

    # ....................{ RUN                            }....................
    # "pytest.pytester.RunResult" object encapsulating the result of forking the
    # current root "pytest" process into an isolated "pytest" subprocess safely
    # passed these test-specific options, which then collects and executes this
    # temporary file as a test file subject to these options.
    #
    # Note that:
    # * Most (but *NOT* all) of these options are copied verbatim from the
    #   top-level "pytest.ini" configuration file for this project.
    # * We intentionally avoid copying that file with "pytester". Most of that
    #   file is inapplicable to the "pytest" subprocess forked below.
    #
    # Unconditionally pass the following command-line options to the "pytest"
    # subprocess forked below. Dismantled, this is:
    #
    # * "-v", increasing verbosity.
    # * "--full-trace", printing a full traceback on keyboard interrupts (e.g.,
    #   hitting <Ctrl-C> during testing at the command line).
    # * "-p no:asyncio", disabling the "pytest-asyncio" plugin -- which is
    #   *ABSOLUTELY* mad, doing horrifying things with unexpected side effects
    #   like:
    #   * Unconditionally importing *EVERYTHING* in our friggin' test suite,
    #     which then promptly raises non-human-readable exceptions during early
    #     test collection time. Like, "Just no, you imbecilic plugin!" Many of
    #     the submodules in our test suite are only safely importable in a
    #     conditional test-specific context.
    #   * Emitting senseless deprecation warnings on "pytest" startup
    #     resembling:
    #         INTERNALERROR> Traceback (most recent call last):
    #              ...
    #         INTERNALERROR>   File "/usr/lib/python3.8/site-packages/pytest_asyncio/plugin.py", line 186, in pytest_configure
    #         INTERNALERROR>     config.issue_config_time_warning(LEGACY_MODE, stacklevel=2)
    #         INTERNALERROR>   File "/usr/lib/python3.8/site-packages/_pytest/config/__init__.py", line 1321, in issue_config_time_warning
    #         INTERNALERROR>     warnings.warn(warning, stacklevel=stacklevel)
    #         INTERNALERROR> DeprecationWarning: The 'asyncio_mode' default value will change to 'strict' in future, please explicitly use 'asyncio_mode=strict' or 'asyncio_mode=auto' in pytest configuration file.
    #
    #     This is *ABSOLUTELY* senseless, because this project intentionally
    #     does *NOT* require, reference, or otherwise leverage "pytest-asyncio"
    #     anywhere. However, many other third-party packages you may have
    #     installed do. Thanks to them, *ALL* "pytest" invocations must now pass
    #     this vapid setting to avoid spewing trash across *ALL* "pytest"-driven
    #     test sessions. *double facepalm*
    # * "-p no:jaxtyping", disabling the "pytest-jaxtyping" plugin -- which
    #   *COULD* attempt to unsafely import JAX at test collection time. If this
    #   plugin does so, then the first unit test requiring forked subprocess
    #   isolation will inscrutably fail with a non-human-readable exception. See
    #   also the "beartype_test.a90_func.z90_lib.a80_jax.test_jax" submodule for
    #   details.
    # * "-p no:xvfb", disabling the "pytest-xvfb" plugin. Although technically
    #   harmless, this plugin unconditionally logs extraneous messages that
    #   hamper readability of pytest output. Ergo, it goes.
    # * "-r a", increasing verbosity of (a)ll types of test summaries.
    # * "--doctest-glob=", disabling implicit detection of doctests (i.e., tests
    #   embedded in docstrings that double as human-readable examples). By default,
    #   pytest runs all files matching the recursive glob "**/test*.txt" through
    #   the standard "doctest" module. Since this project employs explicit tests
    #   rather than implicit doctests, this detection is a non-fatal noop in the
    #   best case and a fatal conflict in the worst case. For collective sanity,
    #   this detection *MUST* be disabled.
    # * "--showlocals", printing local variable values in tracebacks.
    # * "-s", disable all stdout and stderr capturing.
    # See "pytest --help | less" for further details on available options.
    pytest_result = pytester.runpytest_subprocess(
        '-v',
        '--showlocals',
        '-p', 'no:asyncio',
        '-p', 'no:jaxtyping',
        '-p', 'no:xvfb',
        '-r', 'a',
        '-s',
        '-x',
        '--doctest-glob=',
        pytest_option,
    )
    # print(f'pytest_result: {type(pytest_result)}; {dir(pytest_result)}')

    # ....................{ ASSERTS                        }....................
    # Dictionary mapping from each pytest-specific noun (e.g., "failed") output
    # by this "pytest" subprocess to the number of tests whose outcome was that
    # noun.
    #
    # Note that this dictionary *ONLY* maps nouns that were explicitly output.
    # Nouns that were *NOT* explicitly output remain unmapped. It is thus unsafe
    # to directly access key-value pairs from this dictionary. Instead, *ONLY*
    # indirectly access key-value pairs by calling the dict.get() method with a
    # safe fallback (typically, 0 to imply the absence of that noun).
    #
    # For example, if this "pytest" subprocess outputs these outcome nouns:
    #     ======= 1 failed, 1 passed, 1 warning, 1 error in 0.13s ====
    #
    # ...then the contents of this dictionary will be:
    #     {"failed": 1, "passed": 1, "warnings": 1, "errors": 1}
    pytest_result_noun_to_count = pytest_result.parseoutcomes()

    # Attempt to...
    try:
        # Validate that this "pytest" subprocess succeeded with...
        pytest_result.assert_outcomes(
            # *NONE* of the following outcomes, *ALL* of which indicate an
            # unexpected test failure.
            skipped=0,
            failed=0,
            errors=0,
            xpassed=0,
            warnings=0,
            deselected=0,

            # An arbitrary number of the following outcomes, *ALL* of which are
            # irrelevant to the success or failure of this "pytest" subprocess.
            passed=pytest_result_noun_to_count.get('passed', 0),
            xfailed=pytest_result_noun_to_count.get('xfailed', 0),
        )
    # If doing so raises a low-level assertion whose message is largely
    # unreadable and fails to contain either the standard output or error of
    # this failing "pytest" subprocess: e.g.,
    #     AssertionError: assert "deselected": 1 == "deselected": 0
    except AssertionError as exception:
        # Standard output and error emitted by this failing "pytest" subprocess.
        pytest_result_stdout = '\n'.join(pytest_result.outlines)
        pytest_result_stderr = '\n'.join(pytest_result.errlines)

        # Re-raise this low-level assertion as a high-level assertion whose
        # message is both readable *AND* contains the standard output and error
        # of this failing "pytest" subprocess.
        raise AssertionError(
            f'One or more pytest tests or fixtures unexpectedly '
            f'failed type-checking in "pytester"-driven "pytest" subprocess:'
            f'\n\n[standard output]\n{pytest_result_stdout}'
            f'\n\n[standard error]\n{pytest_result_stderr}'
        ) from exception
