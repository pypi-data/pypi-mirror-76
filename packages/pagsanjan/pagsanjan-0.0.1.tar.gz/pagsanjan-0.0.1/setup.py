from setuptools import setup, find_packages

setup(
    name = 'pagsanjan',
    version = '0.0.1',
    author = 'Gianna Pineda',
    author_email = 'gcppineda@gmail.com',
    packages = find_packages(),
    description = "simple pandas logger",
    long_description = "pipe-able pandas logging that converts your logs to dataframe na"
)