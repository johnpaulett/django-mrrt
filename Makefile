SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-print-directory

# ifeq ($(origin .RECIPEPREFIX), undefined)
#   $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
# endif
# .RECIPEPREFIX = >

POETRY := poetry

poetry.lock: pyproject.toml
# If it is a new package, help by generating a lock file,
# but otherwise don't re-run poetry lock automatically as it will upgrade
# packages
	test -f  poetry.lock || $(POETRY) lock
# In case poetry.lock existed before pyproject.toml, update the target
	touch -c poetry.lock

init: poetry.lock
.PHONY: init

dev:
	$(POETRY) run python manage.py runserver
.PHONY: dev

migrate:
	$(POETRY) run python manage.py migrate
.PHONY: migrate

format:
	$(POETRY) run black .
	$(POETRY) run isort .
.PHONY: format

lint:
	$(POETRY) run flake8 .
# FIXME run isort / black in check mode
	$(POETRY) run isort .
.PHONY: lint

# clean, test, lint, mypy
