# -*- coding: utf-8 -*-
"""Setup file."""
from pathlib import Path
from setuptools import setup, find_packages


setup(
    name="unitoken",
    version="0.2.0",
    description="A universal tokenizer package.",
    author="Stéphan Tulkens",
    author_email="stephantul@gmail.com",
    url="https://github.com/stephantul/unitoken",
    license="MIT",
    packages=find_packages(include=["unitoken"]),
    install_requires=["fasttext-langdetect", "spacy"],
    project_urls={
        "Source Code": "https://github.com/stephantul/unitoken",
        "Issue Tracker": "https://github.com/stephantul/unitoken/issues",
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="tokenization",
    zip_safe=True,
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)
