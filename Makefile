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
	@poetry run twine upload --verbose --repository-url https://us-central1-python.pkg.dev/cumplo-scraper/cumplo-pypi/ dist/*

# Logs into Google Cloud
.PHONY: login
login:
	@gcloud config configurations activate $(PROJECT_ID)
	@gcloud auth application-default login

.PHONY: unit
unit:
	@set -o allexport; source .env; set +o allexport
	@pytest tests/unit
