from pathlib import Path

import nox

PROJECT_ROOT = Path(__file__).parent.resolve()


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    """
    Runs the test suite against all supported python versions.
    """
    session.install("pytest", "pytest-cov")
    session.install(".")
    # Posargs allows passing of tests directly
    tests = session.posargs or ["tests/"]
    session.run("pytest", "--cov=pymechtest", *tests)


@nox.session()
def coverage(session):
    """
    Test coverage analysis.
    """
    session.install("coverage")

    session.run("coverage", "report", "--fail-under=96", "--show-missing")
    session.run("coverage", "erase")


@nox.session()
def style(session):
    """
    Formats project with black and isort, then runs flake8 and mypy linting.
    """

    session.install("black", "isort", "flake8", "mypy")
    session.run("isort", ".")
    session.run("black", ".")
    session.run("flake8", ".")
    session.run("mypy", ".")


@nox.session()
def docs(session):
    """
    Builds the project documentation.

    By default just builds (fail on sphinx warning).

    If '-- serve' is passed, will use sphinx-autobuild and open a browser.
    """
    build_dir = str(PROJECT_ROOT.joinpath("docs/_build/html"))
    source_dir = str(PROJECT_ROOT.joinpath("docs/"))

    # Key: -b = build, html = Build type, -W = Fail on warning
    sphinx_args = ["-b", "html", "-W", source_dir, build_dir]

    # Clean any pre-built docs
    session.run("rm", "-rf", build_dir, external=True)
    session.install(
        "sphinx",
        "sphinx-autobuild",
        "sphinx-rtd-theme",
        "recommonmark",
    )
    session.install(".")

    if "serve" in session.posargs:
        sphinx_cmd = "sphinx-autobuild"
        sphinx_args.insert(0, "--open-browser")
    else:
        sphinx_cmd = "sphinx-build"

    session.run(sphinx_cmd, *sphinx_args)
