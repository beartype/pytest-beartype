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

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -e .[dev]` to do an editable install
- Run `pytest` to run tests
- Run `tox` to run tests for each Python version supported. This is ran as part of GitHub Actions.

## Type Checking

Run `mypy .`
