install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=python_oop_project_101 --cov-report xml

lint:
	poetry run flake8 python_oop_project_101

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: install test lint selfcheck check build
