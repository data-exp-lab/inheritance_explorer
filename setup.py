#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "pydot",
    "pycode_similar",
    "numpy",
    "matplotlib",
    "pyvis",
    "networkx",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Chris Havlin",
    author_email="chris.havlin@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A tool for exploring complex inheritance patters in python code",
    entry_points={
        "console_scripts": [
            "inheritance_explorer=inheritance_explorer.cli:map_class",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="inheritance_explorer",
    name="inheritance_explorer",
    packages=find_packages(include=["inheritance_explorer", "inheritance_explorer.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/data-exp-lab/inheritance_explorer",
    version="0.1.0",
    zip_safe=False,
)
