#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
**Hear** ``pytest-beartype`` **tests roar** as it handles errors and warnings.

This submodule defines hierarchies of :mod:`pytest_beartype_test`-specific
exceptions and warnings emitted by unit and integration tests and fixtures.
'''

# ....................{ SUPERCLASS                         }....................
class PytestBeartypeTestException(Exception):
    '''
    Abstract base class of all ``pytest-beartype`` **test exceptions.**

    Instances of subclasses of this exception are raised at test time from
    :mod:`pytest_beartype_test`-specific unit and integration tests and fixtures.
    '''

    pass


class PytestBeartypeTestPathException(PytestBeartypeTestException):
    '''
    ``pytest-beartype`` **test path exception.**

    This exception is raised at test time from callables and classes defined by
    the :mod:`pytest_beartype_test._util.path` subpackage.
    '''

    pass



class PytestBeartypeTestMarkException(PytestBeartypeTestException):
    '''
    ``pytest-beartype`` **test test mark exception.**

    This exception is raised at test time from decorators defined by the
    :mod:`pytest_beartype_test._util.mark` subpackage.
    '''

    pass
