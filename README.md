<!-- ---------------( LICENSE                              )--------------------
Copyright (c) 2024-2025 Beartype authors.
See "LICENSE" for further details.

--------------------( MAIN                                 )--------------------
-->

![](https://raw.githubusercontent.com/beartype/beartype-assets/main/banner/logo.png)

![](https://github.com/beartype/pytest-beartype/workflows/test/badge.svg)

# `pytest-beartype`: Type-check All the [Pytest][] Things

[Pytest][] plugin type-checking tests, fixtures, and/or arbitrary packages
(usually, your codebase) at test-time with [@beartype][]:

> The unbearably fast near-real-time pure-Python runtime-static type-checker.

<!-- FIXME: Add additional discussion here resembling our current "README.rst"
introduction for @beartype itself, please. -->

## Installation

<!-- FIXME: Democratize with reference to "uv" too, please. -->

```bash
pip install pytest-beartype
```

**Congrats.** `pytest-beartype` now type-checks *all* [pytest][] tests and
fixtures. Continue reading if you'd like to disable that or type-check external
packages (typically, yours) when running tests, too.

## Usage

<!-- FIXME: Consider splitting out a new "--beartype-ignore-fixtures" option for
disambiguity. -->

`pytest-beartype` configurably type-checks:

* *All* [pytest][] **tests** and **fixtures** across your entire test suite.
  This is:
  * **Enabled by default.**
  * Disabled by `--beartype-ignore-tests` and `beartype_ignore_tests`.
* Zero or more **external packages** while running those tests and fixtures.
  This is:
  * Disabled by default.
  * Enabled by `--beartype-packages` and `beartype_packages`.

Let's get started. Your codebase ain't gonna type-check itself. <sup>*...or is
it!?!*</sup>

### Type-check Packages

By default, `pytest-beartype` type-checks *no* packages outside your test suite.
If your package(s) are already internally type-checked by [@beartype][], that's
fine.

On the other hand, if you'd prefer to conditionally type-check your package(s)
by [@beartype][] while running tests (and *only* while running tests),
configure `pytest-beartype` to...

#### Type-check a Single Package

Type-check a **single package** (e.g., yours) while running tests:

* By passing the `--beartype-packages={package_name}` option to the `pytest`
  command:

  ```bash
  pytest --beartype-packages=muh_package_name
  ```

* By setting the `beartype_packages = ["{package_name}"]` option in your
  `pyproject.toml` file:

  ```toml
  # In "pyproject.toml":
  [tool.pytest.ini_options]
  beartype_packages = ["muh_package_name"]
  ```

* By setting the `beartype_packages = {package_name}` option in your
  `pytest.ini` file:

  ```ini
  # In "pytest.ini":
  beartype_packages = muh_package_name
  ```

`pytest-beartype`: Because life's too complicated.

#### Type-check Two or More Packages

Type-check **two or more packages** (e.g., yours) while running tests:

* By passing the
  `--beartype-packages="{first_package_name},...,{last_package_name}"` option
  as a comma-delimited list to the `pytest` command:

  ```bash
  pytest --beartype-packages='muh_package_name,muh_other_package_name'
  ```

* By setting the `beartype_packages = ["{first_package_name}", ...,
  "{last_package_name}"]` option as a comma-delimited list in your
  `pyproject.toml` file:

  ```toml
  # In "pyproject.toml":
  [tool.pytest.ini_options]
  beartype_packages = ["muh_package_name", "muh_other_package_name"]
  ```

* By setting the `beartype_packages = {first_package_name} ...
  {last_package_name}` option as a **whitespace**-delimited list in your
  `pytest.ini` file:

  ```ini
  # In "pytest.ini":
  beartype_packages = muh_package_name muh_other_package_name
  ```

`pytest-beartype`: Because code's too complicated, too.

#### Type-check All Packages

Type-check **all packages** transitively imported anywhere while running tests.
Type-check your entire app stack at test time! Only the brave, the foolhardy,
and the desperate need apply:

* By passing the `--beartype-packages="*"` option to the `pytest` command.
  **CAUTION:** The `*` character should typically be single- or double-quoted to
  prevent your current shell from erroneously expanding that as a pathname glob:

  ```bash
  pytest --beartype-packages='*'
  ```

* By setting the `beartype_packages = ["*"]` option in your `pyproject.toml`
  file:

  ```toml
  # In "pyproject.toml":
  [tool.pytest.ini_options]
  beartype_packages = ["muh_package_name", "muh_other_package_name"]
  ```

* By setting the `beartype_packages = *` option in your `pytest.ini` file:

  ```ini
  # In "pytest.ini":
  beartype_packages = *
  ```

**CAUTION:** You may need to omit problematic packages by also passing the
`--beartype-skip-packages` option to `pytest` *or* setting the
`beartype_skip_packages` option in `pyproject.toml` or `pytest.ini`. See below
for further commentary.

### Checking test functions and fixtures

By default, beartype type-checking is applied to your test functions and fixtures. To disable this behavior, use the `--beartype-ignore-tests` option:

```bash
pytest --beartype-packages=your_package_name --beartype-ignore-tests
```

When enabled (default), beartype decoration is applied to:
- **Test functions**: All collected test functions will have their parameters and return types validated
- **Fixtures**: All fixtures will be validated according to beartype, and tests requesting fixtures with invalid types will fail.

#### Configuration

You can also configure this option in your `pytest.ini` file:

```ini
[tool:pytest]
beartype_ignore_tests = true
```

#### Known limitations

Generator fixtures are currently not supported due to [beartype issue #423](https://github.com/beartype/beartype/issues/423). Generator fixtures are automatically skipped with a warning message.

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -e .[dev]` to do an editable install
- Run `pytest` to run tests
- Run `tox` to run tests for each Python version supported. This is run as part of GitHub Actions.

## Type Checking

Run `mypy .`

<!-- ---------------( LINKS                                )---------------- -->
[@beartype]: https://github.com/beartype/beartype
[Pytest]: https://docs.pytest.org
[pytest]: https://docs.pytest.org
