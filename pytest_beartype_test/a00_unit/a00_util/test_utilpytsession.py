#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Unit tests exercising the :mod:`pytest_beartype._util.pytest.utilpytsession`
submodule.
'''

# ....................{ TESTS                              }....................
def test_get_user_test_paths(request: 'pytest.FixtureRequest') -> None:
    '''
    Unit test exercising the
    :func:`pytest_beartype._util.pytest.utilpytsession.get_user_test_paths` getter.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Standard :mod:`pytest` fixture exposing the current pytest session.
    '''

    # Defer test-specific imports.
    from pathlib import Path
    from pytest_beartype._util.pytest.utilpytsession import get_user_test_paths

    # Frozen set of all user test paths for the current pytest session.
    user_test_paths = get_user_test_paths(request.session)

    # Assert this getter returned a non-empty frozen set of "Path" objects.
    assert isinstance(user_test_paths, frozenset)
    assert user_test_paths
    assert all(
        isinstance(user_test_path, Path) for user_test_path in user_test_paths)

    # Path object encapsulating the absolute filename of this test submodule,
    # resolved of all symbolic links (as are all user test paths).
    test_submodule_file = Path(__file__).resolve()

    # Assert this test submodule resides under at least one user test path.
    # Since pytest is currently executing this very test, pytest necessarily
    # collected this test submodule from one of these paths. Note that a user
    # test path may be either a directory *OR* a file (e.g., when pytest is
    # directly passed this test submodule at the command line) -- in which
    # latter case this test submodule is that path itself.
    assert any(
        test_submodule_file.is_relative_to(
            user_test_path if user_test_path.is_dir() else
            user_test_path.parent
        )
        for user_test_path in user_test_paths
    )

    # Assert this getter is memoized on the passed session by asserting that
    # calling this getter again with the same session yields the same object.
    assert get_user_test_paths(request.session) is user_test_paths
