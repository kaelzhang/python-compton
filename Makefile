test:
	pytest -s -v test/test_*.py --doctest-modules --cov compton --cov-config=.coveragerc --cov-report term-missing

install:
	pip install -r requirements.txt -r test-requirements.txt

lint:
	flake8 compton test *.py

fix:
	autopep8 --in-place --aggressive -r compton test *.py

report:
	codecov

build: compton
	rm -rf dist
	python setup.py sdist bdist_wheel

start:
	python start.py

dev:
	SERVER_PORT=8081 python start.py

# publish:
# 	make build
# 	twine upload --config-file ~/.pypirc -r pypi dist/*

.PHONY: test
