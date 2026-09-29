#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **asynchronous fixtures** (i.e., asynchronous fixture functions to be
tested by tests defined elsewhere) submodule.
'''

# ....................{ IMPORTS                            }....................
from asyncio import sleep
from collections.abc import AsyncIterable
from pytest_asyncio import fixture as fixture_async

# ....................{ FIXTURES ~ async : non-gen : root  }....................
# Asynchronous non-generator root fixtures requiring *NO* other fixtures.

@fixture_async
async def fixture_async_nongen() -> str:
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
async def fixture_async_nongen_bad_call() -> int:
    '''
    Asynchronous non-generator fixture annotated by a PEP-compliant return hint
    violating the returned value and thus inducing a call-time violation.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object violating the return hint annotating this fixture.
    return 'O monstrous forms! O effigies of pain!'


@fixture_async
async def fixture_async_nongen_bad_decor() -> (
    'Am I to leave this haven of my rest,'):
    '''
    Asynchronous non-generator fixture annotated by a PEP-noncompliant return
    hint inducing a decoration-time exception.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an arbitrary object.
    return 'This calm luxuriance of blissful light,'

# ....................{ FIXTURES ~ async : non-gen : leaf  }....................
# Asynchronous non-generator leaf fixtures requiring one or more other such
# fixtures.

@fixture_async
async def fixture_async_nongen_needs_fixture(fixture_async_nongen: str) -> str:
    '''
    Asynchronous non-generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object satisfying the return hint annotating this fixture.
    return fixture_async_nongen


@fixture_async
async def fixture_async_nongen_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_async_nongen: int,
    fixture_async_nongen_needs_fixture: int,
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


@fixture_async
async def fixture_async_nongen_needs_fixtures_bad_call(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_async_nongen: str,
    fixture_async_nongen_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_async_nongen_bad_call,
) -> str:
    '''
    Asynchronous non-generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by a PEP-compliant return hint violating the returned value and
    thus inducing a call-time violation.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return 'From stately nave to nave, from vault to vault,'


@fixture_async
async def fixture_async_nongen_needs_fixtures_bad_decor(
    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_async_nongen_bad_decor,

    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_async_nongen: str,
    fixture_async_nongen_needs_fixture: str,
) -> str:
    '''
    Asynchronous non-generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by a PEP-noncompliant return hint inducing a decoration-time
    exception.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return 'This cradle of my glory, this soft clime,'

# ....................{ FIXTURES ~ async : gen : root      }....................
# Asynchronous generator root fixtures requiring *NO* other fixtures.

@fixture_async
async def fixture_async_gen() -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct yield hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the yield hint annotating this fixture.
    yield 'Why do I know ye? why have I seen ye? why'


@fixture_async
async def fixture_async_gen_bad_call() -> AsyncIterable[int]:
    '''
    Asynchronous generator fixture annotated by an incorrect yield hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object violating the yield hint annotating this fixture.
    yield 'Is my eternal essence thus distraught'


@fixture_async
async def fixture_async_gen_bad_decor() -> (
    'These crystalline pavilions, and pure fanes,'):
    '''
    Asynchronous generator fixture annotated by a PEP-noncompliant yield hint
    inducing a decoration-time exception.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an arbitrary object.
    yield 'Of all my lucent empire? It is left'

# ....................{ FIXTURES ~ async : gen : leaf      }....................
# Asynchronous generator leaf fixtures requiring one or more other such
# fixtures.

@fixture_async
async def fixture_async_gen_needs_fixture(
    fixture_async_gen: str) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture requiring another such fixture annotated
    by the same parameter hint as the yield hint annotating the latter fixture.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the yield hint annotating this fixture.
    yield fixture_async_gen


@fixture_async
async def fixture_async_gen_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_async_gen: int,
    fixture_async_gen_needs_fixture: int,
) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct yield hint but
    requiring two or more other such fixtures all annotated by different
    parameter hints from the yield hints annotating those fixtures.

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the yield hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'Saturn is fallen, am I too to fall?'


@fixture_async
async def fixture_async_gen_needs_fixtures_bad_call(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_async_gen: str,
    fixture_async_gen_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_async_gen_bad_call,
) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct yield hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by an incorrect yield hint.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the yield hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'To see and to behold these horrors new?'


@fixture_async
async def fixture_async_gen_needs_fixtures_bad_decor(
    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_async_gen_bad_decor,

    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_async_gen: str,
    fixture_async_gen_needs_fixture: str,
) -> AsyncIterable[str]:
    '''
    Asynchronous generator fixture annotated by a correct yield hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by a PEP-noncompliant yield hint inducing a decoration-time
    exception.
    '''

    # Silently reduce to an asynchronous noop. See above.
    await sleep(0)

    # Yield an object satisfying the yield hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'Deserted, void, nor any haunt of mine.'
