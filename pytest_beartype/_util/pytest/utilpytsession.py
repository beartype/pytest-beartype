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
from pytest_beartype.roar import PytestBeartypeSessionAttributeWarning
from pytest_beartype._data.datatyping import (
    CollectionPaths,
    FrozenSetPaths,
)
from pytest_beartype._metaverse import (
    PACKAGE_NAME,
    URL_ISSUES,
)
from pytest_beartype._util.utilcache import callable_cached
from pytest_beartype._util.utilwarn import issue_warning
from pathlib import Path
from pytest import Session

# ....................{ GETTERS                            }....................
@callable_cached
def get_user_test_paths(session: Session) -> FrozenSetPaths:
    '''
    Frozen set of all **user test paths** (i.e., :class:`pathlib.Path` objects
    encapsulating the absolute paths of all files and directories the user
    instructed the passed :mod:`pytest` session to collect tests from).

    This getter returns **resolved paths** (i.e., :class:`pathlib.Path` objects
    encapsulating the absolute paths to files and directories that are
    guaranteed to *not* be symbolic links). These paths may refer to either
    files *or* directories. :mod:`pytest` happily collects tests from individual
    files (e.g., ``pytest muh_tests.py``) as well as directories. Callers *must*
    manually account for both use cases.

    This getter is memoized for efficiency.

    Caveats
    -------
    **This getter accesses the private** :attr:`pytest.Session._initialpaths`
    **attribute.** :mod:`pytest` publicizes *no* public API providing these
    paths. If this private attribute ever vanishes in a future :mod:`pytest`
    version, this getter issues a non-fatal warning and falls back to manually
    reconstructing these paths from the public :attr:`pytest.Config.args` list.

    Parameters
    ----------
    session : Session
        Current pytest session.

    Returns
    -------
    frozenset[Path]
        Frozen set of all user test paths for this session.

    Warns
    -----
    PytestBeartypeSessionAttributeWarning
        If the private :attr:`pytest.Session._initialpaths` attribute fails to
        exist.
    '''
    assert isinstance(session, Session), f'{repr(session)} not pytest session.'

    # Frozen set of the absolute paths of all files and directories the user
    # instructed this pytest session to collect tests from if the private
    # "Session._initialpaths" attribute still exists *OR* "None" otherwise.
    user_test_paths: CollectionPaths | None = getattr(
        session, '_initialpaths', None)

    # If this private attribute no longer exists, this version of pytest has
    # broken us. In this case...
    if user_test_paths is None:
        user_test_paths = _get_user_test_paths_fallback(session)
    # Else, this private attribute still exists.
    #
    # In either case, this frozen set is guaranteed to now exist.

    # Return the frozen set of each such path resolved of *ALL* symbolic links,
    # guaranteeing sane comparison against other similarly resolved paths.
    return frozenset(
        user_test_path.resolve(strict=True)
        for user_test_path in user_test_paths
    )

# ....................{ PRIVATE ~ getters                  }....................
def _get_user_test_paths_fallback(session: Session) -> CollectionPaths:
    '''
    Frozen set of all **user test paths** (i.e., :class:`pathlib.Path` objects
    encapsulating the absolute paths of all files and directories the user
    instructed the passed :mod:`pytest` session to collect tests from), computed
    according to a fragile fallback algorithm manually reconstructing these
    paths from the public :attr:`pytest.Config.args` list.

    Parameters
    ----------
    session : Session
        Current pytest session.

    Returns
    -------
    collection.abc.Collection[Path]
        Frozen set of all user test paths for this session.

    Warns
    -----
    PytestBeartypeSessionAttributeWarning
        Unconditionally.
    '''
    assert isinstance(session, Session), f'{repr(session)} not pytest session.'

    # ....................{ PREAMBLE                       }....................
    # Warn the user that this plugin is now operating on reconstructed
    # (and thus possibly desynchronized) user test paths *BEFORE* attempting any
    # further logic accessing possibly unsafe attributes from the private
    # "_pytest" package.
    issue_warning(
        warning_cls=PytestBeartypeSessionAttributeWarning,
        message=(
            f'Private "Session._initialpaths" attribute not found. '
            f'Falling back to manually reconstructing user test paths from '
            f'public "session.config.args" attribute. '
            f"Because we have no idea what we're doing, this could fail. "
            f'Consider reporting this issue to '
            f'the {PACKAGE_NAME} issue tracker at:\n'
            f'\t{URL_ISSUES}'
        )
    )

    # ....................{ IMPORTS                        }....................
    # Defer fallback-specific imports of private pytest internals.
    from _pytest.main import resolve_collection_argument

    # ....................{ COPY-PASTA                     }....................
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # WARNING: Begin creepy copy-pasta of private logic reverse-engineered from
    # the private _pytest.main.Session.perform_collect() method, which
    # resolves each command-line collection argument (e.g.,
    # "some_test.py::test_name") into the path component of that argument.
    # If pytest breaks the "_initialpaths" attribute, pytest could break
    # this fallback with similar impunity. It is what it is. *sigh*
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # List of the resolved paths of all collection arguments.
    initialpaths: list[Path] = []

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
        initialpaths.append(collection_argument.path)

    # ....................{ RETURN                         }....................
    # Return this list as is.
    return initialpaths
