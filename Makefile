.PHONY: all test clean install

all:
	@echo "Available targets: install, test"

install:
	pip install -U -r requirements.txt -e .

test:
	@[ -z $$VIRTUAL_ENV ] && echo "Acticate pydarts virtualenv." || python -m unittest discover
