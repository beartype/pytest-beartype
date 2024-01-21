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

This will ensure that any type annotations in those packages are checked at
runtime, while your tests are running.

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -r requirements-dev.txt` to do an editable install
- Run `pytest` to run tests

## Type Checking

Run `mypy .`

## Create and upload a package to PyPI

Make sure to bump the version in `setup.cfg`.

Then run the following commands:

```bash
rm -rf build dist
python setup.py sdist bdist_wheel
```

Then upload it to PyPI using [twine](https://twine.readthedocs.io/en/latest/#installation):

```bash
twine upload dist/*
```
