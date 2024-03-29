import pathlib


from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent.resolve()


def _get_requires():
    with open("requirements.txt", "r") as f:
        install_requires = f.readlines()
    return install_requires


if __name__ == "__main__":
    setup(
        name="xyz",
        description="mini cli toolkit.",
        author="Allen Guo",
        author_email="guosonglin001@gmail.com",
        python_requires=">=3.8",
        install_requires=_get_requires(),
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        entry_points={
            "console_scripts": [
                "mlir_prettier = xyz.mlir_prettier:cli",
            ]
        },
    )
