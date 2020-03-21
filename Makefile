files = compton test

test:
	pytest -s -v test/test_*.py --doctest-modules --cov compton --cov-config=.coveragerc --cov-report term-missing

install:
	pip install -r test-requirements.txt

lint:
	flake8 $(files)

fix:
	autopep8 --in-place -r $(files)

report:
	codecov

build:
	rm -rf dist
	python setup.py sdist bdist_wheel

publish:
	make build
	twine upload --config-file ~/.pypirc -r pypi dist/*

.PHONY: test build
