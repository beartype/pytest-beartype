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
from collections.abc import (
    Callable,
    Collection,
)
from pathlib import Path
from typing import TypeVar

# ....................{ COLLECTION                         }....................
CollectionPaths = Collection[Path]
'''
:pep:`585`-compliant type hint matching *any* collection containing zero or more
**paths** (i.e., :class:`.Path` objects).
'''

# ....................{ FROZENSET                          }....................
FrozenSetPaths = frozenset[Path]
'''
:pep:`585`-compliant type hint matching *any* frozen set containing zero or more
**paths** (i.e., :class:`.Path` objects).
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

# ....................{ PEP ~ 484 : typevar                }....................
CallableT = TypeVar('CallableT', bound=Callable)
'''
**Callable type variable** (i.e., bound to match *only* callables).
'''
