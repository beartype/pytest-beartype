#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **asynchronous fixtures** (i.e., asynchronous fixture functions to be
tested by tests defined elsewhere) submodule.
'''

# ....................{ IMPORTS                            }....................
from collections.abc import Iterable
from pytest import fixture as fixture_sync

# ....................{ FIXTURES ~ sync : non-gen : root   }....................
# Synchronous non-generator root fixtures requiring *NO* other fixtures.

@fixture_sync
def fixture_sync_nongen() -> str:
    '''
    Synchronous non-generator fixture annotated by a correct return hint.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return 'Through bowers of fragrant and enwreathed light,'


@fixture_sync
def fixture_sync_nongen_bad_call() -> int:
    '''
    Synchronous non-generator fixture annotated by a PEP-compliant return hint
    violating the returned value and thus inducing a call-time violation.
    '''

    # Return an object violating the return hint annotating this fixture.
    return 'O monstrous forms! O effigies of pain!'


@fixture_sync
def fixture_sync_nongen_bad_decor() -> 'Am I to leave this haven of my rest,':
    '''
    Synchronous non-generator fixture annotated by a PEP-noncompliant return
    hint inducing a decoration-time exception.
    '''

    # Return an arbitrary object.
    return 'This calm luxuriance of blissful light,'

# ....................{ FIXTURES ~ sync : non-gen : leaf   }....................
# Synchronous non-generator leaf fixtures requiring one or more other such
# fixtures.

@fixture_sync
def fixture_sync_nongen_needs_fixture(fixture_sync_nongen: str) -> str:
    '''
    Synchronous non-generator fixture requiring another such fixture annotated
    by the same parameter hint as the return hint annotating the latter fixture.
    '''

    # Return an object satisfying the return hint annotating this fixture.
    return fixture_sync_nongen


@fixture_sync
def fixture_sync_nongen_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_sync_nongen: int,
    fixture_sync_nongen_needs_fixture: int,
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


@fixture_sync
def fixture_sync_nongen_needs_fixtures_bad_call(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_sync_nongen: str,
    fixture_sync_nongen_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_sync_nongen_bad_call,
) -> str:
    '''
    Synchronous non-generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by a PEP-compliant return hint violating the returned value and
    thus inducing a call-time violation.
    '''

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return 'From stately nave to nave, from vault to vault,'


@fixture_sync
def fixture_sync_nongen_needs_fixtures_bad_decor(
    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_sync_nongen_bad_decor,

    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_sync_nongen: str,
    fixture_sync_nongen_needs_fixture: str,
) -> str:
    '''
    Synchronous non-generator fixture annotated by a correct return hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by a PEP-noncompliant return hint inducing a decoration-time
    exception.
    '''

    # Return an object satisfying the return hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    return 'This cradle of my glory, this soft clime,'

# ....................{ FIXTURES ~ sync : gen : root       }....................
# Synchronous generator root fixtures requiring *NO* other fixtures.

@fixture_sync
def fixture_sync_gen() -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct yield hint.
    '''

    # Yield an object satisfying the yield hint annotating this fixture.
    yield 'Why do I know ye? why have I seen ye? why'


@fixture_sync
def fixture_sync_gen_bad_call() -> Iterable[int]:
    '''
    Synchronous generator fixture annotated by a PEP-compliant yield hint
    violating the yielded value and thus inducing a call-time violation.
    '''

    # Yield an object violating the yield hint annotating this fixture.
    yield 'Is my eternal essence thus distraught'


@fixture_sync
def fixture_sync_gen_bad_decor() -> (
    'These crystalline pavilions, and pure fanes,'):
    '''
    Synchronous generator fixture annotated by a PEP-noncompliant yield hint
    inducing a decoration-time exception.
    '''

    # Yield an arbitrary object.
    yield 'Of all my lucent empire? It is left'

# ....................{ FIXTURES ~ sync : gen : leaf       }....................
# Synchronous generator leaf fixtures requiring one or more other such fixtures.

@fixture_sync
def fixture_sync_gen_needs_fixture(
    fixture_sync_gen: str) -> Iterable[str]:
    '''
    Synchronous generator fixture requiring another such fixture annotated
    by the same parameter hint as the yield hint annotating the latter fixture.
    '''

    # Yield an object satisfying the yield hint annotating this fixture.
    yield fixture_sync_gen


@fixture_sync
def fixture_sync_gen_bad_needs_fixtures(
    # Two or more parent fixtures that are *ALL* incorrectly annotated.
    fixture_sync_gen: int,
    fixture_sync_gen_needs_fixture: int,
) -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct yield hint but
    requiring two or more other such fixtures all annotated by different
    parameter hints from the yield hints annotating those fixtures.

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Yield an object satisfying the yield hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'Saturn is fallen, am I too to fall?'


@fixture_sync
def fixture_sync_gen_needs_fixtures_bad_call(
    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_sync_gen: str,
    fixture_sync_gen_needs_fixture: str,

    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_sync_gen_bad_call,
) -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct yield hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by a PEP-compliant yield hint violating the yielded value and
    thus inducing a call-time violation.
    '''

    # Yield an object satisfying the yield hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'To see and to behold these horrors new?'


@fixture_sync
def fixture_sync_gen_needs_fixtures_bad_decor(
    # This parent fixture is intentionally left unannotated to guarantee that
    # this parent (rather than this child) fixture is type-checked as invalid.
    fixture_sync_gen_bad_decor,

    # Two or more parent fixtures that are *ALL* correctly annotated.
    fixture_sync_gen: str,
    fixture_sync_gen_needs_fixture: str,
) -> Iterable[str]:
    '''
    Synchronous generator fixture annotated by a correct yield hint but
    requiring one or more other such fixtures -- exactly one of which is
    annotated by a PEP-noncompliant yield hint inducing a decoration-time
    exception.
    '''

    # Yield an object satisfying the yield hint annotating this fixture,
    # ensuring that this fixture's failure derives only from requiring an
    # incorrectly hinted fixture.
    yield 'Deserted, void, nor any haunt of mine.'
