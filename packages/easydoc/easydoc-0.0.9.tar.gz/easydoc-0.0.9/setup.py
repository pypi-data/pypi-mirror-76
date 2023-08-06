#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com

import setuptools

with open("easydoc/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
name="easydoc",
        version="0.0.9",
        author="Frank YCJ",
        author_email="1320259466@qq.com",
        description="Make data operation easier!",
        keywords='excel word pdf import export',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/YouAreOnlyOne",
        # packages=setuptools.find_packages(),
        packages=["easydoc"],
        install_requires=['openpyxl>=2.6.4','futures>=3.3.0'],
        python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
        license="Apache 2.0 license",
        Platform="OS All, Python 2.x",

        project_urls={
        "Bug Tracker": "https://github.com/YouAreOnlyOne/FastFrameJar/issues",
        "Documentation": "https://github.com/YouAreOnlyOne/FastFrameJar",
        "Source Code": "https://github.com/YouAreOnlyOne/FastFrameJar",
    },

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "easydoc": ["README"],
        "easydoc": ["README.md"],
        "": ["README.md"],
        "easydoc": ["*.md"],
        "easydoc": ["LICENSE"],
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
