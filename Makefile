include .env
export

# Runs linters
.PHONY: lint
lint:
	@ruff check --fix
	@ruff format
	@mypy --config-file pyproject.toml .


# Builds the library
.PHONY: build
build:
	@rm -rf dist
	@poetry build

# Starts the API server
.PHONY: publish
publish:
	@make _check_pip_configuration
	@twine upload --verbose --repository-url https://us-central1-python.pkg.dev/cumplo-scraper/cumplo-pypi/ dist/*

# Checks if the pip configuration file exists in the virtual environment
.PHONY: _check_pip_configuration
_check_pip_configuration:
	@if [ ! -f .venv/pip.conf ]; then \
		echo "ERROR: pip.conf not set properly for publishing this library"; \
		exit 1; \
	fi

# Logs into Google Cloud
.PHONY: login
login:
	@gcloud config configurations activate $(PROJECT_ID)
	@gcloud auth application-default login
