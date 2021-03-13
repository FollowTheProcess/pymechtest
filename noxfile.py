"""
Nox configuration file for the project.
"""

import os
from pathlib import Path
from typing import List

import nox

PROJECT_ROOT = Path(__file__).parent.resolve()

# GitHub actions has a CI env variable that is always True
ON_CI = os.getenv("CI")

# Local conda test takes ages!
if not ON_CI:
    nox.options.sessions = ["test", "coverage", "lint", "docs"]

DEFAULT_PYTHON: str = "3.9"

PYTHON_VERSIONS: List[str] = [
    "3.7",
    "3.8",
    "3.9",
]

CONDA_REQUIREMENTS: List[str] = [
    "pandas",
    "numpy",
    "altair",
    "altair_data_server",
    "altair_saver",
    "pytest",
    "pytest-cov",
]


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """
    Runs the test suite against all supported python versions.
    """
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[test]")
    # Posargs allows passing of tests directly
    tests = session.posargs or ["tests/"]
    session.run("pytest", "--cov=pymechtest", *tests)
    session.notify("coverage")


@nox.session(python=PYTHON_VERSIONS, venv_backend="conda")
def test_conda(session: nox.Session) -> None:
    """
    Runs the test suite against all support python version in a conda env.
    """
    session.conda_install(*CONDA_REQUIREMENTS)
    session.install(".", "--no-deps")
    tests = session.posargs or ["tests/"]
    session.run("pytest", "--cov=pymechtest", *tests)


@nox.session(python=DEFAULT_PYTHON)
def coverage(session: nox.Session) -> None:
    """
    Test coverage analysis.
    """
    img_path = PROJECT_ROOT.joinpath("docs/img/coverage.svg")

    if not img_path.exists():
        img_path.parent.mkdir(parents=True)
        img_path.touch()

    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[cov]")

    session.run("coverage", "report", "--show-missing")
    session.run("coverage-badge", "-fo", f"{str(img_path)}")


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session) -> None:
    """
    Formats project with black and isort, then runs flake8 and mypy linting.
    """
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[lint]")
    session.run("isort", ".")
    session.run("black", ".")
    session.run("flake8", ".")
    session.run("mypy", ".")


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session) -> None:
    """
    Builds the project documentation.

    If '-- serve' passed, auto serves docs.

    Run 'nox -s docs -- serve' to do this.
    """
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(".[docs]")

    if "serve" in session.posargs:
        session.run("mkdocs", "serve")
    else:
        session.run("mkdocs", "build", "--clean")
