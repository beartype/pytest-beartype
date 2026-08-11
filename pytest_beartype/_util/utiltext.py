#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin **text utilities** (i.e., low-level callables operating on strings in a
general-purpose manner).
'''

# ....................{ IMPORTS                            }....................
from collections.abc import (
    Iterable,
    Sequence,
)

# ....................{ JOINERS                            }....................
def join_strings_delimited(
    # Mandatory parameters.
    strings: Iterable[str],

    # Mandatory keyword-only parameters.
    *,
    delimiter_if_two: str,
    delimiter_if_three_or_more_nonlast: str,
    delimiter_if_three_or_more_last: str,

    # Optional keyword-only parameters.
    is_double_quoted: bool = False,
) -> str:
    '''
    Concatenate the passed iterable of zero or more strings delimited by the
    passed delimiters conditionally depending on the number of strings.

    Specifically, this function returns either:

    * If this iterable contains no strings, the empty string.
    * If this iterable contains one string, this string unmodified.
    * If this iterable contains two strings, these strings delimited by the
      passed ``delimiter_if_two`` delimiter.
    * If this iterable contains three or more strings, all strings except the
      last two delimited by ``delimiter_if_three_or_more_nonlast`` and the last
      two delimited by ``delimiter_if_three_or_more_last``.
    '''
    assert isinstance(strings, Iterable) and not isinstance(strings, str), (
        f'{repr(strings)} not non-string iterable.')
    assert isinstance(delimiter_if_two, str), (
        f'{repr(delimiter_if_two)} not string.')
    assert isinstance(delimiter_if_three_or_more_nonlast, str), (
        f'{repr(delimiter_if_three_or_more_nonlast)} not string.')
    assert isinstance(delimiter_if_three_or_more_last, str), (
        f'{repr(delimiter_if_three_or_more_last)} not string.')
    assert isinstance(is_double_quoted, bool), (
        f'{repr(is_double_quoted)} not boolean.')

    # If this iterable is *NOT* a sequence, internally coerce this iterable
    # into a sequence for subsequent indexing purposes.
    if not isinstance(strings, Sequence):
        strings = tuple(strings)

    # If passed *NO* strings, immediately reduce to a noop.
    if not strings:
        return ''
    # Else, if double-quoting these strings, do so.
    elif is_double_quoted:
        strings = tuple(f'"{string}"' for string in strings)

    # Number of strings in this non-empty sequence.
    strings_len = len(strings)

    # If passed exactly one string, return this string as is.
    if strings_len == 1:
        return strings[0]
    # If passed exactly two strings, delimit these strings as requested.
    elif strings_len == 2:
        return f'{strings[0]}{delimiter_if_two}{strings[1]}'

    # All such strings except the last two, delimited appropriately.
    strings_before_last_two = delimiter_if_three_or_more_nonlast.join(
        strings[0:-2])

    # The last two such strings, delimited appropriately.
    strings_last_two = (
        f'{strings[-2]}{delimiter_if_three_or_more_last}{strings[-1]}')

    # Return these two substrings, delimited appropriately.
    return (
        f'{strings_before_last_two}'
        f'{delimiter_if_three_or_more_nonlast}'
        f'{strings_last_two}'
    )
