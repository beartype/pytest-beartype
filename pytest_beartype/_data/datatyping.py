#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin-wide **type hints** (i.e., PEP-compliant type hints annotating callables
and classes declared throughout this codebase, either for compliance with
:pep:`561`-compliant static type checkers like :mod:`mypy` or simply for
documentation purposes).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from collections.abc import Callable
from typing import TypeVar

# ....................{ PEP ~ 484 : typevar                }....................
CallableT = TypeVar('CallableT', bound=Callable)
'''
**Callable type variable** (i.e., bound to match *only* callables).
'''

# ....................{ TYPE                               }....................
TypeException = type[Exception]
'''
:pep:`585`-compliant type hint matching *any* exception class.
'''


TypeWarning = type[Warning]
'''
:pep:`585`-compliant type hint matching *any* warning category.
'''
