
#
# Aliases
#
_VENV := $(VIRTUAL_ENV)

# if we're not running in a virtual environment
ifeq ($(strip $(_VENV)),)
SERVICER := ./servicer
GRPC := ./servicer_grpc
SCRIPTS := ./scripts
endif
# else
ifneq ($(strip $(_VENV)),)
SERVICER := $(VIRTUAL_ENV)/../servicer
GRPC := $(VIRTUAL_ENV)/../servicer_grpc
SCRIPTS := $(VIRTUAL_ENV)/../scripts
endif

#
#	Commands
#

docs:
	. venv/bin/activate && \
	cd $(SERVICER)/docs/ && make html
	
	. venv/bin/activate && \
	cd $(GRPC)/docs/ && make html

check:
	. venv/bin/activate && \
	pre-commit run --all-files

test:
	. venv/bin/activate && \
	pytest -c $(SERVICER)/pyproject.toml $(SERVICER)/tests
	
	. venv/bin/activate && \
	pytest -c $(GRPC)/pyproject.toml $(GRPC)/tests

#
# Setup functions
#

#
# This function is called to setup the environment variables
# Each repo will have additional variables that need to be added to the script
#
setup-shell:
	. scripts/setup-env.sh

setup-venv:
	python3 -m venv venv

setup-python:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install pyclean

setup-pre-commit:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install pre-commit && \
	pre-commit install && \
	pre-commit install --hook-type commit-msg && \
	pre-commit install --hook-type pre-push

setup-all: setup-venv setup-shell
	. venv/bin/activate && \
	make setup-python && \
	make setup-pre-commit

#
# Install functions
#
#
install-servicer-docs:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install ./servicer[docs]

install-servicer-test:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install ./servicer[test]

# NOTE:  Only dev is editable
install-servicer-dev:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -e ./servicer[dev,test,docs]

# Just plain install
install-servicer:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install ./servicer

install-grpc-docs:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -e ./servicer_grpc[docs]

install-grpc-test:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install ./servicer_grpc[test]

install-grpc-dev:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -e ./servicer_grpc[dev,test,docs]

install-grpc:
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install ./servicer_grpc

install-github-check:
ifeq ($(strip $(_VENV)),)
	pip install --upgrade pip && \
	pip install pre-commit && \
	pip install -e ./servicer/[test,dev] &&\
	pip install -e ./servicer_grpc/[test,dev]
endif
# else
ifneq ($(strip $(_VENV)),)
	echo "WARNING:  !!!  This should not be run in a virtual environment.  Only github actions.  !!!"
endif

# alias to help install
install-all-docs: install-servicer-docs install-grpc-docs

install-all-test: install-servicer-test install-grpc-test

install-all-dev: install-servicer-dev install-grpc-dev

install-all: install-servicer install-grpc

#
# Clean functions
#
clean:
	. venv/bin/activate && \
	pyclean . && \
	pre-commit clean && \
	for folder in [ .mypy_cache .pytest_cache .coverage .hypothesis *.egg-info dist build _build ] ; do \
		find . -name $$folder -not -path "./venv/*" | xargs rm -rf ; \
	done
	rm -rf ~/Library/Caches/pylint
	rm -rf ~/.pylint.d
	

clean-venv:
	. venv/bin/activate && \
	pip freeze > .requirements.txt && pip uninstall -r .requirements.txt -y && \
	rm .requirements.txt

#
# Docker builds
#
docker-build:
	docker build -t service_template --secret id=PASSPORT_CI_TOKEN -f ./servicer/Dockerfile . 

docker-run:
	docker run --publish 50051:50051 -t service_template
