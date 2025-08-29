from setuptools import setup, find_packages

setup(
    name='my_python_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests==2.25.1',
        'django==4.2.22',  # Known critical vulnerability
    ],
)