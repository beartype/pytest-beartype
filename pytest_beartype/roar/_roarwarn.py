#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin **warning hierarchy** (i.e., public and private warning subclasses
issued at decoration, call, and usage time by :mod:`pytest_beartype`).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from abc import ABCMeta as _ABCMeta

# ....................{ SUPERCLASS                         }....................
class PytestBeartypeWarning(UserWarning, metaclass=_ABCMeta):
    '''
    Abstract base class of all **plugin warnings.**

    Instances of subclasses of this warning are issued at test suite execution
    time.
    '''

    # ..................{ INITIALIZERS                       }..................
    def __init__(self, message: str) -> None:
        '''
        Initialize this exception.

        This constructor (in order):

        #. Passes all passed arguments as is to the superclass constructor.
        #. Sanitizes the fully-qualified module name of this
           exception from the private ``"pytest_beartype.roar._roarwarn"``
           submodule to the public ``"pytest_beartype.roar"`` subpackage to both
           improve the readability of exception messages and discourage end
           users from accessing this private submodule.
        '''

        # Defer to the superclass constructor.
        super().__init__(message)

        # Sanitize the fully-qualified module name of the class of this
        # warning. See the docstring for justification.
        self.__class__.__module__ = 'pytest_beartype.roar'

# ....................{ OPTION                             }....................
class PytestBeartypeOptionWarning(PytestBeartypeWarning):
    '''
    Abstract base class of all **plugin option warnings.**

    Instances of subclasses of this warning are issued at :mod:`pytest`
    configuration time when passed one or more problematic command-line options.
    '''

    pass


class PytestBeartypeOptionPackagesWarning(PytestBeartypeOptionWarning):
    '''
    Plugin ``--beartype-packages`` **option warning.**

    This warning is emitted at :mod:`pytest` configuration time when passed a
    problematic ``--beartype-packages`` option, including:

    * When one or more packages or modules to be type-checked have already been
      imported under the active Python interpreter and thus *cannot* be
      type-checked.
    '''

    pass


#FIXME: Currently unneeded, but probably will be shortly. Preserved, yo!
# class PytestBeartypeOptionTestFixturesWarning(PytestBeartypeOptionWarning):
#     '''
#     Plugin ``--beartype-test-fixtures`` **option warning.**
#
#     This warning is emitted at :mod:`pytest` configuration time when passed a
#     problematic ``--beartype-test-fixtures`` option, including:
#
#     * When the only user-specified test paths to be tested by :mod:`pytest`
#       unsafely reduce to the current project's root directory, which commonly
#       contains third-party fixtures unsuitable for runtime type-checking (e.g.,
#       residing under uv-managed ``.venv/`` subdirectories).
#
#     This warning is emitted at :mod:`pytest` configuration time when one or more
#     packages or modules to be type-checked have already been imported under the
#     active Python interpreter and thus *cannot* be type-checked.
#     '''
#
#     pass

# ....................{ SESSION                            }....................
class PytestBeartypeSessionWarning(PytestBeartypeWarning):
    '''
    Abstract base class of all **plugin session warnings.**

    Instances of subclasses of this warning are issued at :mod:`pytest` test
    execution time when encountering a problematic :mod:`pytest` session.
    '''

    pass


class PytestBeartypeSessionAttributeWarning(PytestBeartypeSessionWarning):
    '''
    Plugin **pytest session attribute warning.**

    This warning is emitted at :mod:`pytest` test execution time when
    encountering a problematic :mod:`pytest` session object that fails to define
    an expected attribute.
    '''

    pass
