.PHONY: all test install lint release coverage

all:
	@echo "Available targets: install, test, format, lint, release, coverage"

install:
	pip install -U -e .[develop,audio]

test:
	python -m unittest

format:
	black pydartz/*.py test/*.py

lint:
	find pydartz -name "*.py" | xargs pylint
	find test -name "*.py" | xargs pylint

release:
	git push --tags origin master

coverage:
	coverage erase
	coverage run -m unittest
	coverage report
	coverage html
