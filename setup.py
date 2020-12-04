from pathlib import Path

from setuptools import find_packages, setup

import versioneer

ROOT = Path(__file__).parent.resolve()


def read(path: str, encoding: str = "utf-8") -> str:
    """
    Utility function to read the content of files to
    be passed to setup arguments.
    """

    file_path = ROOT.joinpath(path)
    with open(file_path, encoding=encoding) as fp:
        return fp.read()


def get_install_requirements(path: str) -> list:
    """
    Utility function to read a requirements.txt type file.
    """
    content = read(path)
    return [req for req in content.split("\n") if req != "" and not req.startswith("#")]


setup(
    name="pymechtest",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Python package to automate the boring bits of mechanical test data analysis!",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/FollowTheProcess/pymechtest",
    author="Tom Fleet",
    author_email="tomfleet2018@gmail.com",
    classifiers=[
        # Update this before release
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.7",
    install_requires=get_install_requirements("requirements.txt"),
    extras_require={"dev": get_install_requirements("requirements_dev.txt")},
    license="GNU General Public License v3",
    test_suite="tests",
    zip_safe=False,
    project_urls={
        "Documentation": "https://FollowTheProcess.github.io/pymechtest/",
        "Source Code": "https://github.com/FollowTheProcess/pymechtest",
    },
)
