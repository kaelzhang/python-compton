files = compton test
test_files = *

test:
	pytest -s -v test/test_$(test_files).py --doctest-modules --cov compton --cov-config=.coveragerc --cov-report term-missing

install:
	pip install -U .[dev]

lint:
	@echo "\033[1m>> Running ruff... <<\033[0m"
	@ruff check $(files)

fix:
	ruff check --fix $(files)

build:
	rm -rf dist
	python -m build --sdist --wheel

publish:
	make build
	twine upload --config-file ~/.pypirc -r pypi dist/*

.PHONY: test build
