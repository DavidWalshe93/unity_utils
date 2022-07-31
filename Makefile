SHELL=/bin/bash

# ----------------------------------------------------------------------------
# OS Specific VARS
# ----------------------------------------------------------------------------

ifeq ($(OS), Windows_NT)				# Windows
	SCRIPTS_DIR=./venv/Scripts
else									# Linux/Unix
	SCRIPTS_DIR=./venv/bin
endif

# ----------------------------------------------------------------------------
# VARS
# ----------------------------------------------------------------------------
PYTHON=python
PYTHON_VENV=${SCRIPTS_DIR}/python
PIP=${SCRIPTS_DIR}/python -m pip
PYTEST=${SCRIPTS_DIR}/pytest

MIN_TEST_COVERAGE=0
CODE_DIR_NAME=unity_utils
TESTS_DIR_NAME=tests

BLACK_LINE_LENGTH = 120

# ----------------------------------------------------------------------------
# TARGETS
# ----------------------------------------------------------------------------

#% ----------------------------------------------------------------------------------------
#% Command                         : Information
#% --------------------------------:-------------------------------------------------------

## help                            : Prints this message and exits.
help:
	@sed -n 's/^#% //p' $(MAKEFILE_LIST)
	@sed -n 's/^## //p' $(MAKEFILE_LIST) | sort


## setup                           : Setup the project and install base + test dependencies.
setup: ./venv/pyvenv.cfg

## setup-dev                       : Setup the project and install base, test and dev dependencies.
setup-dev: setup
	${PIP} install -r requirements/dev.txt

## clean                           : Removes venv.
clean:
	rm -rf ./venv

## build                           : Build the project wheel.
build:
	pipx uninstall unity_utils; \
	python ./scripts/update_cli_version.py
	poetry update; \
	poetry build -f wheel; \
	poetry install; \
	echo "Installing `ls dist/ | grep -i ".whl" | sort -r | head -n 1`"; \
	pipx install dist/`ls dist/ | grep -i ".whl" | sort -r | head -n 1` --force

## clear                           : Remove generated files/folders from disk.
clear:
	rm -rf ./Audio;
	rm -rf ./Scripts;
	rm -rf ./Sprites;
	rm -rf ./Docs;
	rm -f README.md

## test                            : Run tests for the project.
test: setup
	${SCRIPTS_DIR}/pytest -vv ${TESTS_DIR_NAME}

## test-coverage                   : Run tests for the project and generate coverage report.
test-coverage: setup
	${SCRIPTS_DIR}/pytest \
	--cov ${CODE_DIR_NAME} \
	--cov-report html:coverage \
	--cov-report xml:coverage.xml \
	--cov-report term-missing \
	--cov-fail-under ${MIN_TEST_COVERAGE} \
	${TESTS_DIR_NAME}

## lint                            : Lint the project.
lint: setup
	${SCRIPTS_DIR}/pylint ${CODE_DIR_NAME}; \
	${SCRIPTS_DIR}/flake8 ${CODE_DIR_NAME}

## format                          : Format the project.
format: setup
	${SCRIPTS_DIR}/black --line-length=${BLACK_LINE_LENGTH} --target-version=py310 ${CODE_DIR_NAME}; \
	${SCRIPTS_DIR}/isort --profile black ${CODE_DIR_NAME}

## bandit                          : Run bandit for the project.
bandit: setup
	${SCRIPTS_DIR}/bandit -r --ini ./.bandit

## tox                             : Run tox for the project.
tox:
	${SCRIPTS_DIR}/tox

## run                             : Run the application
run: setup
	${PYTHON_VENV} main.py

## disable-pc                      : Disable pre-commit hooks for the project.
disable-pc:
	${SCRIPTS_DIR}/pre-commit uninstall

## enable-pc:                      : Enable pre-commit hooks for the project.
enable-pc:
	${SCRIPTS_DIR}/pre-commit install

## run-pc                          : Execute all pre-commit hooks against project.
run-pc:
	${SCRIPTS_DIR}/pre-commit run --all

# ----------------------------------------------------------------------------
# Anonymous Targets
# ----------------------------------------------------------------------------

install-test-deps:
	${PIP} install -r requirements/test.txt

version-lock-test:
	echo '-r base.txt' > requirements/test.txt; \
	${PIP} freeze | grep -iE '^(pytest|pylint|flake8|bandit)' | sort >> requirements/test.txt; \

install-dev-deps:
	${PIP} install -r requirements/dev.txt

version-lock-dev:
	echo '-r test.txt' > requirements/dev.txt; \
	${PIP} freeze | grep -iE '^(pre-commit)'	| sort >> requirements/dev.txt


# ----------------------------------------------------------------------------
# Helper Targets
# ----------------------------------------------------------------------------

./venv/pyvenv.cfg:
	${PYTHON} -m venv venv; \
	${PIP} install --upgrade pip; \
	${PIP} install -r requirements/test.txt