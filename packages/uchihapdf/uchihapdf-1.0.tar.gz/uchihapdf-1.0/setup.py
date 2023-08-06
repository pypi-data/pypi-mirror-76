# import setuptools
#
# setuptools.setup(
#     name="uchihapdf",
#     version=1.0,
#     long_description="",
#     packages=setuptools.find_packages(exclude=["tests", "data"])
# )

import setuptools
from pathlib import Path

setuptools.setup(
    name="uchihapdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)