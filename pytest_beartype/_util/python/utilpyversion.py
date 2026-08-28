#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **Python interpreter version utilities**.

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from sys import version_info

# ....................{ CONSTANTS                          }....................
# While cumbersome, the current approach is substantially faster than automated
# alternatives (e.g., dictionary subclasses overriding the __missing__() dunder
# method to implement crude caches). Faster >>>> every other concern here, as
# Python interpreter version checks appear so frequently in critical code paths.

#FIXME: After dropping Python 3.11 support:
#* Refactor all code conditionally testing this global to be unconditional.
#* Remove this global.
#* Remove all decorators resembling:
#  @skip_if_python_version_less_than('3.12.0')
# IS_PYTHON_AT_LEAST_3_12 = IS_PYTHON_AT_LEAST_3_13 or version_info >= (3, 12)
IS_PYTHON_AT_LEAST_3_12 = version_info >= (3, 12)
'''
:data:`True` only if the active Python interpreter targets at least Python
3.12.0.
'''
