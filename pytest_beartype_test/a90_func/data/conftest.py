#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **integration test fixture data** (i.e., fixture functions to be
tested by integration tests defined elsewhere) submodule.
'''

# ....................{ IMPORTS                            }....................
from ._fixture.fixasync import (
    fixture_async_gen,
    fixture_async_gen_bad_call,
    fixture_async_gen_bad_decor,
    fixture_async_gen_bad_needs_fixtures,
    fixture_async_gen_needs_fixture,
    fixture_async_gen_needs_fixtures_bad_call,
    fixture_async_gen_needs_fixtures_bad_decor,
    fixture_async_nongen,
    fixture_async_nongen_bad_call,
    fixture_async_nongen_bad_decor,
    fixture_async_nongen_bad_needs_fixtures,
    fixture_async_nongen_needs_fixture,
    fixture_async_nongen_needs_fixtures_bad_call,
    fixture_async_nongen_needs_fixtures_bad_decor,
)
from ._fixture.fixsync import (
    fixture_sync_gen,
    fixture_sync_gen_bad_call,
    fixture_sync_gen_bad_decor,
    fixture_sync_gen_bad_needs_fixtures,
    fixture_sync_gen_needs_fixture,
    fixture_sync_gen_needs_fixtures_bad_call,
    fixture_sync_gen_needs_fixtures_bad_decor,
    fixture_sync_nongen,
    fixture_sync_nongen_bad_call,
    fixture_sync_nongen_bad_decor,
    fixture_sync_nongen_bad_needs_fixtures,
    fixture_sync_nongen_needs_fixture,
    fixture_sync_nongen_needs_fixtures_bad_call,
    fixture_sync_nongen_needs_fixtures_bad_decor,
)

