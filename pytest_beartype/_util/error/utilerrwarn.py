#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **warning handlers** (i.e., low-level callables manipulating
non-fatal warnings -- which, technically, are also exceptions -- in a
human-readable general-purpose manner).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from pytest_beartype._data.datatyping import TypeWarning
from pytest_beartype._util.python.utilpyversion import IS_PYTHON_AT_LEAST_3_12
from pytest_beartype._util.cache.utilcachefunc import callable_cached
from warnings import warn

# ....................{ WARNERS                            }....................
#FIXME: Unit test us up, please. *sigh*
# If the active Python interpreter targets Python >= 3.12, the standard
# warnings.warn() function supports the optional "skip_file_prefixes" parameter
# critical for emitting more useful warnings. In this case, define our
# issue_warning() warner to pass that parameter.
if IS_PYTHON_AT_LEAST_3_12:
    # ....................{ IMPORTS                        }....................
    # Defer version-specific imports.
    import pytest_beartype
    from os.path import dirname

    # ....................{ WARNERS                        }....................
    def issue_warning(warning_cls: TypeWarning, message: str) -> None:

        # The warning you gave us is surely our last!
        warn(  # type: ignore[call-overload]
            message,
            warning_cls,
            skip_file_prefixes=_ISSUE_WARNING_IGNORE_DIRNAMES,
            #FIXME: Unsure exactly what this does. Pretend you didn't see this.
            # stacklevel=1,  # <-- dark magic glistens dangerously
        )

    # ....................{ PRIVATE ~ globals              }....................
    _ISSUE_WARNING_IGNORE_DIRNAMES = (dirname(pytest_beartype.__file__),)
    '''
    Tuple of one or more **ignorable warning dirnames** (i.e., absolute
    directory names of all Python modules to be ignored by the
    :func:`.issue_warning` warner when deciding which source module to associate
    with the issued warning, enabling this warner to associate this warning with
    the original externally defined module to which this warning applies).

    This tuple includes the dirname of the top-level directory providing the
    :mod:`beartype` package, enabling this warner to ignore all stack frames
    produced by internal calls to submodules of this package. Doing so emits
    substantially more useful and readable warnings for external callers.
    '''
# Else, the active Python interpreter targets Python < 3.12. In this case,
# define our issue_warning() warner to avoid passing that parameter.
else:
    def issue_warning(warning_cls: TypeWarning, message: str) -> None:

        # Time to cry your tears! Now cry!
        warn(message, warning_cls)


issue_warning.__doc__ = (
    '''
    Issue (i.e., emit) a non-fatal warning of the passed type with the passed
    message.

    Caveats
    -------
    **This high-level warner should always be called in lieu of the low-level**
    :func:`warnings.warn` **warner.** Whereas the latter issues warnings that
    obfuscate the external user-defined modules to which those warnings apply,
    this warner associates this warning with the applicable user-defined module
    when the active Python interpreter targets Python >= 3.12.

    Parameters
    ----------
    warning_cls: type[Warning]
        Type of warning to be issued.
    message: str
        Human-readable warning message to be issued.

    Warns
    -----
    warning_cls
        Unconditionally.
    '''
)

# ....................{ WARNERS ~ once                     }....................
#FIXME: Currently unused but still useful. Preserved for posterity, yo! \o/
#FIXME: Unit test us up, please. *sigh*
# def issue_warning_once(warning_cls: TypeWarning, message: str) -> None:
#     '''
#     Issue (i.e., emit) a non-fatal warning of the passed type with the passed
#     message exactly once for the lifetime of this active Python interpreter.
#
#     Parameters
#     ----------
#     warning_cls: type[Warning]
#         Type of warning to be issued once.
#     message: str
#         Human-readable warning message to be issued once.
#
#     Warns
#     -----
#     warning_cls
#         Unconditionally.
#
#     See Also
#     --------
#     :func:`.issue_warning`
#         Further details.
#     '''
#
#     # The beat of destruction says, "Farewell, dear one-liner brother."
#     _issue_warning_once(warning_cls, message)
#
#
# @callable_cached
# def _issue_warning_once(warning_cls: TypeWarning, message: str) -> None:
#     '''
#     Issue (i.e., emit) a non-fatal warning of the passed type with the passed
#     message exactly once for the lifetime of this active Python interpreter.
#
#     This function is memoized as a trivial means of ensuring that the passed
#     warning is issued exactly once. Since the :func:`.callable_cached` decorator
#     required to do so accepts only positional parameters *and* since the
#     higher-level public :func:`.issue_warning_once` function calling this
#     lower-level private :func:`._issue_warning_once` function flexibly accepts
#     keyword parameters, the former trivially defers to the latter as a
#     simplistic means of achieving both goals. Truly, lamentable design. *sigh*
#
#     See Also
#     --------
#     :func:`.issue_warning_once`
#         Further details.
#     '''
#
#     # Key of the light! Dance on the road, one-liner!
#     issue_warning(warning_cls, message)
