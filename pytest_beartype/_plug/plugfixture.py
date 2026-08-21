#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin-specific **fixture type-checking** (i.e., :mod:`pytest` hook functions
generalizing the runtime behaviour of :mod:`pytest` to type-check collected
user-defined :mod:`pytest` fixtures with :mod:`beartype`).
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

# ....................{ HOOKS ~ fixtures                   }....................
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_fixture_setup(
    fixturedef: 'pytest.FixtureDef[object]',
    request: 'pytest.FixtureRequest',
):
    '''
    Pytest hook initializing the passed user-defined fixture.

    This hook is intentionally declared as a ``tryfirst`` **hook wrapper**
    (i.e., generator running *before* and around all other implementations of
    this hook), guaranteeing this plugin to type-check this fixture *before*
    other pytest plugins obscure this fixture. Notably, the third-party
    "pytest-asyncio" plugin declares its own non-``tryfirst`` hook wrapper for
    this hook, temporarily replacing the function underlying each asynchronous
    fixture with a synchronizer function defined by the "pytest_asyncio.plugin"
    submodule for the duration of all nested hook implementations. If this
    plugin instead inspected fixtures *inside* that replacement window, this
    plugin would erroneously identify *all* asynchronous fixtures as
    third-party fixtures (as their apparent defining file would then be
    "pytest_asyncio/plugin.py") and thus silently preserve *all* asynchronous
    fixtures as is rather than type-checking those fixtures.
    '''

    # Type-check this fixture *BEFORE* all other implementations of this hook
    # (e.g., that of "pytest-asyncio") run.
    _beartype_fixture_setup(fixturedef=fixturedef, request=request)

    # Defer to all other implementations of this hook.
    yield


