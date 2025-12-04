#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
``pytest-beartype``.

``pytest-beartype`` is a :mod:`pytest` plugin optionally type-checking various
objects of test-specific interest with :mod:`beartype`, including:

* *All* :mod:`pytest` fixtures.
* *All* :mod:`pytest` tests.
* Zero or more external packages.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAUTION: Avoid importing from *ANY* packages at global scope to improve pytest
# startup performance. The sole exception is the "pytest" package itself. Since
# pytest has presumably already imported and run this plugin, the "pytest"
# package has presumably already been imported. Ergo, importing from that
# package yet again incurs no further costs.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from pytest_beartype._plug.pluginit import (
    pytest_addoption,
    pytest_configure,
)
from pytest_beartype._plug.plugfixture import (
    pytest_fixture_setup,
    pytest_pyfunc_call,
)
from pytest_beartype._plug.plugtest import (
    pytest_collection_modifyitems,
)

# ....................{ GLOBALS                            }....................
__version__ = '0.3.0'
'''
Human-readable package version as a ``.``-delimited string.

For :pep:`8` compliance, this specifier has the canonical name ``__version__``
rather than that of a typical global (e.g., ``VERSION_STR``).

Note that this is the canonical version specifier for this package. Indeed, the
top-level ``pyproject.toml`` file dynamically derives its own ``version`` string
from this string global.

See Also
--------
pyproject.toml
   The Hatch-specific ``[tool.hatch.version]`` subsection of the top-level
   ``pyproject.toml`` file, which parses its version from this string global.
'''
