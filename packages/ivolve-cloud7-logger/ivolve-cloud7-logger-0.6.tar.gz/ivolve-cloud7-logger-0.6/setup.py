#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
  name = 'ivolve-cloud7-logger',
  packages=setuptools.find_packages(),
  version = '0.6',
  license='iVolve', 
  author="Mujeebullah",
  author_email="mujeebullah.kalwar@ivolve.io",
  description="CLOUD7 Logger",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/iVolve-Tech/",
  keywords = ['logger', 'cloud7', 'ivolve'],
  install_requires=[
          'pycryptodomex',
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)