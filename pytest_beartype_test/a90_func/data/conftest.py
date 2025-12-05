#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **integration test fixture data** (i.e., fixture functions to be
tested by integration tests defined elsewhere) submodule.
'''

# ....................{ TODO                               }....................
#FIXME: Across *ALL* hook functions defined by this plugin, we need to force our
#plugin to be ordered *BEFORE* all other hook functions. There exist two ways to
#accomplish this. The first is what we'll do first... *OH*. Not good.
#"pytest-asyncio" is *SUPER*-hostile to other pytest hooks. They forcefully
#insist their hooks should always be run first. Well, isn't that special. For
#some of these hooks, we can avoid conflicts by one-upping "pytest-asyncio" by
#decorating *OUR* hooks as follows:
#    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
#    def pytest_...
#
#Note, however, that we'll need to refactor our hooks to be generators.
#Annoying, but trivial.
#
#Also, this *STILL* might not be enough. Internally, pytest currently orders
#pytest plugins according to a LIFO (Last-In, First-Out) stack of such plugins.
#Critically, this means that:
#* The *FIRST* pytest plugin that a user registers is the *LAST* pytest plugin
#  that pytest itself will invoke hooks for. *lol*
#* The *LAST* pytest plugin that a user registers is the *FIRST* pytest plugin
#  that pytest itself will invoke hooks for. *lol*
#
#Clearly, this means that "pytest-beartype" should be listed and thus registered
#*LAST* in orderings.
#
#Responsibility for ordering hooks thus ultimately lies with our userbase, at
#the moment. Since we genuinely do want "pytest-beartype" to assume precedence
#over literally *EVERYTHING*, we'll need to revise our documentation to
#encourage users to explicitly order plugins. Confusingly, pytest provides
#*MANY* different means of doing so. See official documentation at:
#    https://docs.pytest.org/en/stable/how-to/writing_plugins.html#plugin-discovery-order-at-tool-startup
#
#One such way (probably the sanest, frankly) is for users to:
#* Defining a top-level "conftest.py" pytest plugin in their root project
#  directory, which itself defines a "pytest_plugins" setting whose value should
#  resemble:
#      pytest_plugins = (
#          ...,
#          'asyncio',  # <-- should not be *LAST*, because pytest.
#          'beartype',  # <-- should be *LAST*, because pytest. wat u goin do?
#      )
#
#Alternately, users can pass "-p asyncio -p beartype". Maybe. No idea, honestly.
#Regardless, 'beartype' should *ALWAYS* be last.
#
#See also:
#* Official documentation:
#    https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html#hook-function-ordering-call-example
#* Upstream "pluggy" open issue. Since pytest internally uses pluggy to order
#  and manage both hooks and pytest plugins, this issue will need to be
#  resolved before pytest officially supports fine-grained pytest plugin
#  ordering (presumably through a topological sort of some kind).
#  https://github.com/pytest-dev/pluggy/issues/51
#* Upstream "pytest" open issue, similar to above:
#  https://github.com/pytest-dev/pytest/issues/7484
#FIXME: Actually, let's test whether this plugin currently behaves as expected
#with "pytest-asyncio" first in both orders: e.g.,
#* "-p asyncio -p beartype".
#* "-p beartype -p asyncio".
#
#It's unlikely, but everything *MIGHT* already work "out-of-the-box" without us
#needing to actually do anything. Unlikely. But possible.

#FIXME: Decorate asynchronous fixtures by @pytest_asyncio.fixture. Look. Just do
#it. We can't trivially reproduce that. We accept what we cannot change. *sigh*

#FIXME: Compact and disambiguate these super-long fixture names like
#* fixture_sync_nongenerator_bad() to fixture_sync_nongen_call_bad().
#* fixture_sync_generator_bad() to fixture_sync_gen_call_bad().

#FIXME: All of this is *STILL* insufficient. Why? Because we're failing to test
#decoration-time exceptions. For each of the four fundamental kinds of fixtures,
#we'll need to:
#* Define a new "bad" fixture intentionally violating PEP compliance with
#  invalid type hints detected at decoration-time: e.g.,
#    @fixture
#    def fixture_sync_nongen_decor_bad() -> 'oh noes this is guaranteed to fail':
#        '''
#        Synchronous non-generator fixture annotated by an incorrect return hint.
#        '''
#
#        # Return an object violating the return hint annotating this fixture.
#        return 'O monstrous forms! O effigies of pain!'

