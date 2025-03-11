# Python Project Setup for Artifactory

## Prerequisites
- macOS system
- Python 3.x installed
- Access to Artifactory instance

## 1. Set Up the Project
### Navigate to the project directory:
```sh
cd ./python
```

### Ensure `requirements.txt` file exists to manage dependencies:
```sh
ls requirements.txt
```

## 2. Set Up Artifactory for Dependency Management
### Configure pip to use Artifactory:
Create or edit the pip configuration file:

On macOS:
```sh
mkdir -p ~/.pip
vi ~/.pip/pip.conf
```

Add the following:
```ini
[global]
index-url = https://<USERNAME>:<PASSWORD>@<ARTIFACTORY_URL>/artifactory/api/pypi/<VIRTUAL_REPO_NAME>/simple
```
Replace `<USERNAME>`, `<PASSWORD>`, `<ARTIFACTORY_URL>`, and `<VIRTUAL_REPO_NAME>` with your Artifactory instance details.

## 3. Install Dependencies

### Install the dependencies:
```sh
pip install -r requirements.txt
```

## 4. Generate a Distribution Package

### Build the package:
```sh
python setup.py sdist
```

## 5. Upload Your Package to Artifactory
### Install `twine`:
```sh
pip install twine
```

### Upload the package:
```sh
twine upload --repository-url https://<ARTIFACTORY_URL>/artifactory/api/pypi/<REPO_NAME> dist/*
```
Replace `<ARTIFACTORY_URL>` and `<REPO_NAME>` with your Artifactory instance details.