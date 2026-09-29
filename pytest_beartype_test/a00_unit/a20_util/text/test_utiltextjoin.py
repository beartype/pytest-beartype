#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin-wide **string-joining utility** unit tests.

This submodule unit tests the public API of the private
:mod:`pytest_beartype._util.text.utiltextjoin` submodule.
'''

# ....................{ TESTS                              }....................
def test_join_strings_delimited() -> None:
    '''
    Test the
    :func:`pytest_beartype._util.text.utiltextjoin.join_strings_delimited`
    function.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer test-specific imports.
    from pytest_beartype._util.text.utiltextjoin import join_strings_delimited

    # ....................{ LOCALS                         }....................
    # Keyword arguments to be passed to *ALL* join_strings_delimited() calls
    # performed below.
    delimiters = dict(
        delimiter_if_two=' and ',
        delimiter_if_three_or_more_nonlast=', ',
        delimiter_if_three_or_more_last=', and ',
    )

    # ....................{ PASS                           }....................
    assert join_strings_delimited(strings=(), **delimiters) == ''
    assert join_strings_delimited(strings=('one',), **delimiters) == 'one'
    assert join_strings_delimited(
        strings=('one', 'two'), **delimiters) == 'one and two'
    assert join_strings_delimited(
        strings=('one', 'two', 'three'), **delimiters) == 'one, two, and three'

    assert join_strings_delimited(
        strings=(str(number) for number in range(4)), **delimiters) == (
        '0, 1, 2, and 3')

    assert join_strings_delimited(
        strings=('one', 'two'), is_double_quoted=True, **delimiters) == (
        '"one" and "two"')
