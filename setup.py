#!/usr/bin/env python3
"""
Setup script for Easy Tracks package
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = ""
readme_file = this_directory / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text()

# Read version from __init__.py
version = {}
with open("easy_tracks/__init__.py") as fp:
    exec(fp.read(), version)

setup(
    name="easy-tracks",
    version=version.get("__version__", "1.0.0"),
    author="Easy Tracks Development Team",
    author_email="",
    description="User-friendly pyGenomeTracks generator for genomics data visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/easy-tracks",  # Update with actual URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "pyBigWig>=0.3.0",
        "PyYAML>=5.4.0",
        "pyGenomeTracks>=3.7",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "easy-tracks=easy_tracks.cli:main",
            "narrowpeak-to-bed=easy_tracks.utils:convert_narrowpeak_to_bed",
        ],
    },
    include_package_data=True,
    package_data={
        "easy_tracks": ["../configs/*.yaml", "../docs/*.md"],
    },
    zip_safe=False,
    keywords="genomics bioinformatics visualization tracks bigwig bed gtf pyGenomeTracks",
    project_urls={
        "Bug Reports": "https://github.com/your-org/easy-tracks/issues",
        "Source": "https://github.com/your-org/easy-tracks/",
        "Documentation": "https://github.com/your-org/easy-tracks/docs",
    },
)