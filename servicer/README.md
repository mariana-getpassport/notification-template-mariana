![license](https://img.shields.io/badge/license-MIT-blue) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-yellow?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![conventional-commits](https://img.shields.io/badge/conventional%20commits-1.0.0-yellow)](https://www.conventionalcommits.org/en/v1.0.0/) [![black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black) [![mypy](https://img.shields.io/badge/mypy-checked-brightgreen)](http://mypy-lang.org/) [![pylint](https://img.shields.io/badge/pylint-required%2010.0-brightgreen)](http://pylint.org/) [![pytest](https://img.shields.io/badge/pytest-enabled-brightgreen)](https://github.com/pytest-dev/pytest) [![coverage](https://img.shields.io/badge/coverage-required%20100%25-brightgreen)](https://github.com/nedbat/coveragepy)

# Servicer Package

This repository is based on a template, a cookiecutter for a new Python services project while keeping [PEP518](https://www.python.org/dev/peps/pep-0518/) in mind. Because it’s hosted on Github it already utilizes a few [Github Actions](https://docs.github.com/en/actions) that enforce repository-side checks for continuous integration and that implement a semantic release setup. And while this package is a starting point for a Python project with good engineering practices, it’s intended to be improved and added to in various ways — see the [Wiki](https://github.com/jenstroeger/python-package-template/wiki) for more suggestions.

You can find all the information in the README.md file at the root level of this repository.

# Example servicer

This code is based off the _recommendations_ example code that is found on Passport's Google Drive [here](https://drive.google.com/drive/folders/1SH5J5X01NSsQCG2OgLPTHrzHMrdOe6JU).
This code is copied & modified from the [Real Python Tutorial on GRPC](https://realpython.com/python-microservices-grpc/).

The source layout is as follows:

root/<br>
|- protos/   <-- proto files for GRPC <br>
|- servicer/ <-- servicer/server that handles the GRPC calls <br>
|- servicer_grpc/    <-- generated GRPC stubs reside here <br>

## How to use
As mentioned in the `root` level README, do the following to setup the repository after cloning and cd'ing into the clone:
```
make setup--all
make install-all
source venv/bin/activate
```

To start the server at the root type: `python -m servicer.src.package_server.__main__`
You can test it out, via a simple test script found here: `python ./servicer/tests/test_server.py`

### Different branches

I’ve built a few prototypes of both examples but want to get some input.
You can try it out with this repo and branch here:  https://github.com/getpassport/bpost-playground/tree/grpc_server
It includes the grpc generated code from  this branch:  https://github.com/getpassport/bpost-playground/tree/grpc_package
