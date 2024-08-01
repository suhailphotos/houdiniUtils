#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module sets up the package for houdiniUtils"""

from setuptools import find_packages, setup

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="houdiniUtils",
    author="Suhail",
    author_email="suhailece@gmail.com",
    maintainer="Suhail",
    maintainer_email="suhailece@gmail.com",
    version="0.1.0",
    url="https://github.com/suhailphotos/houdiniUtils",
    download_url='https://github.com/suhailphotos/houdiniUtils',
    keywords=['Houdini', 'Texture Tools', 'Houdini Utilities'],
    license="MIT",
    description="A collection of utilities for Houdini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/suhailphotos/houdiniUtils/issues",
    },
    python_requires=">=3.10",
    packages=find_packages(include=['houdiniutils', 'houdiniutils.*']),
    include_package_data=True,
    package_data={
        'houdiniutils.textureTools': ['textureID.json', 'houUtils.shelf'],
    },
    install_requires=[
        # List any dependencies here, if applicable
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
