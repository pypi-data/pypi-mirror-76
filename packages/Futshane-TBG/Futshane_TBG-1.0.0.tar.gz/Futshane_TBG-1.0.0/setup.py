import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Futshane_TBG",

    version="1.0.0",

    description="""This package provides simple tools for creating Text Based Games. 
    It allows for player world interaction and battle with enemies, its a great way to turn a 
    story into an interactive game that players can enjoy and still maintain their reading requirements.
    """,

    long_description_content_type="text/markdown",

    long_description=README,

    url="https://github.com/ElLoko233/Text-Based-Game-Package",

    author="Lelethu Futshane",

    classifiers=["License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.8"],

    packages=["TBG"],

    include_package_data=True,
)
