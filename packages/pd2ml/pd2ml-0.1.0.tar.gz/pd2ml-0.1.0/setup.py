# coding=utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pd2ml",
    version="0.1.0",
    author="Tanyee Zhang",
    author_email="676761828@qq.com",
    description="A Python package that provides an efficient way to upload pandas DataFrame to MySQL and download from "
                "the database table into a DataFrame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TanyeeZhang/pd2ml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
