#!/usr/bin/env python

from setuptools import setup, find_packages 
import pathlib 
import os 

version = "0.1.2" 

with open (os.path.join(pathlib.Path(__file__).parent, "README.md")) as f:
    long_description = f.readline()

INSTALL_REQUIRES = ["numpy>=1.15",
                    "Pillow",
                    "pandas",
                    "matplotlib",
                    "scikit-image>=0.14.2",
                    "opencv-python-headless"]

setup (
    name = "aug_img",
    version = version, 
    description = "package test use a simple image precessing example",
    long_description = long_description,
    author = "chloejay",
    author_email = "ji.jie@edhec.com",
    url = "",
    license = "MIT", 
    # classifiers= [],
    # required
    packages = find_packages(include= ["aug_img", "aug_img.*"]),
    include_package_data=True,
    install_requires = INSTALL_REQUIRES,
    package_data = {
        "": ["README.md", "requirements.txt"],
    },
    zip_safe = False
)