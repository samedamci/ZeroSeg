#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="ZeroSeg-Improved",
    version="0.3",
    author="Richard Saville, samedamci",
    author_email="samedamci@disroot.org",
    description=(
        "Improved code library for the ZeroSeg display board for the Raspberry Pi."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samedamci/ZeroSeg",
    project_urls={
        'Issue tracker': 'https://github.com/samedamci/ZeroSeg/issues',
        'Documentation': 'https://github.com/samedamci/ZeroSeg/wiki'
    },
    packages=["ZeroSeg"],
    license="MIT",
    keywords="raspberry pi rpi led max7219 matrix seven segment zeroseg",
    python_requires=">=3.6",
    install_requires=[
        'RPi.GPIO',
        'spidev'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
