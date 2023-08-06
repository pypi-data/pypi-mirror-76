import setuptools
from pathlib import Path

setuptools.setup(
    name="hitanshsumsquare3",
    version=1.0,
    long_description=Path("README3.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
