#!/usr/bin/env python

from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.rst").read_text()

setup(
    name="Ades",
    description="Validate flask inputs with openapi validators",
    version="0.1.0dev1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    long_description=README,
    long_description_content_type="text/x-rst",
)
