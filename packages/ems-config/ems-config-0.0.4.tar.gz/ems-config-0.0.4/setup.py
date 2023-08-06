from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='ems-config',
    author="Emil Haldrup Eriksen",
    author_email="emil.h.eriksen@gmail.com",
    description="Common configuration utilities for EMS projects",
    version="0.0.4",
    url='https://gitlab.com/thedirtyfew/utilities/ems-config',
    packages=['ems_config'],
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires='>=3'
)
