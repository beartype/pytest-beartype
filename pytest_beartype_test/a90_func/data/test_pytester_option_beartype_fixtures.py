#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **fixture integration test** (i.e., integration tests testing that
this plugin passed the ``--beartype-fixtures`` option correctly type-checks
fixtures) submodule.

This submodule is *not* intended to be directly collected by the root
:mod:`pytest` process. This submodule is *only* collected by the leaf
:mod:`pytest` subprocess implicitly spawned by the :mod:`pytest.pytester`
fixture required by the parent ``test_pytester_option_beartype_fixtures`` test.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ TESTS ~ sync : non-gen : pass      }....................
# Synchronous unit tests requiring synchronous non-generator fixtures expected
# to pass.

def test_pytester_option_beartype_fixtures_sync_nongenerator(
    fixture_sync_nongenerator,
    fixture_sync_nongenerator_needs_fixture,
) -> None:
    '''
    Synchronous unit test requiring one or more synchronous non-generator
    fixtures intentionally annotated by *no* hints.
    '''

    # Trivial smoke test that this fixture superficially behaves as expected.
    assert isinstance(fixture_sync_nongenerator, str)
    assert isinstance(fixture_sync_nongenerator_needs_fixture, str)

# ....................{ TESTS ~ sync : non-gen : fail      }....................
# Synchronous unit tests requiring synchronous non-generator fixtures expected
# to fail.

@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongenerator_bad(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongenerator_bad,
) -> None:
    '''
    Synchronous unit test requiring a synchronous non-generator fixture
    annotated by an incorrect return hint.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongenerator_needs_fixtures_bad(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongenerator_needs_fixtures_bad,
) -> None:
    '''
    Synchronous unit test requiring a synchronous non-generator fixture
    annotated by a correct return hint but requiring one or more other such
    fixtures -- exactly one of which is annotated by an incorrect return hint.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongenerator_bad_needs_fixtures(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongenerator_bad_needs_fixtures,
) -> None:
    '''
    Synchronous unit test requiring a synchronous non-generator fixture
    annotated by a correct return hint but requiring two or more other such
    fixtures all annotated by different parameter hints from the return hints
    annotating those fixtures.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongenerator_bad_all(
    # These fixtures are intentionally left unannotated to guarantee that these
    # fixtures (rather than this test) are type-checked as invalid.
    fixture_sync_nongenerator_bad,
    fixture_sync_nongenerator_needs_fixtures_bad,
    fixture_sync_nongenerator_bad_needs_fixtures,
) -> None:
    '''
    Synchronous unit test requiring two or more synchronous non-generator
    fixtures all annotated by incorrect hints (of some unspecified nature).

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass

# ....................{ TESTS ~ sync : gen : pass          }....................
# Synchronous unit tests requiring synchronous generator fixtures expected to
# pass.

def test_pytester_option_beartype_fixtures_sync_generator(
    fixture_sync_generator: str,
    fixture_sync_generator_needs_fixture: str,
) -> None:
    '''
    Synchronous unit test requiring one or more synchronous generator fixtures
    all annotated by correct parameter and return hints.
    '''

    # Trivial smoke test that this fixture superficially behaves as expected.
    assert isinstance(fixture_sync_generator, str)
    assert isinstance(fixture_sync_generator_needs_fixture, str)

# ....................{ TESTS ~ sync : gen : fail          }....................
# Synchronous unit tests requiring synchronous generator fixtures expected to
# fail.

#FIXME: Uncomment *AFTER* @beartype deeply type-checks generator functions.
#Currently, @beartype *ONLY* shallowly type-checks generator functions. In this
#case, @beartype *ONLY* type-checks this generator's outermost "Iterable[...]"
#return hint, which this generator trivially satisfies.
#
#See also this open upstream issue on the topic:
#    https://github.com/beartype/beartype/issues/589
# @pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_generator_bad(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_generator_bad,
) -> None:
    '''
    Synchronous unit test requiring a synchronous generator fixture annotated by
    an incorrect return hint.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


#FIXME: Uncomment *AFTER* @beartype deeply type-checks generator functions.
# @pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_generator_needs_fixtures_bad(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_generator_needs_fixtures_bad,
) -> None:
    '''
    Synchronous unit test requiring a synchronous generator fixture annotated by
    a correct return hint but requiring one or more other such fixtures --
    exactly one of which is annotated by an incorrect return hint.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_generator_bad_needs_fixtures(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_generator_bad_needs_fixtures,
) -> None:
    '''
    Synchronous unit test requiring a synchronous generator fixture annotated by
    a correct return hint but requiring two or more other such fixtures all
    annotated by different parameter hints from the return hints annotating
    those fixtures.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_generator_bad_all(
    # These fixtures are intentionally left unannotated to guarantee that these
    # fixtures (rather than this test) are type-checked as invalid.
    fixture_sync_generator_bad,
    fixture_sync_generator_needs_fixtures_bad,
    fixture_sync_generator_bad_needs_fixtures,
) -> None:
    '''
    Synchronous unit test requiring two or more synchronous generator fixtures
    all annotated by incorrect hints (of some unspecified nature).

    This fixture intentionally annotates multiple fixtures incorrectly,
    validating that this plugin correctly concatenates all failure messages
    originating from concurrently failing fixtures.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass
