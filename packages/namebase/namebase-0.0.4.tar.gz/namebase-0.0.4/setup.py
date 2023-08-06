# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="namebase",  # Replace with your own username
    version="0.0.4",
    python_requires='>=3.6',
    author="v1xingyue",
    author_email="qixingyue@126.com",
    description="Python Client to interact with the Namebase API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/v1xingyue/namebase-py",
    modules=find_packages(exclude=["env"]),
    include_package_data=True,
    # packages=["namebase"],
    install_requires=['requests'],
    keywords=["namebase", "handshake"]
)
