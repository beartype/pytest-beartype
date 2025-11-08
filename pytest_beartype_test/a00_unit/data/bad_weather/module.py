#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Bad weather** (i.e., data module defining sample functions incorrectly
annotated by hints violating :mod:`beartype`).
'''

# ....................{ FUNCTIONS                          }....................
def sum_numbers(numbers: list[int]) -> str:
    '''
    Arbitrary function incorrectly annotated by hints violating :mod:`beartype`.
    '''

    return sum(numbers)


def upper_string(text: str) -> int:
    '''
    Arbitrary function also incorrectly annotated.
    '''

    return text.upper()
