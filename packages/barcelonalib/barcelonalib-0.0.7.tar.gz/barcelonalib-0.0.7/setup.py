# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup

# from setuptools import find_packages
# import os

with open("README.md") as f:
    readme = f.read()


def package_files():
    paths = []
    # for (path, _, filenames) in os.walk("additional/directory"):
    #     for filename in filenames:
    #         paths.append(os.path.join("..", path, filename))
    return paths


extra_files = package_files()

setup(
    name="barcelonalib",
    version="0.0.7",
    description="Library to simplify writing out events during CI/CD workflows.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="David Aronchick",
    author_email="aronchick@gmail.com",
    url="https://github.com/barcelona/barcelonalib",
    license="MIT License",
    keywords=["Barcelona"],  # Keywords that define your package best
    install_requires=[
        "ipython",
        "msgpack",
        "opentelemetry-api",
        "opentelemetry-sdk",
        "environs",
        "setuptools",
        "attrdict",
        "python-dotenv",
    ],
    packages=["barcelonalib"],
    include_package_data=True,
    package_data={"": extra_files},
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
