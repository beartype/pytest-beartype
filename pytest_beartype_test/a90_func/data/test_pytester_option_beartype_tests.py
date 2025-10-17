#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Test submodule defining incorrectly typed test functions to be decorated by
the :func:`beartype.beartype` decorator.
'''

# ....................{ IMPORTS                            }....................
import pytest

# ....................{ TESTS                              }....................
@pytest.mark.skip
def test_function_with_type_violation() -> None:
    # This does not cause beartype violation, because, ehhh, that is like
    # impossible to check
    #
    # Don't do that :) please...
    def helper_func(x: str) -> int:
        return x

    helper_func('test')
