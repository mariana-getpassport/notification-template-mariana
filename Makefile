
#
# Aliases
#
_VENV := $(VIRTUAL_ENV)

# are we running in a virtual environment?
ifneq ($(strip $(_VENV)),)
  SERVICER := $(_VENV)/../servicer
  GRPC := $(_VENV)/../servicer_grpc
  SCRIPTS := $(_VENV)/../scripts
else
  SERVICER := ./servicer
  GRPC := ./servicer_grpc
  SCRIPTS := ./scripts
endif

# This variable contains the first goal that matches any of the listed goals
# here, else it contains an empty string. The net effect is to filter out
# whether this current run of `make` requires a Python virtual environment.
NEED_VENV := $(or \
  $(findstring docs,$(MAKECMDGOALS)), \
  $(findstring check,$(MAKECMDGOALS)), \
  $(findstring test,$(MAKECMDGOALS)), \
  $(findstring upgrade-pip,$(MAKECMDGOALS)), \
  $(findstring setup-python,$(MAKECMDGOALS)), \
  $(findstring setup-pre-commit,$(MAKECMDGOALS)), \
  $(findstring setup-servicer-docs,$(MAKECMDGOALS)), \
  $(findstring setup-servicer-test,$(MAKECMDGOALS)), \
  $(findstring setup-servicer-dev,$(MAKECMDGOALS)), \
  $(findstring setup-servicer-plain,$(MAKECMDGOALS)), \
  $(findstring setup-grpc-docs,$(MAKECMDGOALS)), \
  $(findstring setup-grpc-test,$(MAKECMDGOALS)), \
  $(findstring setup-grpc-dev,$(MAKECMDGOALS)), \
  $(findstring setup-grpc-plain,$(MAKECMDGOALS)), \
  $(findstring setup-docs,$(MAKECMDGOALS)), \
  $(findstring setup-test,$(MAKECMDGOALS)), \
  $(findstring setup-dev,$(MAKECMDGOALS)), \
  $(findstring setup-plain,$(MAKECMDGOALS)), \
  $(findstring clean,$(MAKECMDGOALS)), \
  $(findstring clean-venv,$(MAKECMDGOALS)) \
)

ifneq ($(NEED_VENV),)
  ifeq ($(origin VIRTUAL_ENV),undefined)
    $(error No Python virtual environment found (required by $(NEED_VENV)))
  endif
endif

#
#	Commands
#

.PHONY: docs-html
docs-html:
	cd $(SERVICER)/docs/ && make html
	cd $(GRPC)/docs/ && make html

.PHONY: docs-md
docs-md:
	cd $(SERVICER)/docs/ && make markdown
	cd $(GRPC)/docs/ && make markdown

.PHONY: check
check:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -c $(SERVICER)/pyproject.toml $(SERVICER)/tests
	pytest -c $(GRPC)/pyproject.toml $(GRPC)/tests

#
# Create virtual environment
#

venv:
	python3 -m venv venv

#
# Setup functions
#

#
# This function is called to setup the environment variables
# Each repo will have additional variables that need to be added to the script
#
.PHONY: setup-shell
setup-shell:
	. scripts/setup-env.sh

.PHONY: upgrade-pip
upgrade-pip:
	pip install --upgrade pip

.PHONY: setup-python
setup-python: upgrade-pip
	pip install pyclean

.PHONY: setup-pre-commit
setup-pre-commit: upgrade-pip
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg
	pre-commit install --hook-type pre-push

.PHONY: setup-servicer-docs
setup-servicer-docs: upgrade-pip
	pip install ./servicer[docs]

.PHONY: setup-servicer-test
setup-servicer-test: upgrade-pip
	pip install ./servicer[test]

# NOTE:  Only dev is editable
.PHONY: setup-servicer-dev
setup-servicer-dev: upgrade-pip
	pip install -e ./servicer[dev,test,docs]

# Just plain install
.PHONY: setup-servicer-plain
setup-servicer-plain: upgrade-pip
	pip install ./servicer

.PHONY: setup-grpc-docs
setup-grpc-docs: upgrade-pip
	pip install -e ./servicer_grpc[docs]

.PHONY: setup-grpc-test
setup-grpc-test:
	pip install --upgrade pip
	pip install ./servicer_grpc[test]

.PHONY: setup-grpc-dev
setup-grpc-dev: upgrade-pip
	pip install -e ./servicer_grpc[dev,test,docs]

.PHONY: setup-grpc-plain
setup-grpc-plain: upgrade-pip
	pip install ./servicer_grpc

.PHONY: setup-github-check
setup-github-check: 
ifeq ($(strip $(_VENV)),)
	pip install --upgrade pip
	pip install pre-commit
	pip install -e ./servicer/[test,dev]
	pip install -e ./servicer_grpc/[test,dev]
else
	$(warning WARNING:  !!!  This should not be run in a virtual environment.  Only github actions.  !!!)
endif

# alias to help setup
.PHONY: setup-docs
setup-docs: setup-python setup-pre-commit setup-servicer-docs setup-grpc-docs

.PHONY: setup-test
setup-test: setup-python setup-pre-commit setup-servicer-test setup-grpc-test

.PHONY: setup-dev
setup-dev: setup-python setup-pre-commit setup-servicer-dev setup-grpc-dev

.PHONY: setup-plain
setup-plain: setup-python setup-pre-commit setup-servicer-plain setup-grpc-plain

#
# Clean functions
#
.PHONY: clean
clean:
	pyclean .
	pre-commit clean
	for folder in [ .mypy_cache .pytest_cache .coverage .hypothesis *.egg-info dist build _build ] ; do \
		find . -name $$folder -not -path "./venv/*" | xargs rm -rf ; \
	done
	rm -rf ~/Library/Caches/pylint
	rm -rf ~/.pylint.d
	

.PHONY: clean-venv
clean-venv:
	pip freeze > .requirements.txt
	pip uninstall -r .requirements.txt -y
	rm .requirements.txt

#
# Docker builds
#
.PHONY: docker-build
docker-build:
	docker build -t service_template --secret id=PASSPORT_CI_TOKEN -f ./servicer/Dockerfile . 

.PHONY: docker-run
docker-run:
	docker run --publish 50051:50051 -t service_template
