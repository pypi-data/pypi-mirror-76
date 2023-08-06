#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cflow",
    version="0.1.0",
    author="Joakim Hove",
    author_email="joakim.hove@opm-op.com",
    description="A client to submit opm/flow simulations to the cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/cflow"],
    python_requires='>=2.7',
    install_requires=[
        "requests"
    ],
    test_suite='tests',
)
