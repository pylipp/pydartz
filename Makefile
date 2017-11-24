.PHONY: all test clean install lint

all:
	@echo "Available targets: install, test"

install:
	pip install -U -r requirements.txt -e .

test:
	@[ -z $$VIRTUAL_ENV ] && echo "Acticate pydarts virtualenv." || python -m unittest discover

lint:
	find pydarts -name "*.py" | xargs pylint
	find test -name "*.py" | xargs pylint
