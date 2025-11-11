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
# CAUTION: Avoid importing from *ANY* packages at global scope to improve pytest
# startup performance. The sole exception is the "pytest" package itself. Since
# pytest has presumably already imported and run this plugin, the "pytest"
# package has presumably already been imported. Ergo, importing from that
# package yet again incurs no further costs.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ....................{ IMPORT HOOKS                       }....................
def check_packages_on_import(
    package_names: list[str], skip_package_names: list[str]) -> None:
    '''
    Register a new :mod:`beartype.claw` import hook automatically type-checking
    *all* of the packages and modules with the passed names (excluding *all* of
    the skipped packages and modules with the passed names) subsequently
    imported during :mod:`pytest` test execution with :func:`beartype.beartype`.

    Parameters
    ----------
    package_names : list[str]
        Comma-delimited string listing the fully-qualified names of *all*
        packages and modules to be type-checked, corresponding to
        either:

        * The ``--beartype-packages`` option passed to the ``pytest`` command.
        * The ``beartype_packages`` option in user-defined ``pyproject.toml``
          and ``pytest.ini`` files.
    skip_package_names : list[str]
        Comma-delimited string listing the fully-qualified names of *all*
        packages and modules to *not* be type-checked by beartype,
        corresponding to either:

        * The ``--beartype-skip-packages`` option passed to the ``pytest``
          command.
        * The ``beartype_skip_packages`` option in user-defined ``pyproject.toml``
          and ``pytest.ini`` files.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer global imports to improve "pytest" startup performance.
    from beartype import BeartypeConf
    from beartype.claw import (
        beartype_all,
        beartype_packages,
    )
    from beartype.roar import BeartypeWarning
    from beartype._util.text.utiltextjoin import join_delimited

    # Standard lists of module names, used to filter out already-imported
    # modules from the warning message (about the fact that some modules have
    # already been imported and will not be checked) if the user passes one or
    # both of the "--beartype-packages='*'" or "--beartype-skip-packages=..."
    # command-line options.
    from sys import (
        builtin_module_names as module_names_builtin,
        modules              as module_names_imported,
        stdlib_module_names  as module_names_stdlib,
    )

    # ....................{ CLASSES                        }....................
    class BeartypePytestWarning(BeartypeWarning):
        '''
        Beartype :mod:`pytest` warning.

        This warning is emitted at :mod:`pytest` configuration time when one
        or more packages or modules to be type-checked have already been
        imported under the active Python interpreter.
        '''

    # ....................{ IMPORTED                       }....................
    # Tuple of the subset of these names corresponding to previously
    # imported packages and modules under the active Python interpreter.
    if '*' in package_names:
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

        package_names_imported = sorted({
            module.partition('.')[0] for module in module_names_imported})

        package_imported_names = tuple(
            package_name_imported
            for package_name_imported in package_names_imported
            if package_name_imported not in package_names_ignorable
        )
    else:
        package_imported_names = tuple(
            package_name
            for package_name in package_names
            if package_name in module_names_imported
        )

    # If one or more of these packages have already been imported...
    if package_imported_names:
        # Defer global imports to improve "pytest" startup performance.
        from warnings import warn

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
                f'Previously imported packages '
                f'{package_imported_names_str} not checkable by beartype.'
            ),
            BeartypePytestWarning,
            stacklevel=1,  # <-- dark magic glistens dangerously
        )
    # Else, none of these packages have already been imported.

    # ....................{ IMPORT HOOK                    }....................
    #FIXME: Is the coercion to "tuple" really necessary here? *sigh*
    beartype_conf = BeartypeConf(
        claw_skip_package_names=tuple(skip_package_names))
    # print(f'Hooking packages {repr(package_names)} (skipping {repr(skip_package_names)})...')

    # If the caller embedded a star import (i.e., "*" character) inside the list
    # of package names to be type-checked, unconditionally reduce to
    # type-checking *ALL* imports via the catch-all import hook.
    if '*' in package_names:
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
