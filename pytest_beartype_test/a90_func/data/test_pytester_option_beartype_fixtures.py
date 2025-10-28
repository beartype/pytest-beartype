#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **fixture integration test** (i.e., integration tests testing that
this plugin passed the ``--beartype-fixtures`` option correctly type-checks
fixtures) submodule.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ TESTS ~ pass                       }....................
# Unit tests expected to succeed.

def test_fixture_hint_return_good(fixture_hint_return_good: int): ...
def test_fixture_hint_return_good_needs_fixture_hint_return_good(
    fixture_hint_return_good_needs_fixture_hint_return_good: int): ...

# ....................{ TESTS ~ fail                       }....................
# Unit tests expected to fail.

@pytest.mark.xfail(strict=True)
def test_fixture_hint_return_bad(fixture_hint_return_bad): ...

@pytest.mark.xfail(strict=True)
def test_fixture_needs_fixture_hint_return_bad(
    fixture_needs_fixture_hint_return_bad): ...

@pytest.mark.xfail(strict=True)
def test_fixture_hint_return_bad_needs_fixture_hint_return_good(
    fixture_hint_return_bad_needs_fixture_hint_return_good): ...
