from setuptools import setup


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DualFM", # Replace with your own username
    version="0.0.5",
    author="DualFM",
    author_email="doe92899@gmail.com",
    description="Python module for dualfm api.",
    long_description="Look at https://github.com/Cynlis/DualFM-Python/blob/master/README.md on how to use.",
    long_description_content_type="text/markdown",
    url="https://github.com/Cynlis/DualFM-Python/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)