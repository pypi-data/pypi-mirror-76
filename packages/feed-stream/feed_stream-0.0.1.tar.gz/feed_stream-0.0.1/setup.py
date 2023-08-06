import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
with open("README.md", "r") as fp:
    README = fp.read()

setup(
    name="feed_stream", # Replace with your own username
    version="0.0.1",
    author="Matthew Brulhardt",
    author_email="mwbrulhardt@gmail.com",
    description="A streamable version of pandas.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mwbrulhardt/feed",
    packages=find_packages(exclude=("tests",)),
    license="GPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
