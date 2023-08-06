import io
import os

import setuptools


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return fd.read()


# TODO: add url, author and license
setuptools.setup(
    name="buenbit",
    version="0.0.1",
    description="Buenbit API client.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["requests-openapi==0.9.5", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
