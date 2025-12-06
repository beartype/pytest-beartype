#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **test integration test** (i.e., integration tests testing that this
plugin passed the ``--beartype-tests`` option correctly type-checks tests)
submodule.

This submodule is *not* intended to be directly collected by the root
:mod:`pytest` process. This submodule is *only* collected by the leaf
:mod:`pytest` subprocess implicitly spawned by the :mod:`pytest.pytester`
fixture required by the parent ``test_pytester_option_beartype_tests`` test.
'''

# ....................{ IMPORTS                            }....................
from asyncio import sleep
import pytest

# ....................{ TESTS ~ sync                       }....................
# Note that pytest itself already validates tests to return "None" at runtime.
# If any test returns an object other than "None", pytest emits the following
# non-fatal warning (which our pytest configuration coerces into a fatal error):
#     /usr/lib/python3.13/site-packages/_pytest/python.py:161:
#     PytestReturnNotNoneWarning: Test functions should return None, but
#     test_pytester_option_beartype_tests.py::test_pytester_option_beartype_tests_sync
#     returned <class 'str'>.
#         Did you mean to use `assert` instead of `return`? See
#         https://docs.pytest.org/en/stable/how-to/assert.html#return-not-none
#         for more information.
#
# Pytest understandably provides *NO* means of disabling this functionality.
# Ergo, tests below *CANNOT* test whether a test returns "None" or not.

def test_pytester_option_beartype_tests_sync_bad() -> None:
    '''
    Synchronous test internally defining a synchronous closure intentionally
    annotated by an incorrect return hint.
    '''

    #FIXME: *TYPE-CHECK THIS.* Currently, @beartype doesn't. But @beartype
    #definitely could and arguably should. How? This plugin should (probably)
    #register a special-purpose import hook. Maybe. The issue is that this hook
    #will need to be modified at a low-level from the existing import hook
    #machinery... *WAIT*. Definitely not doing that.
    #
    #Instead, let's define a new
    #"BeartypeConf(claw_is_ignore_pytest_tests_fixtures: bool = False)" option.
    #When passed a configuration enabling this option, the
    #beartype.claw.beartype_package() import hook should then instruct our
    #low-level AST transformation to *NOT* decorate with the @beartype decorator
    #any global function in any submodule hooked by that hook if that global
    #function satisfies either of the following two constraints:
    #* That global function's name is prefixed by "test_". Does this suffice,
    #  though? Does pytest allow this prefix to be configured by users? No idea.
    #* That global function is decorated by @pytest.fixture. This one should be
    #  unambiguous. There's only one @pytest.fixture decorator. *shrug*
    #
    #Once that new option exists, this plugin should then call:
    #    from beartype import BeartypeConf
    #    from beartype.claw import beartype_package
    #    beartype_package(user_test_suite, conf=BeartypeConf(
    #        claw_is_ignore_pytest_tests_fixtures=True))
    def to_this_result(o_dreams_of_day_and_night: str) -> int:
        '''
        Synchronous closure intentionally annotated by an incorrect return hint.

        Currently, this plugin does *not* type-check closures embedded in tests.
        Doing so should be feasible, but is left as an exercise to the reader.
        '''

        return o_dreams_of_day_and_night

    # Arbitrary string to be passed to the above closure.
    o_dreams_of_day = 'To this result: "O dreams of day and night!"'

    # Return an object violating the return hint annotating this test by
    # returning the value returned by calling the above closure.
    assert to_this_result(o_dreams_of_day) == o_dreams_of_day

# ....................{ TESTS ~ sync : fixture : non-gen   }....................
def test_pytester_option_beartype_tests_sync_needs_fixtures_sync_nongen(
    fixture_sync_nongen: str,
    fixture_sync_nongen_needs_fixture: str,
) -> None:
    '''
    Synchronous test requiring one or more synchronous non-generator fixtures
    annotated by the same parameter hints as the return hints annotating those
    fixtures.
    '''

    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_tests_sync_bad_needs_fixtures_sync_nongen(
    # Parent fixture that is correctly annotated.
    fixture_sync_nongen: str,

    # Parent fixture that is intentionally incorrectly annotated.
    fixture_sync_nongen_needs_fixture: int,
) -> None:
    '''
    Synchronous test requiring one or more synchronous non-generator fixtures
    annotated by different parameter hints from the return hints annotating
    those fixtures.
    '''

    pass

# ....................{ TESTS ~ sync : fixture : gen       }....................
def test_pytester_option_beartype_tests_sync_needs_fixtures_sync_gen(
    fixture_sync_gen: str,
    fixture_sync_gen_needs_fixture: str,
) -> None:
    '''
    Synchronous test requiring one or more synchronous generator fixtures
    annotated by the same parameter hints as the return hints annotating those
    fixtures.
    '''

    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_tests_sync_bad_needs_fixtures_sync_gen(
    # Parent fixture that is correctly annotated.
    fixture_sync_gen: str,

    # Parent fixture that is intentionally incorrectly annotated.
    fixture_sync_gen_needs_fixture: int,
) -> None:
    '''
    Synchronous test requiring one or more synchronous generator fixtures
    annotated by different parameter hints from the return hints annotating
    those fixtures.
    '''

    pass

#FIXME: Uncomment *AFTER* we successfully enable the "pytest-asyncio" plugin for
#this subprocess. The standard "pytester" plugin appears to *NOT* support this.
#Ergo, we'll now need to manually pursue subprocess forking. We sigh.
# # ....................{ TESTS ~ async                       }....................
# async def test_pytester_option_beartype_tests_async_bad() -> None:
#     '''
#     Asynchronous test internally defining a asynchronous closure intentionally
#     annotated by an incorrect return hint.
#     '''
#
#     #FIXME: *TYPE-CHECK THIS.* See above.
#     async def to_this_result(o_dreams_of_day_and_night: str) -> int:
#         '''
#         Asynchronous closure intentionally annotated by an incorrect return
#         hint.
#
#         Currently, this plugin does *not* type-check closures embedded in tests.
#         Doing so should be feasible, but is left as an exercise to the reader.
#         '''
#
#         # Silently reduce to an asynchronous noop. Asynchronous callables are
#         # required to call the "await" keyword at least once. Since the object
#         # returned below is synchronous and thus *CANNOT* be asynchronously
#         # awaited, we have *NO* recourse but to asynchronously await a
#         # minimal-cost awaitable. Aaaaaaand...
#         #
#         # This is why the "asyncio" API is Python's most hated. We sigh!
#         await sleep(0)
#
#         return o_dreams_of_day_and_night
#
#     # Arbitrary string to be passed to the above closure.
#     o_dreams_of_day = 'To this result: "O dreams of day and night!"'
#
#     # Return an object violating the return hint annotating this test by
#     # returning the value returned by calling the above closure.
#     assert await to_this_result(o_dreams_of_day) == o_dreams_of_day
#
# # ....................{ TESTS ~ async : fixture : non-gen   }....................
# async def test_pytester_option_beartype_tests_async_needs_fixtures_async_nongen(
#     fixture_async_nongen: str,
#     fixture_async_nongen_needs_fixture: str,
# ) -> None:
#     '''
#     Asynchronous test requiring one or more asynchronous non-generator fixtures
#     annotated by the same parameter hints as the return hints annotating those
#     fixtures.
#     '''
#
#     # Silently reduce to an asynchronous noop. See above.
#     await sleep(0)
#
#
# @pytest.mark.xfail(strict=True)
# async def test_pytester_option_beartype_tests_async_bad_needs_fixtures_async_nongen(
#     # Parent fixture that is correctly annotated.
#     fixture_async_nongen: str,
#
#     # Parent fixture that is intentionally incorrectly annotated.
#     fixture_async_nongen_needs_fixture: int,
# ) -> None:
#     '''
#     Asynchronous test requiring one or more asynchronous non-generator fixtures
#     annotated by different parameter hints from the return hints annotating
#     those fixtures.
#     '''
#
#     # Silently reduce to an asynchronous noop. See above.
#     await sleep(0)
#
# # ....................{ TESTS ~ async : fixture : gen       }....................
# async def test_pytester_option_beartype_tests_async_needs_fixtures_async_gen(
#     fixture_async_gen: str,
#     fixture_async_gen_needs_fixture: str,
# ) -> None:
#     '''
#     Asynchronous test requiring one or more asynchronous generator fixtures
#     annotated by the same parameter hints as the return hints annotating those
#     fixtures.
#     '''
#
#     # Silently reduce to an asynchronous noop. See above.
#     await sleep(0)
#
#
# @pytest.mark.xfail(strict=True)
# async def test_pytester_option_beartype_tests_async_bad_needs_fixtures_async_gen(
#     # Parent fixture that is correctly annotated.
#     fixture_async_gen: str,
#
#     # Parent fixture that is intentionally incorrectly annotated.
#     fixture_async_gen_needs_fixture: int,
# ) -> None:
#     '''
#     Asynchronous test requiring one or more asynchronous generator fixtures
#     annotated by different parameter hints from the return hints annotating
#     those fixtures.
#     '''
#
#     # Silently reduce to an asynchronous noop. See above.
#     await sleep(0)
