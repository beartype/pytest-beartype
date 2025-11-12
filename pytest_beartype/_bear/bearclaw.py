#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2025 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype-specific **import hooks** (i.e., high-level callables registering one
or more third-party packages to be type-checked through :mod:`beartype.claw`
import hooks at :mod:`pytest` test time).
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAUTION: Importing from the external "beartype" package is acceptable *ONLY*
# from within this subpackage.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from beartype import (
    beartype,
    BeartypeConf,
)
from beartype.claw import (
    beartype_all,
    beartype_packages,
)
from beartype.roar import BeartypeWarning
from warnings import warn

#FIXME: Non-ideal violation of privacy encapsulation. To reduce the fragility of
#this plugin, copy-paste this function (and *ALL* parent functions thereof) into
#this plugin, please. *sigh*
from beartype._util.text.utiltextjoin import join_delimited

# Standard lists of module names, used to filter out already-imported modules
# from the warning message (about the fact that some modules have already been
# imported and will not be checked) if the user passes one or both of the
# "--beartype-packages='*'" or "--beartype-skip-packages=..." options.
from sys import (
    builtin_module_names as module_names_builtin,
    modules              as module_names_imported,
    stdlib_module_names  as module_names_stdlib,
)

# ....................{ WARNINGS                           }....................
class BeartypePytestWarning(BeartypeWarning):
    '''
    Beartype :mod:`pytest` warning.

    This warning is emitted at :mod:`pytest` configuration time when one
    or more packages or modules to be type-checked have already been
    imported under the active Python interpreter.
    '''

    pass

# ....................{ IMPORT HOOKS                       }....................
@beartype
def beartype_test_packages(
    package_names: tuple[str, ...],
    skip_package_names: tuple[str, ...],
) -> None:
    '''
    Register a new :mod:`beartype.claw` import hook automatically type-checking
    *all* of the packages and modules with the passed names (excluding *all* of
    the skipped packages and modules with the passed names) subsequently
    imported during :mod:`pytest` test execution with :func:`beartype.beartype`.

    Parameters
    ----------
    package_names : tuple[str, ...]
        Tuple of the fully-qualified names of *all* packages and modules to be
        type-checked, corresponding to either:

        * The ``--beartype-packages`` option passed to the ``pytest`` command.
        * The ``beartype_packages`` option in user-defined ``pyproject.toml``
          and ``pytest.ini`` files.
    skip_package_names : tuple[str, ...]
        Tuple of the fully-qualified names of *all* packages and modules to
        *not* be type-checked by beartype, corresponding to either:

        * The ``--beartype-skip-packages`` option passed to the ``pytest``
          command.
        * The ``beartype_skip_packages`` option in user-defined
          ``pyproject.toml`` and ``pytest.ini`` files.
    '''

    # ....................{ LOCALS                         }....................
    # True only if the caller embedded a star import (i.e., "*" character)
    # inside the list of package names to be type-checked, requesting that *ALL*
    # packages and modules be unconditionally type-checked.
    is_beartype_packages_all = '*' in package_names

    # ....................{ IMPORTED PACKAGES              }....................
    # Tuple of the fully-qualified names of all previously imported packages and
    # modules, initialized by the conditional below.
    package_imported_names: tuple[str, ...] = ()

    # If the user requests that *ALL* packages and modules be type-checked...
    if is_beartype_packages_all:
        # Frozen set of all package names to be explicitly ignored (rather than
        # type-checked by "beartype.claw" import hooks registered below).
        package_names_ignorable = (
            _PACKAGE_NAMES_IGNORABLE |
            # Note that:
            # * The standard "sys.stdlib_module_names" global is a frozenset.
            # * The standard "sys.builtin_module_names" global is a *TUPLE*
            #   rather than a frozenset. Why? No idea. Both globals should have
            #   been defined to be frozensets. Thanks a lot, Python interpreter.
            module_names_stdlib |
            frozenset(module_names_builtin)
        )

        # Generator over the fully-qualified names of all (possibly ignorable)
        # previously imported packages and modules.
        package_names_imported = sorted({
            module.partition('.')[0] for module in module_names_imported})

        # Tuple of the fully-qualified names of all *UNIGNORABLE* packages and
        # modules previously imported under the active Python interpreter.
        package_imported_names = tuple(
            package_name_imported
            for package_name_imported in package_names_imported
            if package_name_imported not in package_names_ignorable
        )
    # Else, the user requests that only specific packages and modules be
    # type-checked. In this case...
    else:
        # Tuple of the fully-qualified names of the subset of these packages and
        # modules that have been previously imported under the active Python
        # interpreter.
        package_imported_names = tuple(
            package_name
            for package_name in package_names
            if package_name in module_names_imported
        )

    # If one or more packages to be type-checked have already been imported...
    if package_imported_names:
        # Comma-delimited double-quoted string listing these packages. Yeah!
        package_imported_names_str = join_delimited(
            strs=package_imported_names,
            delimiter_if_two=' and ',
            delimiter_if_three_or_more_nonlast=', ',
            delimiter_if_three_or_more_last=', and ',
            is_double_quoted=True,
        )

        # Emit a non-fatal warning informing the user.
        warn(
            (
                f'Previously imported packages and modules '
                f'{package_imported_names_str} uncheckable by beartype.'
            ),
            BeartypePytestWarning,
            stacklevel=1,  # <-- dark magic glistens dangerously
        )
    # Else, none of these packages have already been imported.

    # ....................{ HOOKS                          }....................
    # Beartype configuration excluding the passed packages and modules from
    # being type-checked by "beartype.claw" import hooks registered below.
    beartype_conf = BeartypeConf(claw_skip_package_names=skip_package_names)
    # print(f'Hooking packages {repr(package_names)} (skipping {repr(skip_package_names)})...')

    # If the caller embedded a star import (i.e., "*" character) inside the list
    # of package names to be type-checked, unconditionally reduce to
    # type-checking *ALL* imports via the catch-all import hook.
    if is_beartype_packages_all:
        beartype_all(conf=beartype_conf)
    # Else, the caller did *NOT* embed a star import (i.e., "*" character)
    # inside the list of package names to be type-checked. In this case,
    # conditionally type-check only these listed packages.
    else:
        beartype_packages(package_names, conf=beartype_conf)

# ....................{ PRIVATE ~ globals                  }....................
_PACKAGE_NAMES_IGNORABLE = frozenset((
    '__main__',
    '_pytest',
    'beartype',
    'cmd',
    'code',
    'codeop',
    'iniconfig',
    'pluggy',
    'py',
    'pytest',
    'pytest_beartype',
    'rlcompleter',
    'sys',
    'typing',
    'warnings',
))
'''
Frozen set of the names of all **ignorable packages** (i.e., packages to be
ignored by the :func:`beartype.claw.beartype_all` import hook invoked by a user
passing the ``--beartype-packages='*'`` command-line option).
'''
