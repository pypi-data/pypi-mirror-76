#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ivolve-cloud7-logger",
    version="0.1",
    author="Mujeebullah",
    author_email="mujeebullah.kalwar@ivolve.io",
    description="CLOUD7 Logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iVolve-Tech/",
    packages=setuptools.find_packages(),
    install_requires=[
          'pycryptodomex',
          'dotenv',
          'requests',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)