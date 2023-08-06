#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import find_packages, setup  # type: ignore


def main():
    """This function implements build settings."""
    with open("README.md", "r", encoding="utf8") as file:
        readme = file.read()

    setup(
        name="yamldataclassconfig",
        version="1.4.0",
        description="This project helps you to import config file writen by YAML to Python data class.",
        long_description=readme,
        long_description_content_type="text/markdown",
        author="Yukihiko Shinoda",
        author_email="yuk.hik.future@gmail.com",
        packages=find_packages(exclude=("tests*", "myproduct*", "yourproduct*")),
        package_data={"yamldataclassconfig": ["py.typed"]},
        python_requires=">=3.7",
        install_requires=["dataclasses-json", "pyyaml"],
        dependency_links=[],
        setup_requires=["pytest-runner"],
        url="https://github.com/yukihiko-shinoda/yaml-dataclass-config",
        keywords="yaml dataclass dataclasses config",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Quality Assurance",
        ],
    )


if __name__ == "__main__":
    main()
