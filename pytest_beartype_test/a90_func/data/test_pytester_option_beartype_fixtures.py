#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **fixture integration test** (i.e., integration tests testing that
this plugin passed the ``--beartype-test-fixtures`` option correctly type-checks
fixtures) submodule.

This submodule is *not* intended to be directly collected by the root
:mod:`pytest` process. This submodule is *only* collected by the leaf
:mod:`pytest` subprocess explicitly forked by the parent
``test_option_beartype_fixtures`` integration test.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ TESTS ~ sync : non-gen : pass      }....................
# Synchronous unit tests requiring synchronous non-generator fixtures expected
# to pass.

def test_pytester_option_beartype_fixtures_sync_nongen(
    fixture_sync_nongen, fixture_sync_nongen_needs_fixture) -> None:
    '''
    Synchronous unit test requiring one or more synchronous non-generator
    fixtures intentionally annotated by *no* hints.
    '''

    # Trivial smoke test that this fixture superficially behaves as expected.
    assert isinstance(fixture_sync_nongen, str)
    assert isinstance(fixture_sync_nongen_needs_fixture, str)

# ....................{ TESTS ~ sync : non-gen : fail      }....................
# Synchronous unit tests requiring synchronous non-generator fixtures expected
# to fail.

@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongen_bad_needs_fixtures(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongen_bad_needs_fixtures,
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
def test_pytester_option_beartype_fixtures_sync_nongen_bad_call(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongen_bad_call,
) -> None:
    '''
    Synchronous unit test requiring a synchronous non-generator fixture
    annotated by a PEP-compliant return hint violating the returned value and
    thus inducing a call-time violation.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongen_bad_decor(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongen_bad_decor,
) -> None:
    '''
    Synchronous unit test requiring a synchronous non-generator fixture
    annotated by a PEP-noncompliant return hint inducing a decoration-time
    exception.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongen_needs_fixtures_bad_call(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongen_needs_fixtures_bad_call,
) -> None:
    '''
    Synchronous unit test requiring a synchronous non-generator fixture
    annotated by a correct return hint but requiring one or more other such
    fixtures -- exactly one of which is annotated by a PEP-compliant return hint
    violating the returned value and thus inducing a call-time violation.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongen_needs_fixtures_bad_decor(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_nongen_needs_fixtures_bad_decor,
) -> None:
    '''
    Synchronous unit test requiring a synchronous non-generator fixture
    annotated by a correct return hint but requiring one or more other such
    fixtures -- exactly one of which is annotated by a PEP-noncompliant return
    hint inducing a decoration-time exception.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_nongen_bad_all(
    # These fixtures are intentionally left unannotated to guarantee that these
    # fixtures (rather than this test) are type-checked as invalid.
    fixture_sync_nongen_bad_call,
    fixture_sync_nongen_bad_decor,
    fixture_sync_nongen_needs_fixtures_bad_call,
    fixture_sync_nongen_needs_fixtures_bad_decor,
    fixture_sync_nongen_bad_needs_fixtures,
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

def test_pytester_option_beartype_fixtures_sync_gen(
    fixture_sync_gen: str,
    fixture_sync_gen_needs_fixture: str,
) -> None:
    '''
    Synchronous unit test requiring one or more synchronous generator fixtures
    all annotated by correct parameter and return hints.
    '''

    # Trivial smoke test that this fixture superficially behaves as expected.
    assert isinstance(fixture_sync_gen, str)
    assert isinstance(fixture_sync_gen_needs_fixture, str)

# ....................{ TESTS ~ sync : gen : fail          }....................
# Synchronous unit tests requiring synchronous generator fixtures expected to
# fail.

@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_gen_bad_needs_fixtures(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_gen_bad_needs_fixtures,
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


#FIXME: Uncomment *AFTER* @beartype deeply type-checks generator functions.
#Currently, @beartype *ONLY* shallowly type-checks generator functions. In this
#case, @beartype *ONLY* type-checks this generator's outermost "Iterable[...]"
#return hint, which this generator trivially satisfies.
#
#See also this open upstream issue on the topic:
#    https://github.com/beartype/beartype/issues/589
# @pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_gen_bad_call(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_gen_bad_call,
) -> None:
    '''
    Synchronous unit test requiring a synchronous generator fixture annotated by
    a PEP-compliant return hint violating the returned value and thus inducing a
    call-time violation.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_gen_bad_decor(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_gen_bad_decor,
) -> None:
    '''
    Synchronous unit test requiring a synchronous generator fixture annotated by
    a PEP-noncompliant return hint inducing a decoration-time exception.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


#FIXME: Uncomment *AFTER* @beartype deeply type-checks generator functions.
# @pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_gen_needs_fixtures_bad_call(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_gen_needs_fixtures_bad_call,
) -> None:
    '''
    Synchronous unit test requiring a synchronous generator fixture annotated by
    a correct return hint but requiring one or more other such fixtures --
    exactly one of which is annotated by a PEP-compliant return hint violating
    the returned value and thus inducing a call-time violation.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_gen_needs_fixtures_bad_decor(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_sync_gen_needs_fixtures_bad_decor,
) -> None:
    '''
    Synchronous unit test requiring a synchronous generator fixture annotated by
    a correct return hint but requiring one or more other such fixtures --
    exactly one of which is annotated by a PEP-noncompliant return hint inducing
    a decoration-time exception.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass


@pytest.mark.xfail(strict=True)
def test_pytester_option_beartype_fixtures_sync_gen_bad_all(
    # These fixtures are intentionally left unannotated to guarantee that these
    # fixtures (rather than this test) are type-checked as invalid.
    fixture_sync_gen_bad_call,
    fixture_sync_gen_bad_decor,
    fixture_sync_gen_needs_fixtures_bad_call,
    fixture_sync_gen_needs_fixtures_bad_decor,
    fixture_sync_gen_bad_needs_fixtures,
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

# ....................{ TESTS ~ async : non-gen            }....................
# Asynchronous unit tests requiring asynchronous non-generator fixtures.
#
# Note that the asynchronous tests below are intentionally minimal smoke tests
# exercising only the most common asynchronous fixture use cases: one passing
# and one failing test for each of the non-generator and generator fixture
# categories, collectively covering both the call-time violation and
# decoration-time exception code paths. If deeper asynchronous coverage proves
# necessary, mirror the full synchronous test matrix above.

async def test_pytester_option_beartype_fixtures_async_nongen(
    fixture_async_nongen, fixture_async_nongen_needs_fixture) -> None:
    '''
    Asynchronous unit test requiring one or more asynchronous non-generator
    fixtures intentionally annotated by *no* hints.
    '''

    # Trivial smoke test that this fixture superficially behaves as expected.
    assert isinstance(fixture_async_nongen, str)
    assert isinstance(fixture_async_nongen_needs_fixture, str)


@pytest.mark.xfail(strict=True)
async def test_pytester_option_beartype_fixtures_async_nongen_bad_call(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_async_nongen_bad_call,
) -> None:
    '''
    Asynchronous unit test requiring an asynchronous non-generator fixture
    annotated by a PEP-compliant return hint violating the returned value and
    thus inducing a call-time violation.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass

# ....................{ TESTS ~ async : gen                }....................
# Asynchronous unit tests requiring asynchronous generator fixtures.

async def test_pytester_option_beartype_fixtures_async_gen(
    fixture_async_gen, fixture_async_gen_needs_fixture) -> None:
    '''
    Asynchronous unit test requiring one or more asynchronous generator
    fixtures intentionally annotated by *no* hints.
    '''

    # Trivial smoke test that this fixture superficially behaves as expected.
    assert isinstance(fixture_async_gen, str)
    assert isinstance(fixture_async_gen_needs_fixture, str)


@pytest.mark.xfail(strict=True)
async def test_pytester_option_beartype_fixtures_async_gen_bad_decor(
    # This fixture is intentionally left unannotated to guarantee that this
    # fixture (rather than this test) is type-checked as invalid.
    fixture_async_gen_bad_decor,
) -> None:
    '''
    Asynchronous unit test requiring an asynchronous generator fixture
    annotated by a PEP-noncompliant yield hint inducing a decoration-time
    exception.

    Note that this test intentionally requires a fixture inducing a
    decoration-time exception rather than a call-time violation. Why? Because
    @beartype currently only shallowly type-checks generator functions, which
    trivially satisfy their outermost "AsyncIterable[...]" yield hints. See
    also the similar synchronous generator tests above.
    '''

    # Reduce to a noop, ensuring that this test's failure derives solely from
    # requiring an incorrectly hinted fixture.
    pass
