#!/usr/bin/env python3
"""
Setup script for Darkelf Shell
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="darkelf-shell",
    version="1.0.0",
    author="Darkelf Research",
    description="A Tor-enabled, persona-configurable WebView shell for research and education",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Security",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "darkelf-shell=main:main",
        ],
    },
    keywords="tor, privacy, anonymity, browser, research, education, cybersecurity",
    project_urls={
        "Bug Reports": "https://github.com/Darkelf2024/Darkelf-Shell/issues",
        "Source": "https://github.com/Darkelf2024/Darkelf-Shell",
    },
)