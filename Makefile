.PHONY: all test install lint release coverage

all:
	@echo "Available targets: install, test, lint, format, style-check, release, coverage"

install:
	pip install -U -e .[develop,audio]

test:
	python -m unittest

lint:
	pre-commit run --all-files flake8

format:
	pre-commit run --all-files black
	pre-commit run --all-files isort

release:
	git push --tags origin master

coverage:
	coverage erase
	coverage run -m unittest
	coverage report
	coverage html

style-check: format lint
