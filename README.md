<!-- ---------------( LICENSE                              )--------------------
Copyright (c) 2024-2025 Beartype authors.
See "LICENSE" for further details.

--------------------( MAIN                                 )--------------------
-->

![](https://raw.githubusercontent.com/beartype/beartype-assets/main/banner/logo.png)

[![tests](https://github.com/beartype/pytest-beartype/actions/workflows/python_test.yml/badge.svg)](https://github.com/beartype/pytest-beartype/actions/workflows/python_test.yml)

# `pytest-beartype`: Type-check All the [Pytest][] Things

<!-- FIXME: Also document below how users can *DISABLE* this plugin: e.g.,
  # In "pytest.ini":
  addopts = -p no:beartype
-->

`pytest-beartype` is a [pytest][] plugin type-checking tests, fixtures, and your
packages at test-time with [@beartype][]:

> The unbearably fast near-real-time pure-Python runtime-static type-checker.

`pytest-beartype` is [portably implemented][codebase] in [Python 3][Python],
[continuously stress-tested][tests] via [GitHub Actions][] **×** [tox][] **×**
[pytest][], and [permissively distributed](#license) under the [MIT license][].
`pytest-beartype` has only two runtime dependencies ([pytest][] and
[@beartype][], unsurprisingly) and *no* test-time dependencies.
`pytest-beartype` supports *all* [actively developed Python versions][Python
status] and *all* [Python package managers](#installation).

## Installation

`pytest-beartype` supports your favourite Python package managers! It better.

* Via [uv][], the newest upstart to emerge victorious in the battle of wills:

  ```bash
  uv add pytest-beartype       # <-- by the power of ultraviolet radiation
  ```

* Via [pip][], the once-great venerable master now fallen on hard times:

  ```bash
  pip install pytest-beartype  # <-- sometimes the old ways are still okay
  ```

`pytest-beartype`: QA without doing anything.

## Usage

`pytest-beartype` does *nothing* by default. This plugin only type-checks your
external packages, your [pytest][] tests, and your [pytest][] fixtures when you
tell it to – for your safety and the safety of the code you test:

* Type-check everything at the command line! `(◕‿◕✿)`

  ```bash
  $ pytest --beartype-tests --beartype-fixtures \
      --beartype-packages="my_package,your_package" \
      --beartype-skip-packages="my_package.my_bad_submodule,your_bad_package"
  ```

* Type-check everything from [`pyproject.toml`][pyproject.toml]! `(◡‿◡✿)`

  ```toml
  [tool.pytest.ini_options]
  beartype_tests = true
  beartype_fixtures = true
  beartype_packages = ["my_package", "your_package"]
  beartype_skip_packages = ["my_package.my_bad_submodule", "your_bad_package"]
  ```

* Type-check everything from [`pytest.ini`][pytest.ini]! `(❀◦‿◦)`

  ```ini
  [pytest]
  beartype_tests = true
  beartype_fixtures = true
  beartype_packages = my_package your_package
  beartype_skip_packages = my_package.my_bad_submodule your_bad_package
  ```

Would you like to know more? Continue reading for details that may bore you.

## Features

`pytest-beartype` configurably type-checks any combination of [pytest][] tests,
[pytest][] fixtures, and one or more arbitrary [Python][] packages through
plugin-specific options either temporarily passed to the [`pytest`
command][pytest command] *or* permanently set from within project-specific
[`pyproject.toml`][pyproject.toml] and [`pytest.ini`][pytest.ini] configuration
files:

| **Type-check**    | **CLI Option**                                   | **`pyproject.toml` Option**                          | **`pytest.ini` Option**                          |
|-------------------|--------------------------------------------------|------------------------------------------------------|--------------------------------------------------|
| *All* tests       | `--beartype-tests`                               | `beartype_tests = true`                              | `beartype_tests = true`                          |
| *All* fixtures    | `--beartype-fixtures`                            | `beartype_fixtures = true`                           | `beartype_fixtures = true`                       |
| One package       | `--beartype-packages=my_package`                 | `beartype_packages = ["my_package"]`                 | `beartype_packages = my_package`                 |
| Multiple packages | `--beartype-packages="my_package,your_package"`  | `beartype_packages = ["my_package", "your_package"]` | `beartype_packages = my_package your_package`    |
| Exclude packages  | `--beartype-skip-packages=my_package.bad_module` | `beartype_skip_packages = ["my_package.bad_module"]` | `beartype_skip_packages = my_package.bad_module` |

Would you like to know more? No? Oh. Okay... **wait.** What? Really? You really
would like to no more? You should be bored out of your mind already! How can you
still be reading this? How can I even still be typing this!? 😮

`pytest-beartype`: *Let's get this QA party started.*

### Type-check Tests

By default, `pytest-beartype` type-checks *no* tests inside your test suite.
Configure `pytest-beartype` to type-check *all* your tests (including *all*
parameters and fixtures passed to tests) inside your test suite:

* By passing the `--beartype-tests` option to the [`pytest`
  command][pytest command]:

  ```bash
  pytest --beartype-tests
  ```

* By setting the `beartype_tests = true` option in your
  [`pyproject.toml` file][pyproject.toml]:

  ```toml
  [tool.pytest.ini_options]
  beartype_tests = true
  ```

* By setting the `beartype_tests = true` option in your
  [`pytest.ini` file][pytest.ini]:

  ```ini
  beartype_tests = true
  ```

`pytest-beartype`: QA is made of this.

### Type-check Fixtures

By default, `pytest-beartype` type-checks *no* fixtures inside your test suite.
Configure `pytest-beartype` to type-check *all* your fixtures (including *all*
parameters passed to and values returned from those fixtures as well as other
fixtures required by those fixtures) inside your test suite:

* By passing the `--beartype-fixtures` option to the [`pytest`
  command][pytest command]:

  ```bash
  pytest --beartype-fixtures
  ```

* By setting the `beartype_fixtures = true` option in your
  [`pyproject.toml` file][pyproject.toml]:

  ```toml
  [tool.pytest.ini_options]
  beartype_fixtures = true
  ```

* By setting the `beartype_fixtures = true` option in your
  [`pytest.ini` file][pytest.ini]:

  ```ini
  beartype_fixtures = true
  ```

`pytest-beartype`: Who is `pytest` to disagree?

### Type-check Packages

By default, `pytest-beartype` type-checks *no* packages outside your test suite.
If your packages are already internally type-checked by [@beartype][], no
problem. Your packages *are* internally type-checked by [@beartype][], aren't
they!? Uh oh. 😫

Maybe... *not*. Maybe you have justifiable usability or efficiency concerns.
Maybe you prefer to only conditionally type-check your packages by [@beartype][]
while running tests and *only* while running tests. Maybe this is you. Fear not,
fellow QA person! `pytest-beartype` is here to type-check your dreams.

Configure `pytest-beartype` to either...

#### Type-check a Single Package

Type-check a **single package** (e.g., yours) while running tests:

* By passing the `--beartype-packages={package_name}` option to the [`pytest`
  command][pytest command]:

  ```bash
  pytest --beartype-packages=muh_package_name
  ```

* By setting the `beartype_packages = ["{package_name}"]` option in your
  [`pyproject.toml` file][pyproject.toml]:

  ```toml
  [tool.pytest.ini_options]
  beartype_packages = ["muh_package_name"]
  ```

* By setting the `beartype_packages = {package_name}` option in your
  [`pytest.ini` file][pytest.ini]:

  ```ini
  beartype_packages = muh_package_name
  ```

`pytest-beartype`: Because life's already too complicated.

#### Type-check Two or More Packages

Type-check **two or more packages** (e.g., yours) while running tests:

* By passing the
  `--beartype-packages="{first_package_name},...,{last_package_name}"` option
  as a comma-delimited list to the [`pytest` command][pytest command]:

  ```bash
  pytest --beartype-packages='muh_package_name,muh_other_package_name'
  ```

* By setting the `beartype_packages = ["{first_package_name}", ...,
  "{last_package_name}"]` option as a comma-delimited list in your
  [`pyproject.toml` file][pyproject.toml]:

  ```toml
  [tool.pytest.ini_options]
  beartype_packages = ["muh_package_name", "muh_other_package_name"]
  ```

* By setting the `beartype_packages = {first_package_name} ...
  {last_package_name}` option as a **whitespace**-delimited list in your
  [`pytest.ini` file][pytest.ini]:

  ```ini
  beartype_packages = muh_package_name muh_other_package_name
  ```

`pytest-beartype`: Because code's already too complicated, too.

#### Type-check All Packages

Type-check **all packages** transitively imported anywhere while running tests.
Type-check your entire app stack at test time! Only the brave, the foolhardy,
and the desperate need apply:

* By passing the `--beartype-packages="*"` option to the [`pytest`
  command][pytest command].

  ```bash
  pytest --beartype-packages='*'
  ```

  > **CAUTION:** The `"*"` character should typically be single- or
  > double-quoted to prevent your shell from erroneously expanding that as a
  > pathname glob.

* By setting the `beartype_packages = ["*"]` option in your [`pyproject.toml`
  file][pyproject.toml]:

  ```toml
  [tool.pytest.ini_options]
  beartype_packages = ["*"]
  ```

* By setting the `beartype_packages = *` option in your [`pytest.ini`
  file][pytest.ini]:

  ```ini
  beartype_packages = *
  ```

> **CAUTION:** You may need to omit problematic packages by also passing the
> `--beartype-skip-packages` option to the [`pytest` command][pytest command]
> command *or* setting the `beartype_skip_packages` option in your
> [`pyproject.toml`][pyproject.toml] or [`pytest.ini`][pytest.ini] files. See
> below for further commentary that will bore you into oblivion.

### Avoid Type-checking Some Packages

By default, `pytest-beartype` type-checks *all* subpackages and submodules of
packages explicitly listed by passing the `--beartype-packages` option to the
[`pytest` command][pytest command] command *or* setting the `beartype_packages`
option in your [`pyproject.toml`][pyproject.toml] or [`pytest.ini`][pytest.ini]
files.

Ideally, that's fine. Ideally, your packages are all type-checkable in entirety.
But what if that's not fine? This is the real world over here. What if you're
type-checking *all* packages in your app stack with `--beartype-packages="*"`,
for example, and one or more of those packages (or their subpackages or
submodules) fail type-checking? What then, huh?

Configure `pytest-beartype` to *not* type-check one or more of these
(sub)packages or (sub)modules while running tests:

* By passing the
  `--beartype-skip-packages="{first_package_name},...,{last_package_name}"`
  option to the [`pytest` command][pytest command].

  ```bash
  pytest --beartype-skip-packages="muh_package.muh_bad_submodule,muh_bad_package"
  ```

* By setting the `beartype_skip_packages = ["{first_package_name}", ...,
  "{last_package_name}"]` option in your [`pyproject.toml`
  file][pyproject.toml]:

  ```toml
  [tool.pytest.ini_options]
  beartype_skip_packages = ["muh_package.muh_bad_submodule", "muh_bad_package"]
  ```

* By setting the `beartype_skip_packages = {first_package_name} ...
  {last_package_name}` option as a **whitespace**-delimited list in your
  [`pytest.ini` file][pytest.ini]:

  ```ini
  beartype_skip_packages = muh_package.muh_bad_submodule muh_bad_package
  ```

`pytest-beartype`: That'll do, GitHub. That'll do.

## License

`pytest-beartype` is [open-source software released][license] under the
[permissive MIT license][MIT license].

## Security

`pytest-beartype` encourages security researchers, institutes, and concerned
netizens to [responsibly disclose security vulnerabilities as GitHub-originated
Security Advisories][security] – published with full acknowledgement in the
public [GitHub Advisory Database][].

<!-- ---------------( LINKS ~ self                         )---------------- -->
[codebase]: https://github.com/beartype/pytest-beartype/tree/main/pytest_beartype
[license]: ./LICENSE
[security]: https://github.com/beartype/pytest-beartype/blob/main/.github/SECURITY.md
[tests]: https://github.com/beartype/beartype/actions?workflow=tests

<!-- ---------------( LINKS ~ other                        )---------------- -->
[@beartype]: https://github.com/beartype/beartype
[GitHub Actions]: https://github.com/features/actions
[GitHub Advisory Database]: https://github.com/advisories
[MIT license]: https://opensource.org/licenses/MIT
[pyproject.toml]: https://packaging.python.org/en/latest/guides/writing-pyproject-toml
[Pytest]: https://docs.pytest.org
[pytest]: https://docs.pytest.org
[pytest command]: https://docs.pytest.org/en/stable/how-to/usage.html
[Python]: https://www.python.org
[Python status]: https://devguide.python.org/versions/#versions
[pytest.ini]: https://docs.pytest.org/en/stable/reference/customize.html
[pip]: https://packaging.python.org/en/latest/tutorials/installing-packages
[tox]: https://tox.readthedocs.io
[uv]: https://docs.astral.sh/uv
