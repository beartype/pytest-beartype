#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin-wide **pytest session utilities** (i.e., low-level callables
introspecting the current :class:`pytest.Session`, gracefully papering over
private :mod:`pytest` APIs where public APIs fail to suffice).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from pytest_beartype._util.utilcache import callable_cached
from pathlib import Path
from pytest import Session
from warnings import warn

# ....................{ GETTERS                            }....................
@callable_cached
def get_user_test_paths(session: Session) -> frozenset[Path]:
    '''
    Frozen set of all **user test paths** (i.e., :class:`pathlib.Path` objects
    encapsulating the absolute paths of all files and directories the user
    explicitly instructed the passed :mod:`pytest` session to collect tests
    from, resolved of all symbolic links).

    Note that user test paths are *not* guaranteed to be directories. Pytest
    happily collects tests from individual files (e.g., ``pytest
    test_something.py``) as well as directories. Callers comparing arbitrary
    paths against these paths should account for both possibilities.

    Caveats
    -------
    **This getter accesses the private** :attr:`pytest.Session._initialpaths`
    **attribute.** Pytest publicizes *no* API yielding the paths the user asked
    pytest to run. The public :meth:`pytest.Session.collect` method implicitly
    re-collects the entire test suite and is thus prohibitively slow for plugin
    use. If this private attribute ever vanishes in some future pytest, this
    getter falls back to manually reconstructing these paths from the public
    :attr:`pytest.Config.args` list -- emitting a non-fatal warning while
    doing so.

    This getter is memoized on the passed session for efficiency, as hooks
    (e.g., ``pytest_fixture_setup()``) repeatedly call this getter with the
    same session.

    Parameters
    ----------
    session : pytest.Session
        Current pytest session.

    Returns
    -------
    frozenset[Path]
        Frozen set of all user test paths for this session.
    '''
    assert isinstance(session, Session), f'{repr(session)} not pytest session.'

    # Frozen set of the absolute paths of all files and directories the user
    # instructed this pytest session to collect tests from if the private
    # "Session._initialpaths" attribute still exists *OR* "None" otherwise.
    user_test_paths = getattr(session, '_initialpaths', None)

    # If this private attribute no longer exists, this version of pytest has
    # broken us. In this case...
    if user_test_paths is None:
        # Warn the user that this plugin is now operating on reconstructed
        # (and thus possibly desynchronized) user test paths.
        warn(
            'Private "pytest.Session._initialpaths" attribute not found. '
            'Falling back to manually reconstructing user test paths from '
            'command-line arguments. '
            'Consider reporting this to the "pytest-beartype" issue tracker.'
        )

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # WARNING: Creepy copy-pasta of private logic reverse-engineered from
        # the private _pytest.main.Session.perform_collect() method, which
        # resolves each command-line collection argument (e.g.,
        # "some_test.py::test_name") into the path component of that argument.
        # If pytest breaks the "_initialpaths" attribute, pytest could break
        # this fallback with similar impunity. It is what it is. *sigh*
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Defer fallback-specific imports of private pytest internals.
        from _pytest.main import resolve_collection_argument

        # List of the resolved paths of all collection arguments.
        user_test_path_list = []

        # For each command-line collection argument passed to this session...
        for session_arg_index, session_arg in enumerate(session.config.args):
            # Object encapsulating the resolution of this argument. Note that
            # the signature of this private function requires "pytest >=
            # 9.1.0", which this plugin thus requires as well.
            collection_argument = resolve_collection_argument(
                session.config.invocation_params.dir,
                session_arg,
                session_arg_index,
                as_pypath=session.config.option.pyargs,
            )

            # Append the path component of this resolved argument.
            user_test_path_list.append(collection_argument.path)

        # Reduce this list to the expected frozen set.
        user_test_paths = user_test_path_list

    # Return the frozen set of these paths, resolved of all symbolic links to
    # guarantee sane comparison against other similarly resolved paths.
    return frozenset(
        Path(user_test_path).resolve() for user_test_path in user_test_paths)
