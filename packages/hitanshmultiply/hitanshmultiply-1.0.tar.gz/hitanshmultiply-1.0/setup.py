import setuptools
from pathlib import Path

setuptools.setup(
    name="hitanshmultiply",
    version=1.0,
    long_description=Path("README2.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
