
from setuptools import setup, find_packages

setup(
    name="my_python_project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask==2.2.2",
        "requests==2.28.1",
    ],
)