def _beartype_fixture_setup(
    fixturedef: 'pytest.FixtureDef[object]',
    request: 'pytest.FixtureRequest',
) -> None:
    '''
    Wrap the passed user-defined fixture with type-checking if instructed to do
    so by the user (e.g., if passed the ``--beartype-test-fixtures``
    command-line option) *or* silently reduce to a noop otherwise.

    In the former case, this function attempts to decorate this fixture by
    :func:`beartype.beartype`. If doing so:

    * Raises a decoration-time exception, replace this fixture with a
      higher-level closure either returning or yielding (depending on fixture
      type) an instance of the plugin-specific placeholder
      :class:`pytest_beartype._bear.bearfixture.BeartypeFixtureFailure` type
      encapsulating this exception.
    * Does *not* raise a decoration-time exception, replace this fixture with a
      higher-level closure attempting to call this fixture. If doing so:

      * Raises a call-time :mod:`beartype` exception (e.g., due to a
        type-checking violation), either return or yield (depending on fixture
        type) an instance of the plugin-specific placeholder
        :class:`pytest_beartype._bear.bearfixture.BeartypeFixtureFailure` type
        encapsulating this exception.
      * Does *not* raise a call-time exception, either return or yield
        (depending on fixture type) the value returned or yielded by this
        fixture.

    When a fixture violates a type-check, the higher-level closure wrapping that
    fixture with type-checking intentionally captures that violation rather than
    permitting that violation to unwind the pytest call stack. Why? Because the
    latter approach would:

    * Erroneously mark dependent tests requiring that fixture as failing with
      the classifier ``"error"`` (indicating an internal issue in the
      :mod:`pytest` package itself) rather than the classifier ``"fail"``
      (indicating a failing test).
    * Produce unreadable tracebacks from pytest internals during pytest
      collection and fixture execution.

    For those same reasons, both pytest plugin hooks and user-defined fixtures
    should ideally *never* raise exceptions.
    '''

    # ....................{ IMPORTS ~ early                }....................
    # Defer hook-specific imports.
    from pytest_beartype._util.utiloption import is_pytest_option_bool

    # ....................{ NOOP                           }....................
    # If either...
    if (
        # *NOT* instructed by the user to type-check fixtures *OR*...
        not is_pytest_option_bool(
            config=request.config, option_name='beartype_test_fixtures') or
        # This fixture has already been type-checked...
        hasattr(fixturedef, '__beartype_fixture_wrapper')
    ):
        # Then silently reduce to a noop.
        return
    # Else, the user instructed this plugin to type-check tests *AND* this
    # fixture has yet to be type-checked.

    # ....................{ IMPORTS ~ late                 }....................
    # Defer fixture-specific imports.
    from pytest_beartype._bear.bearfixture import (
        beartype_fixture_async_generator,
        beartype_fixture_async_nongenerator,
        beartype_fixture_sync_generator,
        beartype_fixture_sync_nongenerator,
    )
    from pytest_beartype._util.utilpytsession import get_user_test_paths
    from inspect import (
        getfile,
        isasyncgenfunction,
        iscoroutinefunction,
        isgeneratorfunction,
    )
    from pathlib import Path

    # ....................{ LOCALS                         }....................
    # Low-level pure-Python function implementing this high-level fixture.
    fixture_func = fixturedef.func

    # Fully-qualified name of this fixture.
    fixture_name = fixturedef.argname

    # Absolute filename declaring this fixture.
    #
    # Pytest exposes fixtures supplied by third-party plugins to this hook as
    # well as fixtures declared by the current test suite.  The
    # "--beartype-test-fixtures" option intentionally applies only to the
    # latter: third-party plugins are external dependencies whose annotations
    # are not under the user's control and may be unsuitable for runtime
    # introspection (e.g., names imported only under "typing.TYPE_CHECKING").
    fixture_func_filename = getfile(fixture_func)

    # "Path" object encapsulating this filename.
    fixture_func_file = Path(fixture_func_filename).resolve(strict=True)

    # Frozen set of all user test paths (i.e., files and directories the user
    # explicitly instructed this pytest session to collect tests from).
    user_test_paths = get_user_test_paths(request.session)

    # "Path" object encapsulating the absolute dirname of the root directory of
    # the current pytest session (e.g., typically, the project root).
    repo_dirname = request.config.rootpath.resolve(strict=True)

    # True only if at least one user test path was strictly narrower than this
    # root directory and thus usable as a type-checking boundary.
    is_user_test_dir = False

    # Preserve this fixture as is unless declared under a user test directory.
    # In particular, this prevents this plugin from accidentally type-checking
    # fixtures supplied by other third-party "pytest" plugins.
    #
    # For each user test path...
    for user_test_path in user_test_paths:
        # Directory associated with this path. Each user test path that is a
        # file compares as its parent directory instead. Why? Because fixtures
        # are typically declared by "conftest.py" plugin files residing *NEXT
        # TO* (rather than under) the test files requiring those fixtures. A
        # user collecting tests from a single test file (e.g., "pytest
        # test_something.py") still expects the fixtures declared by the
        # adjacent "conftest.py" file to be type-checked.
        user_test_dir = (
            user_test_path if user_test_path.is_dir() else
            user_test_path.parent)

        # If this directory is the root directory itself, this directory is too
        # coarse to be a type-checking boundary. The root directory typically
        # contains a virtual environment (e.g., ".venv", ".tox") physically
        # containing third-party pytest plugins (e.g., "pytest-asyncio") whose
        # fixtures are unsuitable for type-checking (e.g., due to unresolvable
        # "typing.TYPE_CHECKING"-guarded annotations). Skip this directory.
        if user_test_dir == repo_dirname:
            continue
        # Else, this directory is strictly narrower than the root directory.
        is_user_test_dir = True

        # If this fixture is declared under this directory, type-check this
        # fixture below.
        if fixture_func_file.is_relative_to(user_test_dir):
            break
        # Else, this fixture is *NOT* declared under this directory. Continue
        # searching the remaining user test paths.
    # If this fixture is declared under *NO* user test directory...
    else:
        # If *NO* user test path was usable as a type-checking boundary (e.g.,
        # the user ran "pytest" from the project root with *NO* explicit test
        # paths or "testpaths" configuration), then *NO* fixtures whatsoever
        # will be type-checked by this plugin. Since the user explicitly
        # requested fixture type-checking, silently type-checking nothing would
        # be even more harmful than doing nothing loudly. Warn the user (only
        # once per pytest session) with an actionable suggestion.
        if not is_user_test_dir and not hasattr(
            request.config, '_pytest_beartype_warned_no_user_test_dirs'):
            # Defer branch-specific imports.
            from warnings import warn

            # Warn the user. Rise up!
            warn(
                'pytest fixture type-checking disabled, as all pytest test '
                'paths are the project root directory itself -- which '
                'typically contains third-party fixtures unsuitable for '
                'type-checking (e.g., under a ".venv" subdirectory). '
                'Consider either setting "testpaths" in your pytest '
                'configuration *OR* passing explicit test directories to the '
                '"pytest" command.'
            )

            # Prevent this warning from being emitted more than once.
            request.config._pytest_beartype_warned_no_user_test_dirs = True  # type: ignore[attr-defined]

        # Preserve this fixture as is.
        return
    # Else, this fixture is declared under at least one user test directory.

    # ....................{ TYPE-CHECK                     }....................
    # Note that tests are intentionally ordered in descending order from most to
    # least popular kinds of fixture functions. Synchronous fixtures are *MUCH*
    # more commonplace than asynchronous fixtures. Pytest itself has *NO*
    # builtin support for asynchronous fixtures, requiring users to either:
    # * Install, configure, and use the third-party "pytest-asyncio" package
    #   *OR*...
    # * Define their own custom pytest hooks (e.g., as in the "beartype_test"
    #   test suite).
    #
    # Despite this preferred ordering, note that standard fixture functions
    # (i.e., synchronous non-generator functions) can *ONLY* be detected as what
    # they're not. Which is to say, they *MUST* necessarily be tested last,
    # despite being the most common kind of fixtures. It is what it is. *sigh*

    # If this fixture function is a synchronous generator function (i.e., *NOT*
    # prefixed by the "async" keyword whose body contains one or more "yield"
    # statements), wrap this function with appropriate type-checking.
    if isgeneratorfunction(fixture_func):
        fixture_func_checked = beartype_fixture_sync_generator(
            fixture_func=fixture_func, fixture_name=fixture_name)
    # Else, this fixture function is *NOT* a synchronous generator function.
    #
    # If this fixture function is an asynchronous non-generator function (i.e.,
    # prefixed by the "async" keyword whose body contains *NO* "yield"
    # statements), wrap this function with appropriate type-checking.
    elif iscoroutinefunction(fixture_func):
        fixture_func_checked = beartype_fixture_async_nongenerator(
            fixture_func=fixture_func, fixture_name=fixture_name)
    # Else, this fixture function is *NOT* an asynchronous non-generator
    # function.
    #
    # If this fixture function is an asynchronous generator function (i.e.,
    # prefixed by the "async" keyword whose body contains one or more "yield"
    # statements), wrap this function with appropriate type-checking.
    elif isasyncgenfunction(fixture_func):
        fixture_func_checked = beartype_fixture_async_generator(
            fixture_func=fixture_func, fixture_name=fixture_name)
    # Else, this fixture function is *NOT* asynchronous. However, this function
    # is also *NOT* a synchronous generator function. By elimination, this
    # function *MUST* be a synchronous non-generator function (i.e., *NOT*
    # prefixed by the "async" keyword whose body contains *NO* "yield"
    # statements).
    #
    # In this case, wrap this function with appropriate type-checking.
    else:
        fixture_func_checked = beartype_fixture_sync_nongenerator(
            fixture_func=fixture_func, fixture_name=fixture_name)

    # ....................{ MONKEY-PATCH                   }....................
    # Replace the original fixture function with this wrapper.
    fixturedef.func = fixture_func_checked  # type: ignore[misc]

    # Mark this fixture as decorated to avoid double decoration in the future.
    fixturedef.__beartype_fixture_wrapper = True  # type: ignore[attr-defined]


