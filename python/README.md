# Python Project with Artifactory Dependency Management

## 1. Create a Python Project

1. Create a project directory:
   ```bash
   mkdir my_python_project
   cd my_python_project

Create a requirements.txt file to manage dependencies:

touch requirements.txt

Add project files, e.g., main.py:

touch main.py

## 2. Set Up Artifactory for Dependency Management
Configure pip to use Artifactory: Create or edit the pip configuration file:

On Linux/macOS: ~/.config/pip/pip.conf
On Windows: $env:APPDATA\pip\pip.ini
Add the following:

[global]
index-url = https://<USERNAME>:<PASSWORD>@<ARTIFACTORY_URL>/artifactory/api/pypi/<REPO_NAME>/simple/
trusted-host = <ARTIFACTORY_URL>

Replace <ARTIFACTORY_URL> and <REPO_NAME> with your Artifactory instance details.

## 3. Install Dependencies
Add dependencies to requirements.txt, e.g.:

flask==2.2.2
requests==2.28.1

Install them:

pip install -r requirements.txt

## 4. Generate a Distribution Package 
If creating and uploading your own package:

Create a setup.py file:

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

Build the package:

pip install setuptools

python setup.py sdist

## 5. Upload Your Package to Artifactory
Install twine:

pip install twine
Upload the package:

twine upload --repository-url https://<ARTIFACTORY_URL>/artifactory/api/pypi/<REPO_NAME>/ dist/*