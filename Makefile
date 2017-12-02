.PHONY: all test clean install lint

all:
	@echo "Available targets: install, test"

install:
	pip install -U -r requirements.txt -e .

test:
	@$$WORKON_HOME/pydarts/bin/python -m unittest discover

lint:
	find pydarts -name "*.py" | xargs pylint
	find test -name "*.py" | xargs pylint
