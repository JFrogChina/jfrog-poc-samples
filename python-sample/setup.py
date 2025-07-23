from setuptools import setup, find_packages

setup(
    name='my_python_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests==2.32.4',
        'django==1.11.29',  # Known critical vulnerability
    ],
)