#FIXME: Define *AND* test in the "test_pytester_option_beartype_fixtures" *AND*
#"test_pytester_option_beartype_tests" submodules:
#* A coroutine (asynchronous non-generator) fixture. This is non-trivial. Why?
#  Because testing this requires asynchronous test support, which then requires
#  we copy-paste from the @beartype test suite. Feasible, certainly. We must do
#  this, certainly. Yet, this takes time. Time is scarce! My face is tired.
#* An asynchronous non-generator fixture. Once coroutine support has been nailed
#  down, this suddenly becomes trivial. Yay! Something should be easy for once!

# ....................{ IMPORTS                            }....................
#FIXME: *CURRENTLY UNUSED.* "pytester" fails to support package structures,
#rendering this unimportable. Once we migrate away from "pytester", though, this
#suddenly becomes usable and thus useful. Let's preserve this for now. *sigh*
# from ._fixture.fixsync import (
#     fixture_sync_nongenerator,
#     fixture_sync_nongenerator_bad,
#     fixture_sync_nongenerator_needs_fixture,
#     fixture_sync_nongenerator_needs_fixtures_bad,
#     fixture_sync_nongenerator_bad_needs_fixtures,
#     fixture_sync_generator,
#     fixture_sync_generator_bad,
#     fixture_sync_generator_needs_fixture,
#     fixture_sync_generator_needs_fixtures_bad,
#     fixture_sync_generator_bad_needs_fixtures,
# )

# ....................{ IMPORTS                            }....................
from asyncio import sleep
from collections.abc import (
    AsyncIterable,
    Iterable,
)
from pytest import fixture as fixture_sync
from pytest_asyncio import fixture as fixture_async

# ....................{ FIXTURES ~ sync : non-gen : root   }....................
# Synchronous non-generator root fixtures requiring *NO* other fixtures.

@fixture_sync
def fixture_sync_nongenerator() -> str:
    '''
    Synchronous non-generator fixture annotated by a correct return hint.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return 'Through bowers of fragrant and enwreathed light,'


@fixture_sync
def fixture_sync_nongenerator_bad() -> int:
    '''
    Synchronous non-generator fixture annotated by an incorrect return hint.
    '''

    # Return an object violating the return hint annotating this fixture.
    return 'O monstrous forms! O effigies of pain!'

# ....................{ FIXTURES ~ sync : non-gen : leaf   }....................
# Synchronous non-generator leaf fixtures requiring one or more other such
# fixtures.

@fixture_sync
def fixture_sync_nongenerator_needs_fixture(
    fixture_sync_nongenerator: str) -> str:
    '''
    Synchronous non-generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return fixture_sync_nongenerator


@fixture_sync
def fixture_sync_nongenerator_needs_fixtures_bad(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_sync_nongenerator: str,
    fixture_sync_nongenerator_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_sync_nongenerator_bad,
) -> str:
    '''
    Synchronous non-generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by an incorrect return hint.
    '''

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return 'From stately nave to nave, from vault to vault,'


@fixture_sync
def fixture_sync_nongenerator_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_sync_nongenerator: int,
    fixture_sync_nongenerator_needs_fixture: int,
) -> str:
    '''
    Synchronous non-generator fixture annotated by a correct return hint but
    requiring two or more other such fixtures all annotated by different
    parameter hints from the return hints annotating those fixtures.

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return "O lank-ear'd Phantoms of black-weeded pools!"

# ....................{ FIXTURES ~ sync : gen : root       }....................
# Synchronous generator root fixtures requiring *NO* other fixtures.

@fixture_sync
def fixture_sync_generator() -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct return hint.
    '''

    # Yield an object satisfying the return hint annotating this fixture.
    yield 'Why do I know ye? why have I seen ye? why'


@fixture_sync
def fixture_sync_generator_bad() -> Iterable[int]:
    '''
    Synchronous generator fixture annotated by an incorrect return hint.
    '''

    # Yield an object violating the return hint annotating this fixture.
    yield 'Is my eternal essence thus distraught'

# ....................{ FIXTURES ~ sync : non-gen : leaf   }....................
# Synchronous generator leaf fixtures requiring one or more other such fixtures.

