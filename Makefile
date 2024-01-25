export PYTHONPATH=$(shell dirname "$(abspath $(lastword $(MAKEFILE_LIST)))")
name:=httpdecho


.PHONY: test
test:
	python3 -m pytest -v


.PHONY: lint
lint:
	python3 -m pylint *.py


.PHONY: build
build:
	python3 -m build


.PHONY: clean
clean:
	-python3 -m coverage erase
	rm -rf site.py build/ dist/ .tox/ .pytest_cache/ .mypy_cache/
	find . -depth \( -name '*.pyc' -o -name '__pycache__' -o -name '__pypackages__' \
		-o -name '*.pyd' -o -name '*.pyo' -o -name '*.egg-info' \
		-o -name '*.py,cover'  \) -exec rm -rf \{\} \;
