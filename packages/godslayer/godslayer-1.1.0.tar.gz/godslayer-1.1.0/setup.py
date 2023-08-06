#!/usr/bin/env python
"""The setup script."""

from setuptools import find_packages, setup  # type: ignore

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    author="Yukihiko Shinoda",
    author_email="yuk.hik.future@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Indexing",
        "Typing :: Typed",
    ],
    dependency_links=[],
    description="Provides generator to read Kami (god) CSV record as list of string.",
    exclude_package_data={"": ["__pycache__", "*.py[co]", ".pytest_cache"]},
    include_package_data=True,
    install_requires=[],
    keywords="God CSV Excel Microsoft 神CSV ネ申CSV 神エクセル ネ申エクセル マイクロソフト",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="godslayer",
    packages=find_packages(include=["godslayer", "godslayer.*", "tests", "tests.*"]),
    package_data={"godslayer": ["py.typed"], "tests": ["*"]},
    python_requires=">=3.7",
    test_suite="tests",
    tests_require=["pytest>=3"],
    url="https://github.com/yukihiko-shinoda/god-slayer",
    version="1.1.0",
    zip_safe=False,
)
