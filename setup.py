from __future__ import annotations

import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent.resolve()


def _get_requires():
    with open("requirements.txt", "r") as f:
        install_requires = f.readlines()
    return install_requires


if __name__ == "__main__":
    setup(
        install_requires=_get_requires(),
        package_dir={"": "src"},
        packages=find_packages(where="src"),
    )
