#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Good weather** (i.e., data module defining sample functions correctly
annotated by hints satisfying :mod:`beartype`).
'''

# ....................{ FUNCTIONS                          }....................
def main(numbers: list[int]) -> int:
    '''
    Arbitrary function correctly annotated by hints satisfying :mod:`beartype`.
    '''

    return sum(numbers)


def helper_function(text: str) -> str:
    '''
    Arbitrary function also correctly annotated.
    '''

    return text.upper()
