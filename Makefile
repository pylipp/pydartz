VERSION=$(shell python -c "import pydarts; print(pydarts.__version__)")

# Make sure we're on the master branch
ifneq "$(shell git rev-parse --abbrev-ref HEAD)" "master"
$(error Not on master branch)
endif

.PHONY: all test clean install lint upload tag publish

all:
	@echo "Available targets: install, test, lint, publish"

install:
	pip install -U -r requirements.txt -e .

test:
	@$$WORKON_HOME/pydarts/bin/python -m unittest discover

lint:
	find pydarts -name "*.py" | xargs pylint
	find test -name "*.py" | xargs pylint

README.rst: README.md
	pandoc README.md -o README.rst
	python setup.py check -r

upload: README.rst tag
	rm -f dist/*
	python setup.py bdist_wheel --universal
	twine upload dist/*

tag:
	git tag v$(VERSION)
	git push --tags

publish: tag upload
