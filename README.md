# pytest-beartype

Pytest plugin to run your tests with beartype checking enabled.

## Installation

```bash
pip install pytest_beartype
```

## Usage

```bash
pytest --beartype-packages='your_package_name,other_package_name'
```

or, with a single package:
```bash
pytest --beartype-packages=your_package_name
```

or, against all the packages ever mentioned in your code:
```bash
pytest --beartype-packages='*'
```

This will ensure that any type annotations in those packages are checked at
runtime, while your tests are running.

### Checking test functions and fixtures

To enable beartype type-checking on your test functions and fixtures themselves, use the `--beartype-check-tests` option:

```bash
pytest --beartype-packages=your_package_name --beartype-check-tests
```

This option applies beartype decoration to:
- **Test functions**: All collected test functions will have their parameters and return types validated
- **Fixtures**: All fixtures will have their parameters and return types validated at runtime

#### How it works

When `--beartype-check-tests` is enabled:

1. **Test functions**: During test collection, beartype decorators are applied to all test functions
2. **Fixtures**: During fixture setup, beartype decorators are applied to fixture functions. If a beartype violation occurs in a fixture, the test will fail (not error) with a clear error message indicating which fixture caused the violation

#### Configuration

You can also configure this option in your `pytest.ini` file:

```ini
[tool:pytest]
beartype_check_tests = true
```

#### Known limitations

Generator fixtures are currently not supported due to [beartype issue #423](https://github.com/beartype/beartype/issues/423). When a generator fixture is encountered, it will be skipped automatically and a warning will be emitted.

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -e .[dev]` to do an editable install
- Run `pytest` to run tests
- Run `tox` to run tests for each Python version supported. This is ran as part of GitHub Actions.

## Type Checking

Run `mypy .`
