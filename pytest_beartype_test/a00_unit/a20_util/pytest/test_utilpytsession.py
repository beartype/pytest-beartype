#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Unit tests testing the private
:mod:`pytest_beartype._util.pytest.utilpytsession` submodule.
'''

# ....................{ TESTS                              }....................
def test_get_user_test_paths(request: 'pytest.FixtureRequest') -> None:
    '''
    Unit test testing the public
    :func:`pytest_beartype._util.pytest.utilpytsession.get_user_test_paths`
    getter.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Standard :mod:`pytest` fixture exposing the current pytest session.
    '''

    # Defer test-specific imports.
    from pytest_beartype._util.pytest.utilpytsession import get_user_test_paths

    # Frozen set of all user test paths for the current pytest session.
    user_test_paths = get_user_test_paths(request.session)

    # Assert that this getter is memoized on this session by asserting that
    # calling this getter again with the same session returns the same set.
    assert get_user_test_paths(request.session) is user_test_paths

    # Assert that this getter returned a frozen set.
    assert isinstance(user_test_paths, frozenset)

    # Assert that this frozen set contains the expected items.
    _assert_get_user_test_paths(
        user_test_paths=user_test_paths, request=request)


def test_get_user_test_paths_fallback(request: 'pytest.FixtureRequest') -> None:
    '''
    Unit test testing the private
    :func:`pytest_beartype._util.pytest.utilpytsession._get_user_test_paths_fallback`
    getter.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Standard :mod:`pytest` fixture exposing the current pytest session.
    '''

    # Defer test-specific imports.
    from pytest_beartype.roar import PytestBeartypeSessionAttributeWarning
    from pytest_beartype._util.pytest.utilpytsession import (
        _get_user_test_paths_fallback)
    from pytest import warns

    # Assert that this fallback getter unconditionally raises the expected
    # warning.
    with warns(PytestBeartypeSessionAttributeWarning):
        # Collection of all user test paths for the current pytest session.
        user_test_paths = _get_user_test_paths_fallback(request.session)

        # Assert that this collection contains the expected items.
        _assert_get_user_test_paths(
            user_test_paths=user_test_paths, request=request)

# ....................{ PRIVATE ~ asserters                }....................
def _assert_get_user_test_paths(
    user_test_paths: 'collections.abc.Collection[pathlib.Path]',
    request: 'pytest.FixtureRequest',
) -> None:
    '''
    Assert that the passed user test paths (presumably created and returned by a
    getter with an API resembling that of the public
    :func:`pytest_beartype._util.pytest.utilpytsession.get_user_test_paths`
    getter) contains the expected items.

    Parameters
    ----------
    user_test_paths : collections.abc.Collection[pathlib.Path]
        User test paths to be tested.
    request : pytest.FixtureRequest
        Standard :mod:`pytest` fixture exposing the current pytest session.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer test-specific imports.
    from collections.abc import Collection
    from pathlib import Path

    # ....................{ LOCALS                         }....................
    # Path object encapsulating the absolute filename of this test submodule,
    # resolved of all symbolic links (as are all user test paths).
    test_submodule_file = Path(__file__).resolve()

    # ....................{ ASSERTS                        }....................
    # Assert that the passed object is a non-empty collection of "Path" objects.
    assert isinstance(user_test_paths, Collection)
    assert user_test_paths
    assert all(
        isinstance(user_test_path, Path) for user_test_path in user_test_paths)

    # Assert that this test submodule resides under at least one user test path.
    # Since pytest is currently executing this very test, pytest necessarily
    # collected this test submodule from one of these paths.
    #
    # Note that a user test path may be either a directory *OR* a file (e.g.,
    # when pytest is directly passed this test submodule at the command line) --
    # in which latter case this test submodule is that path itself.
    assert any(
        test_submodule_file.is_relative_to(
            user_test_path if user_test_path.is_dir() else
            user_test_path.parent
        )
        for user_test_path in user_test_paths
    )
