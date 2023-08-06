#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from setuptools import setup, find_packages

setup(
    name="warc2zim",
    version="0.0.1",
    description="OpenZIM's WARC to ZIM file converter",
    long_description="",
    long_description_content_type="text/markdown",
    author="openzim",
    author_email="reg@kiwix.org",
    url="https://github.com/openzim/warc2zim",
    keywords="openzim kiwix zim offline",
    license="GPLv3+",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    python_requires=">=3.6",
)
