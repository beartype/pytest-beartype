#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **integration test fixture data** (i.e., fixture functions to be
tested by integration tests defined elsewhere) submodule.
'''

# ....................{ TODO                               }....................
#FIXME: *ALL* asynchronous fixtures need to contain additional calls to
#asyncio.sleep(0). It is what it is.

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
from collections.abc import (
    AsyncIterable,
    Iterable,
)
from pytest import fixture

# ....................{ FIXTURES ~ sync : non-gen : root   }....................
# Synchronous non-generator root fixtures requiring *NO* other fixtures.

@fixture
def fixture_sync_nongenerator() -> str:
    '''
    Synchronous non-generator fixture annotated by a correct return hint.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return 'Through bowers of fragrant and enwreathed light,'


@fixture
def fixture_sync_nongenerator_bad() -> int:
    '''
    Synchronous non-generator fixture annotated by an incorrect return hint.
    '''

    # Return an object violating the return hint annotating this fixture.
    return 'O monstrous forms! O effigies of pain!'

# ....................{ FIXTURES ~ sync : non-gen : leaf   }....................
# Synchronous non-generator leaf fixtures requiring one or more other such
# fixtures.

@fixture
def fixture_sync_nongenerator_needs_fixture(
    fixture_sync_nongenerator: str) -> str:
    '''
    Synchronous non-generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return fixture_sync_nongenerator


@fixture
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


@fixture
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

@fixture
def fixture_sync_generator() -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct return hint.
    '''

    # Yield an object satisfying the return hint annotating this fixture.
    yield 'Why do I know ye? why have I seen ye? why'


@fixture
def fixture_sync_generator_bad() -> Iterable[int]:
    '''
    Synchronous generator fixture annotated by an incorrect return hint.
    '''

    # Yield an object violating the return hint annotating this fixture.
    yield 'Is my eternal essence thus distraught'

# ....................{ FIXTURES ~ sync : non-gen : leaf   }....................
# Synchronous generator leaf fixtures requiring one or more other such fixtures.

@fixture
def fixture_sync_generator_needs_fixture(
    fixture_sync_generator: str) -> Iterable[str]:
    '''
    Synchronous generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Yield an object satisfying the return hint annotating this fixture.
    yield fixture_sync_generator


@fixture
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


@fixture
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

@fixture
async def fixture_async_nongenerator() -> str:
    '''
    Asynchronous non-generator fixture annotated by a correct return hint.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return 'Through bowers of fragrant and enwreathed light,'


@fixture
async def fixture_async_nongenerator_bad() -> int:
    '''
    Asynchronous non-generator fixture annotated by an incorrect return hint.
    '''

    # Return an object violating the return hint annotating this fixture.
    return 'O monstrous forms! O effigies of pain!'

# ....................{ FIXTURES ~ async : non-gen : leaf  }....................
# Asynchronous non-generator leaf fixtures requiring one or more other such
# fixtures.

@fixture
async def fixture_async_nongenerator_needs_fixture(
    fixture_async_nongenerator: str) -> str:
    '''
    Asynchronous non-generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return fixture_async_nongenerator


@fixture
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

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return 'From stately nave to nave, from vault to vault,'


@fixture
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

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return "O lank-ear'd Phantoms of black-weeded pools!"

# ....................{ FIXTURES ~ async : gen : root      }....................
# Asynchronous generator root fixtures requiring *NO* other fixtures.

@fixture
async def fixture_async_generator() -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct return hint.
    '''

    # Yield an object satisfying the return hint annotating this fixture.
    yield 'Why do I know ye? why have I seen ye? why'


@fixture
async def fixture_async_generator_bad() -> AsyncIterable[int]:
    '''
    Asynchronous generator fixture annotated by an incorrect return hint.
    '''

    # Yield an object violating the return hint annotating this fixture.
    yield 'Is my eternal essence thus distraught'

# ....................{ FIXTURES ~ async : non-gen : leaf  }....................
# Asynchronous generator leaf fixtures requiring one or more other such fixtures.

@fixture
async def fixture_async_generator_needs_fixture(
    fixture_async_generator: str) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Yield an object satisfying the return hint annotating this fixture.
    yield fixture_async_generator


@fixture
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

    # Yield an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'To see and to behold these horrors new?'


@fixture
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

    # Yield an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'Saturn is fallen, am I too to fall?'
