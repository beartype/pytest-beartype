#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2024-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Project **metaverse** (e.g., submodule exporting scalar global constants safely
describing this package *without* requiring first- or third-party imports from
potentially unsafe external packages or modules residing outside this package).
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAUTION: Avoid importing from *ANY* first- or third-party package or module.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from pytest_beartype._util.text.utiltextversion import (
    convert_str_version_to_tuple as _convert_str_version_to_tuple)

# ....................{ METADATA                           }....................
NAME = 'pytest-beartype'
'''
Human-readable project name.
'''

# ....................{ METADATA ~ package                 }....................
PACKAGE_NAME = NAME.replace('-', '_')
'''
Fully-qualified name of the top-level Python package containing this submodule.
'''


PACKAGE_TEST_NAME = f'{PACKAGE_NAME}_test'
'''
Fully-qualified name of the top-level Python package testing this project.
'''

# ....................{ METADATA ~ version                 }....................
VERSION = '0.3.0'
'''
Human-readable package version as a ``.``-delimited string.
'''


VERSION_PARTS = _convert_str_version_to_tuple(VERSION)
'''
Machine-readable package version as a tuple of integers.
'''

# ....................{ METADATA ~ urls                    }....................
# Although feasible, parsing URLs from "_package_metadata" is non-trivial.
# Rather than break our body over something nobody cares about, violate the DRY
# (Don't Repeat Yourself) principle by repeating various URLs already specified
# in our top-level "pyproject.toml" file.

# ....................{ METADATA ~ urls : repo             }....................
URL_REPO_ORG_NAME = PACKAGE_NAME
'''
Name of the **organization** (i.e., parent group or user principally responsible
for maintaining this project, indicated as the second-to-last trailing
subdirectory component) of the URL of this project's git repository.
'''


URL_REPO_BASENAME = PACKAGE_NAME
'''
**Basename** (i.e., trailing subdirectory component) of the URL of this
project's git repository.
'''


URL_REPO = f'https://github.com/{URL_REPO_ORG_NAME}/{URL_REPO_BASENAME}'
'''
URL of this project's git repository.
'''


URL_DOWNLOAD = f'{URL_REPO}/archive/{VERSION}.tar.gz'
'''
URL of the source tarball for the current version of this project.

This URL assumes a tag whose name is ``v{VERSION}`` where ``{VERSION}`` is the
human-readable current version of this project (e.g., ``v0.4.0``) to exist.
Typically, no such tag exists for live versions of this project -- which
have yet to be stabilized and hence tagged. Hence, this URL is typically valid
*only* for previously released (rather than live) versions of this project.
'''


URL_FORUMS = f'{URL_REPO}/discussions'
'''
URL of this project's user forums.
'''


URL_ISSUES = f'{URL_REPO}/issues'
'''
URL of this project's issue tracker.
'''


URL_RELEASES = f'{URL_REPO}/releases'
'''
URL of this project's release list.
'''
