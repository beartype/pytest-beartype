#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
``pytest-beartype``.

``pytest-beartype`` is a :mod:`pytest` plugin optionally type-checking various
objects of test-specific interest with :mod:`beartype`, including:

* Local :mod:`pytest` fixtures (i.e., user-defined fixtures defined in the test
  suite currently being tested).
* Local :mod:`pytest` tests (i.e., user-defined tests defined in the test suite
  currently being tested).
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
from pytest_beartype._metaverse import (
    VERSION as _VERSION,
    VERSION_PARTS as _VERSION_PARTS,
)
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
__version__ = _VERSION
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


__version_info__ = _VERSION_PARTS
'''
Machine-readable package version as a tuple of integers.

For :pep:`8` compliance, this specifier has the canonical name
``__version_info__`` rather than that of a typical global (e.g.,
``VERSION_PARTS``).
'''

# ....................{ GLOBALS ~ __all__                  }....................
__all__ = [
    '__version__',
    '__version_info__',
]
'''
Special list global of the unqualified names of all public package attributes
explicitly exported by and thus safely importable from this package.

Caveats
-------
**This global is defined only for conformance with static type checkers,** a
necessary prerequisite for :pep:`561`-compliance. This global is *not* intended
to enable star imports of the form ``from beartype import *`` (now largely
considered a harmful anti-pattern by the Python community), although it
technically does the latter as well.

This global would ideally instead reference *only* a single package attribute
guaranteed *not* to exist (e.g., ``'STAR_IMPORTS_CONSIDERED_HARMFUL'``),
effectively disabling star imports. Since doing so induces spurious static
type-checking failures, we reluctantly embrace the standard approach. For
example, :mod:`mypy` emits an error resembling:

    error: Module 'pytest_beartype' does not explicitly export attribute
    '__version__'; implicit reexport disabled.
'''
