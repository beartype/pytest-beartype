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
    Integration test validating that the ``--beartype-fixtures`` option accepted by
    this plugin correctly type-checks *all* pytest test functions.

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
    '''
    assert isinstance(pytest_option, str), f'{repr(pytest_option)} not string.'

    # Copy this test submodule to a temporary file.
    pytester.copy_example(str(test_submodule_path))

    # Fork the active Python interpreter into a subprocess safely running a new
    # "pytest" command passed this plugin-specific option, which then collects
    # and executes this temporary file as a test file subject to this option.
    pytest_result = pytester.runpytest_subprocess(pytest_option)

    # Parse the result of this fork.
    outcomes = pytest_result.parseoutcomes()

    assertion_failure_explanation = (
        ' This means that fixture/function beartype checking inside pytest '
        'does not work correctly.'
    )

    # Note that "xfailed" in the outcomes is fine: it can be interpreted as
    # "the test failed as expected" -> so all is good
    assert 'failed' not in outcomes, (
        f'Something failed when testing pytest while running '
        f'pytest inside of pytest... test-ception?'
        f'{assertion_failure_explanation}'
    )
    assert 'error' not in outcomes, (
        f'Oh-oh, internal pytest error in the plugin - '
        f'something pretty bad happened, maybe new pytest version?'
        f'{assertion_failure_explanation}'
    )
