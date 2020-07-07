#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="ZeroSeg-Improved",
    version="0.1.1",
    author="Richard Saville, samedamci",
    author_email="samedamci@disroot.org",
    description=(
        "Improved code library for the ZeroSeg display board for the Raspberry Pi."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samedamci/ZeroSeg",
    packages=["ZeroSeg"],
    license="MIT",
    keywords="raspberry pi rpi led max7219 matrix seven segment zeroseg",
    python_requires=">=3.6",
    install_requires=[
        'GPIO',
        'spidev'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
