#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **asynchronous fixtures** (i.e., asynchronous fixture functions to be
tested by tests defined elsewhere) submodule.
'''

# ....................{ IMPORTS                            }....................
from collections.abc import Iterable
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
