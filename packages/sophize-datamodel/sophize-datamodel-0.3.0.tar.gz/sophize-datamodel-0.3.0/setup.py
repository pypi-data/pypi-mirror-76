import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "sophize_datamodel" / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sophize-datamodel",
    version="0.3.0",
    description="Classes for data can be ingested by Sophize.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Sophize/datamodel-python",
    author="Abhishek Chugh",
    author_email="achugh89@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sophize_datamodel"],
    include_package_data=True
)
