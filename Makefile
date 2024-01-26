PYTHON_VERSION := $(shell python -c "print(open('.python-version').read().strip())")
INSTALLED_VERSION := $(shell python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

.PHONY: \
  check_python_version \
  linters \
  setup_venv \
  build \
  publish \
  _check_pip_configuration

# Checks if the installed Python version matches the required version
check_python_version:
	@if [ "$(PYTHON_VERSION)" != "$(INSTALLED_VERSION)" ]; then \
		echo "ERROR: Installed Python version $(INSTALLED_VERSION) does not match the required version $(PYTHON_VERSION)"; \
		exit 1; \
	fi

# Creates a virtual environment and installs dependencies
setup_venv:
	@make check_python_version
	@rm -rf .venv
	@poetry install

# Runs linters
linters:
	@if [ ! -d ".venv" ]; then \
		echo "Virtual environment not found. Creating one..."; \
		make setup_venv; \
	fi

	@poetry run python -m black --check --line-length=120 .
	@poetry run python -m flake8 --config .flake8
	@poetry run python -m pylint --rcfile=.pylintrc --recursive=y --ignore=.venv --disable=fixme .
	@poetry run python -m mypy --config-file mypy.ini .

# Builds the library
build:
	@rm -rf dist
	@poetry build

# Starts the API server
publish:
	@make _check_pip_configuration
	@poetry run twine upload --verbose --repository-url https://us-central1-python.pkg.dev/cumplo-scraper/cumplo-pypi/ dist/*

# Checks if the pip configuration file exists in the virtual environment
_check_pip_configuration:
	@if [ ! -f .venv/pip.conf ]; then \
		echo "ERROR: pip.conf not set properly for publishing this library"; \
		exit 1; \
	fi
