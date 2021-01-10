"""
Handy invoke automation tasks.

Use nox for testing and these just to help development.
"""

from invoke import task


@task
def docs(c):
    """
    Builds project docs with mkdocs.
    """
    c.run("mkdocs build --clean")


@task
def autodocs(c):
    """
    Builds & serves docs.
    """
    c.run("mkdocs serve")


@task
def test(c):
    """
    Runs testing with pytest.
    """
    c.run("pytest --cov=pymechtest")


@task(test)
def cov(c):
    """
    Runs test coverage analysis.
    """
    c.run("coverage report --show-missing")
