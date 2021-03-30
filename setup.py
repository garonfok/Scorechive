from scorechive._version import __version__
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scorechive",
    version=__version__,
    author="Garon Fok",
    author_email="fokgaron@gmail.com",
    packages=["example_pkg"],
    description="Scorechive is a fast and lightweight CLI program that is designed to keep track of your music scores using SQLite.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    python_requires='>=3.9.2',
    install_requires=[
         "click>=7.1.2",
         "columnize">="0.3.10"
    ]
)
