import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="flow_sdk_utils",
    version="1.0.0",
    description="Python utils for HahnPRO Flow-SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tklingenhoefer/flow-sdk-utils",
    author="Timo Klingenhöfer",
    author_email="tk@hahnpro.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=["pika", "numpy"],
)