@fixture_sync
def fixture_sync_generator_needs_fixture(
    fixture_sync_generator: str) -> Iterable[str]:
    '''
    Synchronous generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Yield an object satisfying the return hint annotating this fixture.
    yield fixture_sync_generator


@fixture_sync
def fixture_sync_generator_needs_fixtures_bad(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_sync_generator: str,
    fixture_sync_generator_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_sync_generator_bad,
) -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by an incorrect return hint.
    '''

    # Yield an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'To see and to behold these horrors new?'


@fixture_sync
def fixture_sync_generator_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_sync_generator: int,
    fixture_sync_generator_needs_fixture: int,
) -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct return hint but
    requiring two or more other such fixtures all annotated by different
    parameter hints from the return hints annotating those fixtures.

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Yield an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'Saturn is fallen, am I too to fall?'

# ....................{ FIXTURES ~ async : non-gen : root  }....................
# Asynchronous non-generator root fixtures requiring *NO* other fixtures.

@fixture_async
async def fixture_async_nongenerator() -> str:
    '''
    Asynchronous non-generator fixture annotated by a correct return hint.
    '''

    # Silently reduce to an asynchronous noop. Asynchronous callables are
    # required to call the "await" keyword at least once. Since the object
    # returned below is synchronous and thus *CANNOT* be asynchronously awaited,
    # we have *NO* recourse but to asynchronously await a minimal-cost
    # awaitable. Aaaaaaand...
    #
    # This is why the "asyncio" API is Python's most hated. We sigh!
    await sleep(0)

    # Return an object satisfying the return hint annotating this fixture.
    return 'Through bowers of fragrant and enwreathed light,'


@fixture_async
async def fixture_async_nongenerator_bad() -> int:
    '''
    Asynchronous non-generator fixture annotated by an incorrect return hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object violating the return hint annotating this fixture.
    return 'O monstrous forms! O effigies of pain!'

# ....................{ FIXTURES ~ async : non-gen : leaf  }....................
# Asynchronous non-generator leaf fixtures requiring one or more other such
# fixtures.

@fixture_async
async def fixture_async_nongenerator_needs_fixture(
    fixture_async_nongenerator: str) -> str:
    '''
    Asynchronous non-generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object satisfying the return hint annotating this fixture.
    return fixture_async_nongenerator


@fixture_async
async def fixture_async_nongenerator_needs_fixtures_bad(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_async_nongenerator: str,
    fixture_async_nongenerator_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_async_nongenerator_bad,
) -> str:
    '''
    Asynchronous non-generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by an incorrect return hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return 'From stately nave to nave, from vault to vault,'


@fixture_async
async def fixture_async_nongenerator_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_async_nongenerator: int,
    fixture_async_nongenerator_needs_fixture: int,
) -> str:
    '''
    Asynchronous non-generator fixture annotated by a correct return hint but
    requiring two or more other such fixtures all annotated by different
    parameter hints from the return hints annotating those fixtures.

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return "O lank-ear'd Phantoms of black-weeded pools!"

# ....................{ FIXTURES ~ async : gen : root      }....................
# Asynchronous generator root fixtures requiring *NO* other fixtures.

@fixture_async
async def fixture_async_generator() -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct return hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the return hint annotating this fixture.
    yield 'Why do I know ye? why have I seen ye? why'


@fixture_async
async def fixture_async_generator_bad() -> AsyncIterable[int]:
    '''
    Asynchronous generator fixture annotated by an incorrect return hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object violating the return hint annotating this fixture.
    yield 'Is my eternal essence thus distraught'

# ....................{ FIXTURES ~ async : non-gen : leaf  }....................
# Asynchronous generator leaf fixtures requiring one or more other such fixtures.

@fixture_async
async def fixture_async_generator_needs_fixture(
    fixture_async_generator: str) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the return hint annotating this fixture.
    yield fixture_async_generator


@fixture_async
async def fixture_async_generator_needs_fixtures_bad(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_async_generator: str,
    fixture_async_generator_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_async_generator_bad,
) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by an incorrect return hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'To see and to behold these horrors new?'


@fixture_async
async def fixture_async_generator_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_async_generator: int,
    fixture_async_generator_needs_fixture: int,
) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct return hint but
    requiring two or more other such fixtures all annotated by different
    parameter hints from the return hints annotating those fixtures.

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'Saturn is fallen, am I too to fall?'
