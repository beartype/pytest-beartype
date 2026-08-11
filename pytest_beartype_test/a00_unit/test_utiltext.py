#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin text utility unit tests.
'''

# ....................{ TESTS                              }....................
def test_join_strings_delimited() -> None:
    '''Test the local ``join_strings_delimited`` utility.'''

    from pytest_beartype._util.utiltext import join_strings_delimited

    delimiters = dict(
        delimiter_if_two=' and ',
        delimiter_if_three_or_more_nonlast=', ',
        delimiter_if_three_or_more_last=', and ',
    )

    assert join_strings_delimited(strings=(), **delimiters) == ''
    assert join_strings_delimited(strings=('one',), **delimiters) == 'one'
    assert join_strings_delimited(
        strings=('one', 'two'), **delimiters) == 'one and two'
    assert join_strings_delimited(
        strings=('one', 'two', 'three'), **delimiters) == 'one, two, and three'
    assert join_strings_delimited(
        strings=(str(number) for number in range(4)),
        **delimiters,
    ) == '0, 1, 2, and 3'
    assert join_strings_delimited(
        strings=('one', 'two'),
        is_double_quoted=True,
        **delimiters,
    ) == '"one" and "two"'
