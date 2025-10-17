#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
:mod:`pytest` **test-skipping decorators.**

This submodule provides decorators conditionally marking their decorated tests
as skipped depending on whether the conditions signified by the passed
parameters are satisfied (e.g., the importability of the passed module name).
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import pytest
from collections.abc import (
    Mapping,
    Sequence,
)
from types import FunctionType
from typing import (
    Optional,
    Type,
)

# Sadly, the following imports require private modules and packages.
from _pytest.runner import Skipped

# ....................{ SKIP                               }....................
skip_if = pytest.mark.skipif
'''
Conditionally skip the decorated test or fixture with the passed human-readable
justification if the passed boolean is ``False``.

Parameters
----------
boolean : bool
    Boolean to be tested.
reason : str
    Human-readable message justifying the skipping of this test or fixture.
'''


def skip(reason: str):
    '''
    Unconditionally skip the decorated test with the passed human-readable
    justification.

    This decorator is intended to be called both directly as a function *and*
    indirectly as a decorator, which differs from both:

    * :func:`pytest.skip`, intended to be called only directly as a function.
      Attempting to call that function indirectly as a decorator produces
      extraneous ignorable messages on standard output resembling
      ``"SKIP [1] beartype_test/unit/test_import.py:66: could not import
      'xdist'"``, for unknown (and probably uninteresting) reasons.
    * :func:`pytest.mark.skip`, intended to be called only indirectly as a
      decorator. Attempting to call that decorator directly as a function
      reduces to a noop, for unknown (and probably uninteresting) reasons.

    Parameters
    ----------
    reason : str
        Human-readable message justifying the skipping of this test.

    Returns
    -------
    pytest.skipif
        Decorator skipping the decorated test with this justification.
    '''
    assert isinstance(reason, str), f'{repr(reason)} not string.'

    return skip_if(True, reason=reason)

# ....................{ SKIP ~ py : module                 }....................
def skip_unless_package(
    package_name: str, minimum_version: Optional[str] = None):
    '''
    Skip the decorated test or fixture if the package with the passed name is
    **unsatisfied** (i.e., either dynamically unimportable *or* importable but
    of a version less than the passed minimum version if non-:data:`None`).

    Parameters
    ----------
    package_name : str
        Fully-qualified name of the package to be skipped.
    minimum_version : Optional[str]
        Optional minimum version of this package as a dot-delimited string
        (e.g., ``0.4.0``) to be tested for if any *or* :data:`None` otherwise, in
        which case any version is acceptable. Defaults to :data:`None`.

    Returns
    -------
    pytest.skipif
        Decorator describing these requirements if unmet *or* the identity
        decorator reducing to a noop otherwise.
    '''
    assert isinstance(package_name, str), (
        f'{repr(package_name)} not string.')

    # Skip the decorated test or fixture unless the requisite dunder submodule
    # declared by this package satisfies these requirements.
    return skip_unless_module(
        module_name=package_name,

        #FIXME: Fascinatingly, this submodule importation worked for *ALL*
        #third-party packages except PyTorch. For unknown reasons, attempting to
        #dynamically import the "torch.__init__" submodule raises:
        #    NameError: name '_C' is not defined
        #
        #Thankfully, directly importing the package as is suffices. *shrug*
        # module_name=f'{package_name}.__init__',

        minimum_version=minimum_version,
    )


def skip_unless_module(
    module_name: str, minimum_version: Optional[str] = None):
    '''
    Skip the decorated test or fixture if the module with the passed name is
    **unsatisfied** (i.e., either dynamically unimportable *or* importable but
    of a version less than the passed minimum version if non-:data:`None`).

    Caveats
    -------
    **This decorator should never be passed the fully-qualified name of a
    package.** Consider calling the :func:`skip_unless_package` decorator
    instead to skip unsatisfied packages. Calling this decorator with package
    names guarantees those packages to be skipped, as packages are *not*
    directly importable as modules.

    Parameters
    ----------
    module_name : str
        Fully-qualified name of the module to be skipped.
    minimum_version : Optional[str]
        Optional minimum version of this module as a dot-delimited string
        (e.g., ``0.4.0``) to be tested for if any *or* :data:`None` otherwise, in
        which case any version is acceptable. Defaults to :data:`None`.

    Returns
    -------
    pytest.skipif
        Decorator describing these requirements if unmet *or* the identity
        decorator reducing to a noop otherwise.
    '''
    assert isinstance(module_name, str), (
        f'{repr(module_name)} not string.')
    assert isinstance(minimum_version, (str, type(None))), (
        f'{repr(minimum_version)} neither string nor "None".')

    return _skip_if_callable_raises_exception(
        exception_type=Skipped,
        func=pytest.importorskip,
        args=(module_name, minimum_version),
    )

# ....................{ SKIP ~ private                     }....................
def _skip_if_callable_raises_exception(
    # Mandatory parameters.
    exception_type: Type[BaseException],
    func: FunctionType,

    # Optional parameters.
    args: Optional[Sequence] = None,
    kwargs: Optional[Mapping] = None,
):
    '''
    Skip the decorated test or fixture if calling the passed callable with the
    passed positional and keyword arguments raises an exception of the passed
    type.

    Specifically, if calling this callable raises:

    * The passed type of exception, this test is marked as skipped.
    * Any other type of exception, this test is marked as a failure.
    * No exception, this test continues as expected.

    Parameters
    ----------
    exception_type : Type[BaseException]
        Type of exception expected to be raised by this callable.
    func : FunctionType
        Callable to be called.
    args : Optional[Sequence]
        Sequence of all positional arguments to unconditionally pass to the
        passed callable if any *or* :data:`None` otherwise. Defaults to
        :data:`None`.
    kwargs : Optional[Mapping]
        Mapping of all keyword arguments to unconditionally pass to the passed
        callable if any *or* :data:`None` otherwise. Defaults to :data:`None`.

    Returns
    -------
    pytest.skipif
        Decorator skipping this test if this callable raises this exception
        *or* the identity decorator reducing to a noop otherwise.
    '''

    # Avoid circular import dependencies.
    from pytest_beartype_test._util.mark.pytmark import noop

    # Default all unpassed arguments to sane values.
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    # Validate *AFTER* defaulting these arguments.
    assert isinstance(exception_type, type), (
        f'{repr((exception_type))} not type.')
    assert callable(func), f'{repr(func)} uncallable.'
    assert isinstance(args, Sequence), f'{repr(args)} not sequence.'
    assert isinstance(kwargs, Mapping), f'{repr(kwargs)} not mapping.'

    # Attempt to call this callable with these arguments.
    try:
        func(*args, **kwargs)
    # If this callable raises an expected exception, skip this test.
    except exception_type as exception:
        return skip(str(exception))
    # Else if this callable raises an unexpected exception, fail this test by
    # permitting this exception to unwind the current call stack.

    # Else, this callable raised no exception. Silently reduce to a noop.
    return noop
