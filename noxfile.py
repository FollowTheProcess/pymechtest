"""
Nox configuration file for the project.
"""

import configparser
import json
import os
import shutil
import subprocess
import webbrowser
from pathlib import Path
from typing import List, Set

import nox

# Nox config
nox.needs_version = ">=2021.6.6"
nox.options.error_on_external_run = True

# GitHub Actions
ON_CI = bool(os.getenv("CI"))

# Global project stuff
PROJECT_ROOT = Path(__file__).parent.resolve()
PROJECT_SRC = PROJECT_ROOT / "pymechtest"
PROJECT_TESTS = PROJECT_ROOT / "tests"
SETUP_CFG = PROJECT_ROOT.joinpath("setup.cfg")

# Git info
DEFAULT_BRANCH = "main"

# Where to save the coverage badge
COVERAGE_BADGE = PROJECT_ROOT / "docs" / "img" / "coverage.svg"

# VSCode
VSCODE_DIR = PROJECT_ROOT / ".vscode"
SETTINGS_JSON = VSCODE_DIR / "settings.json"

# Virtual environment stuff
VENV_DIR = PROJECT_ROOT / ".venv"
PYTHON = os.fsdecode(VENV_DIR / "bin" / "python")

# Python to use for non-test sessions
DEFAULT_PYTHON: str = "3.9"

# All supported python versions for pymechtest
PYTHON_VERSIONS: List[str] = [
    "3.7",
    "3.8",
    "3.9",
]

# List of seed packages to upgrade to their most
# recent versions in every nox environment
# these aren't strictly required but I've found including them
# solves most installation problems
SEEDS: List[str] = [
    "pip",
    "setuptools",
    "wheel",
]

# "dev" should only be run if no virtual environment found and we're not on CI
# i.e. someone is using nox to set up their local dev environment to
# work on pymechtest
if not VENV_DIR.exists() and not ON_CI:
    nox.options.sessions = ["dev"]
else:
    nox.options.sessions = ["test", "coverage", "lint", "docs"]


def get_requirements(section: str) -> List[str]:
    """
    Uses configparser to parse `setup.cfg` and extract a list
    of requirements for an `extras` section e.g 'lint', 'docs' etc.

    Similar to calling `pip install .[section]` except this
    function does not install the package or it's dependencies as
    some sessions do not require the installation of the package.

    Args:
        section (str): Valid `setup.cfg` extras_require header
            e.g. 'lint', 'docs' etc.

    Returns:
        List[str]: Versioned requirements from `setup.cfg`
    """

    config = configparser.ConfigParser()
    config.read(SETUP_CFG)

    return config.get("options.extras_require", section).strip().split("\n")


def set_up_vscode(session: nox.Session) -> None:
    """
    Helper function that will set VSCode's workspace settings
    to use the auto-created virtual environment and enable
    pytest support.

    If called, this function will only do anything if
    there aren't already VSCode workspace settings defined.

    Args:
        session (nox.Session): The enclosing nox session.
    """

    if not VSCODE_DIR.exists():
        session.log("Setting up VSCode Workspace.")
        VSCODE_DIR.mkdir(parents=True)
        SETTINGS_JSON.touch()

        settings = {
            "python.defaultInterpreterPath": PYTHON,
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": [PROJECT_TESTS.name],
        }

        with open(SETTINGS_JSON, mode="w", encoding="utf-8") as f:
            json.dump(settings, f, sort_keys=True, indent=4)


def update_seeds(session: nox.Session) -> None:
    """
    Helper function to update the core installation seed packages
    to their latest versions in each session.
    Args:
        session (nox.Session): The nox session currently running.
    """

    session.install("--upgrade", *SEEDS)


