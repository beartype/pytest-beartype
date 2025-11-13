#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Integration test validating both the ``--beartype-tests`` and
``--beartype-fixtures`` command-line options accepted by this plugin.
'''

# ....................{ TESTS                              }....................
def test_option_beartype_tests(
    pytester: 'pytest.pytester',
    path_test_pytester_option_beartype_tests: 'pathlib.Path',
) -> None:
    '''
    Integration test validating that the ``--beartype-tests`` option accepted by
    this plugin correctly type-checks *all* pytest test functions.

    Parameters
    ----------
    pytester : 'pytest.pytester'
        Standard :mod:`pytest` fixture enabling plugins to be tested.
    path_test_pytester_option_beartype_tests : 'pathlib.Path'
        :class:`pathlib.Path` object encapsulating the absolute filename of the
        ``pytest_beartype_test.a90_func.data.test_pytester_option_beartype_tests``
        submodule.
    '''

    # Fork the active Python interpreter into a subprocess safely running a new
    # "pytest" command passed this plugin-specific option, which then collects
    # and executes this temporary file as a test file subject to this option.
    _run_pytester_plugin_test(
        pytester=pytester,
        pytest_option='--beartype-tests',
        test_submodule_path=path_test_pytester_option_beartype_tests,
    )


def test_option_beartype_fixtures(
    pytester: 'pytest.pytester',
    path_test_pytester_option_beartype_fixtures: 'pathlib.Path',
) -> None:
    '''
    Integration test validating that the ``--beartype-fixtures`` option accepted
    by this plugin correctly type-checks *all* pytest test functions.

    Parameters
    ----------
    pytester : 'pytest.pytester'
        Standard :mod:`pytest` fixture enabling plugins to be tested.
    path_test_pytester_option_beartype_fixtures : 'pathlib.Path'
        :class:`pathlib.Path` object encapsulating the absolute filename of the
        ``pytest_beartype_test.a90_func.data.test_pytester_option_beartype_fixtures``
        submodule.
    '''

    # Fork the active Python interpreter into a subprocess safely running a new
    # "pytest" command passed this plugin-specific option, which then collects
    # and executes this temporary file as a test file subject to this option.
    _run_pytester_plugin_test(
        pytester=pytester,
        pytest_option='--beartype-fixtures',
        test_submodule_path=path_test_pytester_option_beartype_fixtures,
    )

# ....................{ PRIVATE                            }....................
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

    # Copy this test submodule to a temporary file.
    #
    # Note that this call implicitly raises a "pytest.LookupError" exception if
    # this test submodule does *NOT* exist. We needn't validate that manually.
    pytester.copy_example(str(test_submodule_path))

    # "pytest.pytester.RunResult" object encapsulating the result of forking the
    # current root "pytest" process into an isolated "pytest" subprocess safely
    # passed these test-specific options, which then collects and executes this
    # temporary file as a test file subject to these options.
    pytest_result = pytester.runpytest_subprocess(pytest_option)
    # print(f'pytest_result: {type(pytest_result)}; {dir(pytest_result)}')

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
        # Re-raise this low-level assertion as a high-level assertion whose
        # message is both readable *AND* contains the standard output and error
        # of this failing "pytest" subprocess.
        raise AssertionError(
            f'One or more pytest tests or fixtures unexpectedly '
            f'failed type-checking in "pytester"-driven "pytest" subprocess:'
            f'\n\n[standard output]\n{'\n'.join(pytest_result.outlines)}'
            f'\n\n[standard error]\n{'\n'.join(pytest_result.errlines)}'
        ) from exception
