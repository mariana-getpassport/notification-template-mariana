"""Setup for this package."""

import ast
import os
import typing

import setuptools

here = os.path.abspath(os.path.dirname(__file__))
src = os.path.join(here, "src")

with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    README = fh.read()
with open(os.path.join(here, "LICENSE.md"), encoding="utf-8") as fh:
    LICENSE = fh.read()
with open(os.path.join(src, "package_server", "__init__.py"), encoding="utf-8") as fh:
    module = ast.parse(next(filter(lambda line: line.startswith("__version__"), fh)))
    assign = typing.cast(ast.Assign, module.body[0])
    # See also: https://github.com/relekang/python-semantic-release/issues/388
    VERSION = typing.cast(ast.Constant, assign.value).s

# https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-args
# https://docs.python.org/3/distutils/apiref.html#distutils.core.setup
setuptools.setup(
    name="package_server",
    version=VERSION,
    description="Server for Recommendations APIs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://project.url/",
    # author="Brad Post",
    # author_email="brad@getpassport.co",
    maintainer="Brad Post",
    maintainer_email="brad@getpassport.co",
    license=LICENSE,
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.9",
    keywords="",
    project_urls={
        "Homepage": "https://foo.bar/",
    },
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "package_server": ["py.typed"],
    },
    include_package_data=True,
    install_requires=[
        "grpcio==1.41.1",
        "grpcio-tools==1.41.1",
        "grpc-interceptor==0.13.0",
        "opentelemetry-instrumentation-grpc==0.29b0",
        "opentelemetry-propagator-b3==1.10.0",
        "sqlalchemy[mypy,postgresql_psycopg2binary]==1.4.26",
        "sqlalchemy-utils==0.38.2",
        "alembic[tz]==1.7.6",
        f"utilities @ git+https://{os.environ['PASSPORT_CI_TOKEN']}@github.com/getpassport/utils_package_python.git@v0.6.0",  # noqa: E501 # pylint: disable=line-too-long
        f"orm @ git+https://{os.environ['PASSPORT_CI_TOKEN']}@github.com/getpassport/orm_package_python.git@v2.3.0",  # noqa: E501 # pylint: disable=line-too-long
    ],
    extras_require={
        "test": ["hypothesis==6.35.1", "pytest==6.2.5", "pytest-cov==3.0.0"],
        "dev": [
            "bandit==1.7.1",
            "flake8==4.0.1",
            "flake8-builtins==1.5.3",
            "flake8-docstrings==1.6.0",
            "flake8-rst-docstrings==0.2.5",
            "hypothesis==6.35.1",
            # Using Mypy 0.921 because version 0.931 has issues with SQLAlchemy plugin.
            "mypy==0.921",
            "pep8-naming==0.12.1",
            "pre-commit==2.17.0",
            "pylint==2.12.2",
            "types-setuptools==57.4.2",
            "pyclean",
        ],
        "docs": ["sphinx==4.4.0"],
    },
    options={},
    platforms="",
    zip_safe=False,
)
