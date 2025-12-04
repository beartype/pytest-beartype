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
from pytest_beartype_test.a90_func.data._fixture.fixsync import (
    fixture_sync_nongenerator,
    fixture_sync_nongenerator_bad,
    fixture_sync_nongenerator_needs_fixture,
    fixture_sync_nongenerator_needs_fixtures_bad,
    fixture_sync_nongenerator_bad_needs_fixtures,
    fixture_sync_generator,
    fixture_sync_generator_bad,
    fixture_sync_generator_needs_fixture,
    fixture_sync_generator_needs_fixtures_bad,
    fixture_sync_generator_bad_needs_fixtures,
)
