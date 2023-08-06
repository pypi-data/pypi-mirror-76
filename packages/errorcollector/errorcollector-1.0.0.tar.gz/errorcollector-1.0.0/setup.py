#!/usr/bin/env python
"""This module implements build settings."""
from setuptools import find_packages, setup  # type: ignore


def main():
    """This function implements build settings."""
    with open("README.md", "r", encoding="utf8") as file:
        readme = file.read()

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
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development",
            "Topic :: Software Development :: Quality Assurance",
            "Topic :: Utilities",
            "Typing :: Typed",
        ],
        dependency_links=[],
        description="This project helps you to collect raised error during with statement.",
        exclude_package_data={"": ["__pycache__", "*.py[co]", ".pytest_cache"]},
        include_package_data=True,
        install_requires=[],
        keywords="error exception",
        long_description=readme,
        long_description_content_type="text/markdown",
        name="errorcollector",
        packages=find_packages(include=["errorcollector", "errorcollector.*", "tests", "tests.*"]),
        package_data={"errorcollector": ["py.typed"], "tests": ["*"]},
        python_requires=">=3.6",
        test_suite="tests",
        tests_require=["pytest>=3"],
        url="https://github.com/yukihiko-shinoda/error-collector",
        version="1.0.0",
        zip_safe=False,
    )


if __name__ == "__main__":
    main()
