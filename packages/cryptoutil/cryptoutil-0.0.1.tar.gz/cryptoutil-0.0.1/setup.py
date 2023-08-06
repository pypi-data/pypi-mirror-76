import setuptools

name = "cryptoutil"
description = "A collection of cryptography related utilities."
version = "0.0.1"
dependencies = [
    "pybackpack >= 0.1.0",
    "cryptography >= 3.0.0"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author="Pooya Vahidi",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pooyavahidi/cryptoutil",
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
    python_requires=">=3.6",
)