.PHONY: all $(MAKECMDGOALS)
DOC_PORT ?= 8030
PROJECT_NAME ?= leetcode
help: # print all the available targets
	@echo "\nAvailable targets:\n"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sed 's/:.*#/\t/' | column -t -s '	' ; echo

install: # install requirements without development dependencies
	uv sync

dev: install-dev  # install requirements with all dependencies that are needed for development
	uv run pre-commit install

install-uv: # install uv tool
	curl -LsSf https://astral.sh/uv/install.sh | sh

install-dev: # install dev dependencies
	uv sync --all-groups

install-test: # install test dependencies
	uv sync --group test

format: # format the code with the ruff tool
	uv run ruff format $(PROJECT_NAME) utils

format-check: # check the formatting code with ruff
	uv run ruff format --check $(PROJECT_NAME) utils

lint: # check the code style
	uv run ruff check $(PROJECT_NAME) utils

lint-fix: # check and fix the code style
	uv run ruff check --fix $(PROJECT_NAME) utils

lint-doc: # check the docstring style
	uv run flake8 $(PROJECT_NAME) utils

doc: # create the project documentation; Build and visualize documentation through a local server
	uv run properdocs serve -f properdocs.yml --dev-addr 0.0.0.0:$(DOC_PORT)
