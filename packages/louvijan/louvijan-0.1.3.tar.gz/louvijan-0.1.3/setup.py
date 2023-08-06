# coding=utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="louvijan",
    version="0.1.3",
    author="Tanyee Zhang",
    author_email="676761828@qq.com",
    description="A tool to control the script pipeline, which means that scripts can be executed in a specified order.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TanyeeZhang/louvijan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

