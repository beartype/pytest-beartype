#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
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
def pytest_fixture_setup(
    fixturedef: 'pytest.FixtureDef[object]',
    request: 'pytest.FixtureRequest',
) -> None:
    '''
    Apply beartype decoration to fixtures unless the ``--beartype-ignore-tests``
    option is passed.

    Pytest calls this plugin hook *before* fixture setup execution.

    The idea for type-checking fixtures is quite simple: we replace the fixtures
    with our sentinel if we detect them failing, so that later we can intercept
    it. The main reason for doing so, instead of just wrapping the thing into
    :func:`beartype.beartype` is such that we don't fail *inside* of pytest
    internals (which produces unreadable error logs), but so that we can fail
    outside of pytest internals, leading to a decent error log and the test
    classified as "fail" instead of "error" (which usually indicates an internal
    pytest error, which is wrong in this case).
    '''

    # ....................{ IMPORTS ~ early                }....................
    # Defer hook-specific imports.
    from pytest_beartype._util.utilopt import is_pytest_option_bool

    # ....................{ NOOP                           }....................
    # If either...
    if (
        # *NOT* instructed by the user to type-check fixtures *OR*...
        not is_pytest_option_bool(
            config=request.config, option_name='beartype_fixtures') or
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
        beartype_fixture_async,
        beartype_fixture_sync_generator,
        beartype_fixture_sync_nongenerator,
    )
    from inspect import (
        isasyncgenfunction,
        iscoroutinefunction,
        isgeneratorfunction,
    )

    # ....................{ LOCALS                         }....................
    # Low-level pure-Python function implementing this high-level fixture.
    fixture_func = fixturedef.func

    # Fully-qualified name of this fixture.
    fixture_name = fixturedef.argname

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

    #FIXME: Are we unit testing any of this? Probably... *NOT*. *sigh*
    # If this fixture function is a synchronous generator function (i.e., *NOT*
    # prefixed by the "async" keyword whose body contains one or more "yield"
    # statements), wrap this function with appropriate type-checking.
    if isgeneratorfunction(fixture_func):
        fixture_func_checked = beartype_fixture_sync_generator(
            fixture_func=fixture_func, fixture_name=fixture_name)
    # Else, this fixture function is *NOT* a synchronous generator function.
    #
    # If this fixture function is either...
    elif (
        # An asynchronous non-generator function (i.e., prefixed by the "async"
        # keyword whose body contains *NO* "yield" statements) *OR*...
        iscoroutinefunction(fixture_func) or
        # An asynchronous generator function (i.e., prefixed by the "async"
        # keyword whose body contains one or more "yield" statements).
        isasyncgenfunction(fixture_func)
    ):
        # Then function is asynchronous. In this case, wrap this asynchronous
        # function with appropriate type-checking.
        fixture_func_checked = beartype_fixture_async(
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
    from pytest_beartype._util.utilopt import is_pytest_option_bool

    # ....................{ NOOP                           }....................
    # If *NOT* instructed by the user to type-check fixtures, reduce to a noop.
    # See below for further commentary on why "None" is returned. *sigh*
    if not is_pytest_option_bool(
        config=pyfuncitem.config, option_name='beartype_fixtures'):
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
