VERSION=$(shell python -c "import pydartz; print(pydartz.__version__)")

# Make sure we're on the master branch
ifneq "$(shell git rev-parse --abbrev-ref HEAD)" "master"
$(error Not on master branch)
endif

.PHONY: all test clean install lint upload tag publish

all:
	@echo "Available targets: install, test, lint, publish"

install:
	pip install -U -e .[develop,audio]

test:
	@$$WORKON_HOME/pydartz/bin/python -m unittest discover
	@$$WORKON_HOME/pydartz-py2/bin/python -m unittest discover

lint:
	find pydartz -name "*.py" | xargs pylint
	find test -name "*.py" | xargs pylint

README.rst: README.md
	pandoc README.md -o README.rst
	python setup.py check -r

upload: README.rst setup.py
	rm -f dist/*
	python setup.py bdist_wheel --universal
	twine upload dist/*

tag:
	git tag v$(VERSION)
	git push --tags

publish: tag upload

coverage:
	@for f in test/test_*.py; do coverage run -a $$f; done
	coverage report

coverage-html: coverage
	coverage html
	xdg-open htmlcov/index.html
