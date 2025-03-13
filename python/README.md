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

### Create Artifactory Repositories for PyPI
#### Create a Local Repository
1. Log in to your Artifactory instance.
2. Go to the "Admin" tab.
3. Under "Repositories", select "Local".
4. Click "New" and choose "pypi" as the package type.
5. Name the repository (e.g., `pypi-local`).
6. Save the repository.

#### Create a Remote Repository
1. Under "Repositories", select "Remote".
2. Click "New" and choose "pypi" as the package type.
3. Name the repository (e.g., `pypi-remote`).
4. Set the URL to the PyPI registry (e.g., `https://pypi.org`).
5. Save the repository.

#### Create a Virtual Repository
1. Under "Repositories", select "Virtual".
2. Click "New" and choose "pypi" as the package type.
3. Name the repository (e.g., `pypi-virtual`).
4. Add the local and remote repositories created earlier to the virtual repository.
5. Save the repository.

### Add the Local Repository to JFrog Xray Indexed Repositories
1. Log in to your JFrog Platform.
2. Go to the "Administrator" module.
3. Navigate to "Xray" > "Index Repositories".
4. Click "Add Repositories".
5. Select the local repository (e.g., `pypi-local`) to be indexed by Xray.
6. Save the changes.

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