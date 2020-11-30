.PHONY: test build install clean todo

help:
	# Print help documentation
	@echo "This makefile holds the following targets"
	@echo "  help                        Print help documentation"
	@echo "  black                       Run Python's Black formatter on the code"
	@echo "  build                       Build the Project (using setuptools)"
	@echo "  clean                       Clean Python Package Data (Tests/Eggs/Cache)"
	@echo "  install                     Install the python package locally for testing"
	@echo "  mypy                        Run Python's Mypy type checker on the code"
	@echo "  pylint                      Run Python's Pylint syntax checker on the code"
	@echo "  test                        Test the python package (using setuptools and pytest)"
	@echo "  test_unit                   Run Unit Tests (using setuptools and pytest)
	@echo "  test_integration            Run Integration Tests (using setuptools and pytest)
	@echo "  todo                        Get project TODOs"


###
# Development Steps
###


test: test_unit test_integration
	# Test the python package (using setuptools and pytest)

test_unit:
	# Run Unit Tests (using setuptools and pytest)
	python3 setup.py test --addopts="-m 'not integration' --cov-config=.coveragerc --cov-report=html --cov-report=term --cov=magicwand --html=test_report/unit.html"

test_integration:
	# Run Integration Tests (using setuptools and pytest)
	python3 setup.py test --addopts="-m 'integration' --html=test_report/integration.html"

todo:
	# Get all package TODOs
	grep -rE "TODO" . | egrep .py | egrep -v .html | egrep -v .eggs | egrep -v .pyc

mypy:
	# Run Mypi on the package
	mypy --config-file=.mypy.ini

pylint:
	# Run Pylint on the package
	pylint --rcfile=.pylintrc --output-format=colorized magicwand

black:
	# Run Black on the package
	black --config=pyproject.toml magicwand


###
# Buid Process
###


build: test
	# Build the Project (using setuptools)
	python3 setup.py build


###
# Install
###


install:
	# Install the python package locally for testing
	pip3 install --editable .


###
# Cleanup Process
###


clean:
	# Clean Python Package Data (Tests/Eggs/Cache)
	rm -rf *.egg* .eggs .pytest_cache/ test_report/ .coverage build/ htmlcov/
	find . -name '__pycache__' -type d | xargs rm -fr
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