def pytest_pyfunc_call(pyfuncitem: 'pytest.Function') -> bool | None:
    '''
    Expose type-checked fixture failures (as previously recorded during fixture
    collection by the :func:`.pytest_fixture_setup` hook) during each call to a
    test parametrized by that fixture.

    Pytest runs this hook during test execution, enabling this plugin to
    gracefully propagate prior fixture failures into a current test failure.
    Pytest is test-centric. Pytest is *not* fixture-centric. Pytest only has a
    means of reporting test failures. Pytest has *no* means of reporting fixture
    failures. The only means of reporting fixture failures is to coerce fixture
    failures into test failures.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer hook-specific imports.
    from pytest_beartype._util.utiloption import is_pytest_option_bool

    # ....................{ NOOP                           }....................
    # If *NOT* instructed by the user to type-check fixtures, reduce to a noop.
    # See below for further commentary on why "None" is returned. *sigh*
    if not is_pytest_option_bool(
        config=pyfuncitem.config, option_name='beartype_test_fixtures'):
        return None
    # Else, the user instructed this plugin to type-check fixtures.

    # ....................{ IMPORTS ~ late                 }....................
    # Defer fixture-specific imports.
    from pytest_beartype._bear.bearfixture import BeartypeFixtureFailure

    # ....................{ SEARCH                         }....................
    # For the fully-qualified name of each fixture requested by this test...
    #
    # This logic iteratively detects whether *ANY* such fixture previously
    # violated a beartype-specific type-check and, if so, transitively
    # propagates that failure onto this test by marking this test as a failure
    # for the same reason.
    for argname in pyfuncitem.fixturenames:
        # Fixture with this name requested by this test.
        fixture_value = pyfuncitem._request.getfixturevalue(argname)

        # If this fixture has been replaced by the plugin-specific placeholder
        # signifying fixture failure, this fixture previously violated a
        # beartype-specific type-check. In this case...
        if isinstance(fixture_value, BeartypeFixtureFailure):
            # Defer global imports to improve pytest startup performance.
            from traceback import format_tb

            failure_message_traceback = ''
            failure_traceback = getattr(
                fixture_value.fixture_exception, '__traceback__', None)

            # Include traceback in the error message for better debugging.
            if failure_traceback:
                failure_traceback_formatted = format_tb(failure_traceback)
                failure_message_traceback = (
                    f'\n{"".join(failure_traceback_formatted)}')

            # Message to be emitted as the cause of the failure of this test.
            failure_message = (
                f'Fixture "{fixture_value.fixture_name}" failed '
                f'beartype type-checking: '
                f'{fixture_value.fixture_exception}'
                f'{failure_message_traceback}'
            )

            #FIXME: How does this interact with *MULTIPLE* fixture failures?
            #Pretty sure we never tested that. Ideally, *MULTIPLE* fixture
            #failure messages should all be concatenated together into a single
            #failure message. Unsure whether the pytest.fail() API does that for
            #us (probably not) *OR* whether we need to do so manually
            #(probably). This is why testing is useful. I facepalm slowly.

            # Mark this test as a failure with this failure message.
            pytest.fail(failure_message, pytrace=False)
        # Else, this fixture has *NOT* been replaced by the plugin-specific
        # placeholder signifying fixture failure. In this case, continue
        # searching for fixture failures.

    # ....................{ RETURN                         }....................
    # Return "None", instructing pytest to call this test as it normally would.
    # Look. We don't make the rules. We just shrug our shoulders as others make
    # bad rules that make no sense whatsoever. Welcome to Planet Python.
    return None
