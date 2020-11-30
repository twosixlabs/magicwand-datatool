# Magicwand Tests

*Welcome to the Magicwand tests!*

## Running Magicwand Tests

To run the tests locally, first install the tests-specific requirements with `pip` using the `requirements-test.txt` file:

```
$ pip install -r magicwand-data-generator/requirements-tests.txt
```


Tests can then be run as follows from the project `root`:

```bash
$ make test
```

The Makefile uses the `pytest` runner and testing suite as well as the coverage library.

These are automated tests that are run before each new release
