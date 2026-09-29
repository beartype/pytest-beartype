#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin-wide **callable cache utility** unit tests.

This submodule unit tests the public API of the private
:mod:`pytest_beartype._util.cache.utilcachefunc` submodule.
'''

# ....................{ TESTS                              }....................
def test_callable_cached() -> None:
    '''
    Test the
    :func:`pytest_beartype._util.cache.utilcachefunc.callable_cached` decorator.
    '''

    # ..................{ IMPORTS                            }..................
    # Defer test-specific imports.
    from pytest_beartype._util.cache.utilcachefunc import callable_cached
    from pytest import raises

    # ..................{ CALLABLES                          }..................
    @callable_cached
    def still_i_rise(bitter, twisted, lies):
        '''
        Arbitrary non-variadic callable memoized by this decorator.
        '''

        # If an arbitrary condition, raise an exception whose value depends on
        # these parameters to exercise this decorator's conditional caching of
        # exceptions.
        if len(lies) == 6:
            raise ValueError(lies)

        # Else, return a value depending on these parameters to exercise this
        # decorator's conditional caching of return values.
        return bitter + twisted + lies


    @callable_cached
    def from_savage_men(with_his, sweet_voice = ('and, eyes',), *args):
        '''
        Arbitrary variadic callable memoized by this decorator.
        '''

        # If an arbitrary condition, raise an exception whose value depends on
        # these parameters to exercise this decorator's conditional caching of
        # exceptions.
        if len(args) == 6:
            raise ValueError(lies)

        # Else, return a value depending on these parameters to exercise this
        # decorator's conditional caching of return values.
        return with_his + sweet_voice + args

    # ..................{ LOCALS                             }..................
    # Hashable objects to be passed as parameters below.
    bitter  = ('You', 'may', 'write', 'me', 'down', 'in', 'history',)
    twisted = ('With', 'your', 'bitter,', 'twisted,', 'lies.',)
    lies    = ('You', 'may', 'trod,', 'me,', 'in', 'the', 'very', 'dirt',)
    dust    = ('But', 'still,', 'like', 'dust,', "I'll", 'rise',)

    # ..................{ PASS ~ non-variadic                }..................
    # Test the non-variadic function defined above.

    # Assert that memoizing two calls passed the same positional arguments
    # caches and returns the same value.
    assert (
        still_i_rise(bitter, twisted, lies) is
        still_i_rise(bitter, twisted, lies))

    # Assert that memoizing a call expected to raise an exception does so.
    with raises(ValueError) as exception_first_info:
        still_i_rise(bitter, twisted, dust)

    # Assert that repeating that call reraises the same exception.
    with raises(ValueError) as exception_next_info:
        still_i_rise(bitter, twisted, dust)
    assert exception_first_info.value is exception_next_info.value

    # Assert that passing one or more unhashable parameters to this callable
    # succeeds with the expected return value.
    assert still_i_rise(
        ['Just', 'like', 'moons',],
        ['and', 'like', 'suns',],
        ['With the certainty of tides',],
    ) == [
        'Just', 'like', 'moons',
        'and', 'like', 'suns',
        'With the certainty of tides',
    ]

    # ..................{ PASS ~ non-variadic                }..................
    # Test the variadic function defined above.

    # Assert that memoizing two calls passed *NO* optional or variadic
    # positional arguments caches and returns the same value.
    assert from_savage_men(bitter) is from_savage_men(bitter)

    # Assert that memoizing two calls passed optional positional arguments but
    # *NO* variadic positional arguments caches and returns the same value.
    assert from_savage_men(bitter, twisted) is from_savage_men(bitter, twisted)

    # Assert that memoizing two calls passed the same positional arguments
    # caches and returns the same value.
    assert (
        from_savage_men(bitter, twisted, *lies) is
        from_savage_men(bitter, twisted, *lies))
