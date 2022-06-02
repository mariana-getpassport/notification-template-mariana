![license](https://img.shields.io/badge/license-MIT-blue) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-yellow?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![conventional-commits](https://img.shields.io/badge/conventional%20commits-1.0.0-yellow)](https://www.conventionalcommits.org/en/v1.0.0/) [![black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black) [![mypy](https://img.shields.io/badge/mypy-checked-brightgreen)](http://mypy-lang.org/) [![pylint](https://img.shields.io/badge/pylint-required%2010.0-brightgreen)](http://pylint.org/) [![pytest](https://img.shields.io/badge/pytest-enabled-brightgreen)](https://github.com/pytest-dev/pytest) [![coverage](https://img.shields.io/badge/coverage-required%20100%25-brightgreen)](https://github.com/nedbat/coveragepy)

# Python Service Template

This repository is intended to be a base template, a cookiecutter for a new Python services using GRPC and REST APIs that keeps [PEP518](https://www.python.org/dev/peps/pep-0518/) in mind. It is derived from the Python package project that can be found [locally](https://github.com/getpassport/python-package-template) or [upstream-remote](https://github.com/jenstroeger/python-package-template). Because it’s hosted on Github it already utilizes a few [Github Actions](https://docs.github.com/en/actions) that enforce repository-side checks for continuous integration and that implement a semantic release setup.

This README covers only the _*differences*_ between this project and the Python package template.

## Table of Contents

[Layout differences](#layout-differences)  
[How to use this repository](#how-to-use-this-repository)  
[Setting up after cloning](#setting-up-after-cloning)  
[Makefile commands](#makefile-commands)  
&emsp;[Setup](#setup-commands)  
&emsp;[Install](#install-commands)  
&emsp;[Build and Test](#build-and-test-commands)  
&emsp;[Clean](#clean-commands)  
&emsp;[Docker](#docker-commands)  
[Caveats and Gothcas](#caveats)  
&emsp;[Generating GRPC Files](#generating-grpc-files)

[General Features (shared with package-template)](#general-features-from-python-package-template)  

## Layout differences

The layout of this repository should be respected, the various folders have specific roles:

- *protos*:  This folder contains all the grpc proto files

- *scripts*: This folder contains scripts for setting up the repository locally for development as well as a script for generating the grpc proto files.

- *servicer_grpc*: This folder contains the generated grpc files as well as any support routines that you wish to export to help consumers of the grpc files. This folder generates a new package that can be installed via PIP.

- *servicer*: This folder contains the implementation of the code necessary to handle the grpc calls.  This folder creates a package that can be installe via PIP.


## How to use this repository

If you’d like to contribute to the project template, please open an issue for discussion or submit a pull request.

If you’d like to start your own Python project from scratch, you can either copy the content of this repository into your new project folder or fork this repository. Either way, consider making the following adjustments to your copy:

- Append to this README.md file additional information that developers will need to know in order to build and deploy the service and grpc imports. Each package has a separate _*README*_ which should be updated as well.  For more information about how to write good README files, see this [symbolic link](https://en.wikipedia.org/wiki/Symbolic_link) `README.md`.

- `./scripts/setup-env.sh` - this file contains any specific environment variables necessary for the project.  By default the PASSPORT_CI_TOKEN is written out to the users _*.bash\_profile*_ file.  

- `Makefile` -- contains setup, install and clean steps to get the repo setup for development.  Add any additional steps for setup, installation or cleanup here.

- Adjust the Dependabot settings in `.github/dependabot.yaml` to your desired target branch that you’d like to have monitored by Dependabot.

- `servicer_grpc folder` changes required
    - Reset the package’s version number in `servicer_grpc/src/package_grpc/__init__.py`.
    - Rename the `servicer_grpc/src/package_grpc` folder to whatever your own package grpc's name. Adjust the name in the following other areas:
        - Github Actions in `.github/workflows/`
        - `servicer_grpc/setup.py`
        - `servicer_grpc/pyproject.toml`
        - `pre-commit-config.yaml` and the unit tests accordingly.  
    - Adjust the content of the `servicer_grpc/setup.py` file according to your needs, and make sure to fill in the project URL, maintainer and author information too.
    - Finally, update the `README.md` to discuss the package grpc

- `servicer folder` changes required
    - Reset the package’s version number in `servicer/src/service/__init__.py`
    - Rename the `servicer/src/service` folder to whatever your own package grpc's name. Adjust the name in the following other areas:
        - Github Actions in `.github/workflows/`
        - `servicer/setup.py`
        - `servicer/pyproject.toml`
        - `pre-commit-config.yaml` and the unit tests accordingly.
    - Adjust the content of the `servicer/setup.py` file according to your needs, and make sure to fill in the project URL, maintainer and author information too.
        - Correct the URL to the package_grpc as found in the _install requires__ section:
        ```
        f"package-grpc @ git+https://{os.environ['PASSPORT_CI_TOKEN']}@github.com/getpassport/python-services-template.git#subdirectory=servicer_grpc",
        ```
    - Update the `README.md` to discuss the package service

## Setting up after cloning

All the setup should be contained within the makefile.  After cloning the repo you should `cd` into the cloned repo and then do the following:

```bash
make setup-all
make install-all-dev
source venv/bin/activate
```

This should setup the venv for development.

_*NOTE*_: If you have added additional environment variables for your shell you will have to restart the shell upon the first setup -- a warning in the terminal should notify the developer.

## Makefile commands

The Makefile contains commands for setup, install, building, docker and test.  Not all the commands are documented here, but the main ones that developers and build tools will use.

### Setup commands

- `make setup-all` -- this command setups up the following: (1) environment variables via the _*./scripts/setup-env.sh*_ file; (2) virtual environment which is defined in the _*venv*_ folder; (3) additional setup installs like pyclean and upgrading

### Install commands

- `make install-all-dev` -- Does a _*pip install -e*_ for the packages for development purposes

### Build and Test commands

- `make check` -- runs the pre-commit tests

- `make test` -- runs the pytest tests

### Clean commands

- `make clean` -- cleans the artifacts generated during a build and/or test

- `make clean-venv` -- doest a complete _*pip uninstall*_ on the venv to start afresh.

### Docker commands

- `make docker-build` -- builds the docker container using the Docker file found at ./servicer/Dockerfile

- `make docker-run` -- runs the docker container


## Caveats and Gotchas

Most of this repository will just work as is, but you need to be aware of _minor_ edits that need to occur to ensure things build smoothly. The subsections below call them all out so you can make changes to your cloned/copy of this template.

### Generating GRPC files

Whenever you generate new files from the `.proto` files you will have to modifiy them slightly to ensure they load correctly.  Typically a generated `_pb2_grpc.py` file will have an include like this:

```
import somefile_pb2 as somefile__pb2
```

This will cause import issues when you are developing _*BOTH*_ the service and the grpc imports.  The reason is that the `import` directive could pick up a newer installed package vs. the local package you are developing.  To fix this, you should change this line to be as follows:

```
from . import somefile_pb2 as somefile__pb2
```

This will ensure that the imports are always using the _local_ version of the `somefile_pb2`.  


***
***

# General Features from Python Package Template
_This section is copied from the general python-package-template and is duplicated here just for ease of use._

[General Features (shared with package-template)](#general-features-from-python-package-template)  
&emsp;[Typing](#typing)  
&emsp;[Quality assurance](#quality-assurance)  
&emsp;[Unit testing](#unit-testing)  
&emsp;[Documentation](#documentation)  
&emsp;[Versioning and publishing](#versioning-and-publishing)  
&emsp;[Dependency analysis](#dependency-analysis)  
&emsp;[Security analysis](#security-analysis)  
&emsp;[Standalone](#standalone)  

### Typing

The package requires a minimum of [Python 3.9](https://www.python.org/downloads/release/python-390/) and supports [Python 3.10](https://www.python.org/downloads/release/python-3100/). All code requires comprehensive [typing](https://docs.python.org/3/library/typing.html). The [mypy](http://mypy-lang.org/) static type checker is invoked by a git hook and through a Github Action to enforce continuous type checks. Make sure to add type hints to your code or to use [stub files](https://mypy.readthedocs.io/en/stable/stubs.html) for types, to ensure that users of your package can `import` and type-check your code (see also [PEP 561](https://www.python.org/dev/peps/pep-0561/)).

### Quality assurance

A number of git hooks are invoked before and after a commit, and before push. These hooks are all managed by the [pre-commit](https://pre-commit.com/) tool and enforce a number of [software quality assurance](https://en.wikipedia.org/wiki/Software_quality_assurance) measures (see [below](#git-hooks)).

### Unit testing

Comprehensive unit testing is enabled using [pytest](https://pytest.org/) combined with [Hypothesis](https://hypothesis.works/) (to generate test payloads and strategies), and test code coverage is measured using [coverage](https://github.com/nedbat/coveragepy) (see [below](#testing)).

### Documentation

Documentation is important, and [Sphinx](https://www.sphinx-doc.org/en/master/) is set up already to produce standard documentation for the package, assuming that code contains [docstrings with reStructuredText](https://www.python.org/dev/peps/pep-0287/) (see [below](#documentation)).

### Versioning and publishing

Automatic package versioning and tagging, publishing to [PyPI](https://pypi.org/), and [Changelog](https://en.wikipedia.org/wiki/Changelog) generation are enabled using Github Actions (see [below](#versioning-publishing-and-changelog)).

### Dependency analysis

[Dependabot](https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/about-dependabot-version-updates) is enabled to scan the dependencies and automatically create pull requests when an updated version is available.

### Security analysis

[CodeQL](https://codeql.github.com/) is enabled to scan the Python code for security vulnerabilities. You can adjust the GitHub Actions workflow at `.github/workflows/codeql-analysis.yaml` and the configuration file at `.github/codeql/codeql-config.yaml` to add more languages, change the default paths, scan schedule, and queries.

Additionally, the [bandit](https://github.com/PyCQA/bandit) tool is being installed as part of a development environment (i.e. the `[dev]` package extra); however, bandit does not run automatically! Instead, you can invoke it manually:

```bash
bandit --recursive src  # Add '--skip B101' when checking the tests, Bandit issue #457.
```

### Standalone

In addition to being an importable standard Python package, the package is also set up to be used as a runnable and standalone package using Python’s [-m](https://docs.python.org/3/using/cmdline.html#cmdoption-m) command-line option, or by simply calling its console script wrapper `something` which is automatically generated and installed into the hosting Python environment.
