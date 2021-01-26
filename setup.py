from codecs import open
from setuptools import setup, find_packages
from pathlib import Path
import python_little_tools


# Get long description from relevant file
here = Path(__file__).absolute().parent
with open(here.joinpath('README.md'), 'r', encoding='utf-8') as in_fh:
    long_desc = in_fh.read()

version = python_little_tools.__version__

setup(
    name="python_little_tools",
    version=version,
    author="Darren Xie",
    author_email="mndarren@gmail.com",
    description=("An demonstration of how to create, document, and publish "
                 "to the cheese shop a5 pypi.org."),
    license="BSD",
    url="http://packages.python.org/an_example_pypi_project",
    packages=find_packages(exclude=["tests", "test*"]),
    long_description=long_desc,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_require='>=3.8.5',
    install_requires=[
        'cx_Oracle'
    ],
)
