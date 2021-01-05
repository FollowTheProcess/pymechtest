"""
Nox configuration file for the project.
"""

from pathlib import Path

import nox

PROJECT_ROOT = Path(__file__).parent.resolve()


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    """
    Runs the test suite against all supported python versions.
    """
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[test]")
    # Posargs allows passing of tests directly
    tests = session.posargs or ["tests/"]
    session.run("pytest", "--cov=pymechtest", *tests)


@nox.session(python=["3.7", "3.8", "3.9"], venv_backend="conda")
def test_conda(session):
    """
    Runs the test suite against all support python version
    in a conda virtual environment.
    """
    session.conda_install(
        "pandas>=1.1.4",
        "numpy>=1.19.4",
        "openpyxl>=3.0.5",
        "altair>=4.1.0",
        "altair_data_server>=0.4.1",
        "altair_saver>=0.5.0",
        "pytest>=6.1.2",
        "pytest-cov>=2.10.1",
    )
    session.install(".", "--no-deps")
    tests = session.posargs or ["tests/"]
    session.run("pytest", "--cov=pymechtest", *tests)


@nox.session()
def coverage(session):
    """
    Test coverage analysis.
    """
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[cov]")

    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "erase")


@nox.session()
def lint(session):
    """
    Formats project with black and isort, then runs flake8 and mypy linting.
    """
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[lint]")
    session.run("isort", ".")
    session.run("black", ".")
    session.run("flake8", ".")
    session.run("mypy", ".")


@nox.session()
def docs(session):
    """
    Builds the project documentation.
    """
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[docs]")

    session.run("mkdocs", "build", "--clean")
