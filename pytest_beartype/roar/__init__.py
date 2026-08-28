#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
**Plugin exception and warning hierarchies.**

This submodule publishes a hierarchy of:

* :mod:`pytest_beartype`-specific exceptions raised by this plugin at test suite
  execution time.
* :mod:`pytest_beartype`-specific warnings emitted at similar times.

Hear :mod:`pytest_beartype` roar as it efficiently checks types, validates data,
and raids native beehives for organic honey.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To prevent "mypy --no-implicit-reexport" from raising literally
# hundreds of errors at static analysis time, *ALL* public attributes *MUST* be
# explicitly reimported under the same names with "{exception_name} as
# {exception_name}" syntax rather than merely "{exception_name}". Yes, this is
# ludicrous. Yes, this is mypy. For posterity, these failures resemble:
#     beartype/_cave/_cavefast.py:47: error: Module "beartype.roar" does not
#     explicitly export attribute "BeartypeCallUnavailableTypeException";
#     implicit reexport disabled  [attr-defined]
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Public exception hierarchy.
from pytest_beartype.roar._roarexc import (
    PytestBeartypeException as PytestBeartypeException,
)

# Public warning hierarchy.
from pytest_beartype.roar._roarwarn import (
    PytestBeartypeWarning as PytestBeartypeWarning,
    PytestBeartypeConfWarning as PytestBeartypeConfWarning,
    PytestBeartypeConfPackagesWarning as PytestBeartypeConfPackagesWarning,
)