def has_changes() -> bool:
    """
    Invoke git in a subprocess to check if we have
    any uncommitted changes in the local repo.

    Returns:
        bool: True if uncommitted changes, else False.
    """
    status = (
        subprocess.run(
            "git status --porcelain",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )
    return len(status) > 0


def get_branch() -> str:
    """
    Invoke git in a subprocess to get the name of
    the current branch.

    Returns:
        str: Name of current branch.
    """
    return (
        subprocess.run(
            "git rev-parse --abbrev-ref HEAD",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )


def enforce_branch_no_changes(session: nox.Session) -> None:
    """
    Errors out the current session if we're not on
    default branch or if there are uncommitted changes.
    """
    if has_changes():
        session.error("All changes must be committed or removed before release")

    branch = get_branch()

    if branch != DEFAULT_BRANCH:
        session.error(
            f"Must be on {DEFAULT_BRANCH!r} branch. Currently on {branch!r} branch"
        )


@nox.session(python=DEFAULT_PYTHON)
def dev(session: nox.Session) -> None:
    """
    Sets up a python dev environment for the project if one doesn't already exist.

    This session will:
    - Create a python virtualenv for the session
    - Install the `virtualenv` cli tool into this environment
    - Use `virtualenv` to create a global project virtual environment
    - Invoke the python interpreter from the global project environment to install
      the project and all it's development dependencies.
    """
    # Check if dev has been run before
    # this prevents manual running nox -s dev more than once
    # thus potentially corrupting an environment
    if VENV_DIR.exists():
        session.error(
            "There is already a virtual environment deactivate and remove it "
            "before running 'dev' again"
        )

    # Create the project virtual environment using virtualenv
    # installed into this sessions virtual environment
    # confusing but it works!
    session.install("virtualenv")
    session.run("virtualenv", os.fsdecode(VENV_DIR), silent=True)

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensure it's installed
    # in the right way
    session.run(
        PYTHON,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
        "setuptools",
        "wheel",
        silent=True,
        external=True,
    )
    session.run(PYTHON, "-m", "pip", "install", "-e", ".[dev]", external=True)

    if bool(shutil.which("code")):
        # Only do this is user has VSCode installed
        set_up_vscode(session)


@nox.session(python=False)
def update(session: nox.Session) -> None:
    """
    Updates the dependencies in the virtual environment to their latest versions.

    Note: this is still based on the version specifiers present in setup.cfg.
    """

    session.run(PYTHON, "-m", "pip", "install", "--upgrade", "-e", ".[dev]")


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """
    Runs the test suite against all supported python versions.
    """

    update_seeds(session)
    # Tests require the package to be installed
    session.install(".[test]")

    session.run("pytest", f"--cov={PROJECT_SRC}", f"{PROJECT_TESTS}")
    session.notify("coverage")


@nox.session(python=DEFAULT_PYTHON)
def coverage(session: nox.Session) -> None:
    """
    Test coverage analysis.
    """

    if not COVERAGE_BADGE.exists():
        COVERAGE_BADGE.parent.mkdir(parents=True)
        COVERAGE_BADGE.touch()

    update_seeds(session)
    session.install(*get_requirements("cov"))

    session.run("coverage", "report", "--show-missing")
    session.run("coverage-badge", "-fo", f"{COVERAGE_BADGE}")


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session) -> None:
    """
    Formats project with black and isort, then runs flake8 and mypy linting.
    """

    update_seeds(session)
    session.install(*get_requirements("lint"))

    # If we're on CI, run in check mode so build fails if formatting isn't correct
    if ON_CI:
        session.run("isort", ".", "--check")
        session.run("black", ".", "--check")
    else:
        # If local, go ahead and fix formatting
        session.run("isort", ".")
        session.run("black", ".")

    session.run("flake8", ".")
    session.run("mypy")


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session) -> None:
    """
    Builds the project documentation. Use '-- serve' to see changes live.
    """

    update_seeds(session)
    # Because we autogen API docs, we need the project installed too
    session.install(".[docs]")

    if "serve" in session.posargs:
        webbrowser.open(url="http://127.0.0.1:8000/pymechtest/")
        session.run("mkdocs", "serve")
    else:
        session.run("mkdocs", "build", "--clean")


@nox.session(python=DEFAULT_PYTHON)
def build(session: nox.Session) -> None:
    """
    Builds the package sdist and wheel.
    """

    update_seeds(session)
    session.install(".")
    session.install("build")

    session.run("build", "--sdist", "--wheel")


@nox.session(python=DEFAULT_PYTHON)
def release(session: nox.Session) -> None:
    """
    Kicks off the automated release process by creating and pushing a new tag.

    Invokes bump2version with the posarg setting the version.

    Usage:

    $ nox -s release -- [major|minor|patch]
    """

    enforce_branch_no_changes(session)

    allowed_args: Set[str] = {"major", "minor", "patch"}
    n_args: int = len(session.posargs)

    if n_args != 1:
        session.error(
            f"Only 1 session arg allowed, got {n_args}. Pass one of: {allowed_args}"
        )

    # If we get here, we know there's only 1 posarg
    version = session.posargs.pop()

    if version not in allowed_args:
        session.error(
            f"Invalid argument: got {version!r}, expected one of: {allowed_args}"
        )

    # If we get here, we should be good to go
    # Let's do a final check for safety
    confirm = input(
        f"You are about to bump the {version!r} version. Are you sure? [y/n]: "
    )

    # Abort on anything other than 'y'
    if confirm.lower().strip() != "y":
        session.error(f"You said no when prompted to bump the {version!r} version.")

    update_seeds(session)

    session.install("bump2version")

    session.log(f"Bumping the {version!r} version")
    session.run("bump2version", version)

    session.log("Pushing the new tag")
    session.run("git", "push", external=True)
    session.run("git", "push", "--tags", external=True)
