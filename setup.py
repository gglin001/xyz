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
        url="https://github.com/gglin001/xyz",
        python_requires=">=3.8",
        install_requires=_get_requires(),
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        entry_points={
            "console_scripts": [
                "xyz.mlir_prettier = xyz.mlir_prettier:cli",
                "xyz.cl2hpp = xyz.cl2hpp:cli",
                "xyz.file2hex = xyz.file2hex:cli",
                "xyz.hex2file = xyz.hex2file:cli",
                "xyz.file2qr = xyz.file2qr:cli",
                "xyz.qr2file = xyz.qr2file:cli",
            ]
        },
    )
