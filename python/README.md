# Python Build Instructions with JFrog Artifactory

## Prerequisites (especially for macOS users)
1. **Python and pip**  
   Ensure that Python (3.x preferred) and pip are installed.  
   *You can verify by running:*  
   ```bash
   python --version
   pip --version
   ```

2. **JFrog CLI**  
   Install the JFrog CLI. If you have Homebrew on macOS, you can do:
   ```bash
   brew install jfrog-cli
   ```
   Otherwise, refer to the JFrog CLI documentation for other installation methods.

## Setting Up Repositories in Artifactory
Before proceeding with the commands below, ensure that you have configured three repositories in Artifactory:
- `pypi-local`: A local repository for internal packages.
- `pypi-remote`: A remote repository pointing to an external PyPI registry.
- `pypi-virtual`: A virtual repository that aggregates both `pypi-local` and `pypi-remote`.

Your Python builds and resolutions will typically point to `pypi-virtual`.

## Step-by-Step Instructions
### Configure Artifactory (JFrog CLI config)
```bash
jf c add
```
Follow the interactive prompts to add your Artifactory URL, credentials, and default repository settings.

### Configure the project's resolution repository (`pypi-virtual`)
```bash
jf rt pipc
```
When prompted, specify the virtual repository name (e.g., `pypi-virtual`).

### Install project dependencies with pip from Artifactory
```bash
jf rt pipi -r requirements.txt --build-name=my-pip-build --build-number=1 --module=jfrog-python-example
```

### Configure JFrog Xray to Scan All Builds
Before building, ensure that JFrog Xray is configured to scan all builds:

Refer to this link: https://jfrog.com/help/r/xray-how-to-index-and-scan-all-builds-in-xray-in-the-unified-platform/xray-how-to-index-and-scan-all-builds-in-xray-in-the-unified-platform

### Package the project
Create distribution archives (tar.gz and whl):
```bash
python setup.py sdist bdist_wheel
```
This command will generate `.tar.gz` and `.whl` files under the `dist/` directory.

### Upload the packages to the pypi repository in Artifactory:
```bash
jf rt u dist/ pypi-virtual/ --build-name=my-pip-build --build-number=1 --module=jfrog-python-example
```
Adjust `pypi-virtual/` to your specific repository path if needed (e.g., `pypi-local/` or your virtual repository).

### Collect environment variables
Add them to the build info:
```bash
jf rt bce my-pip-build 1
```

### Publish the build info to Artifactory:
```bash
jf rt bp my-pip-build 1
```

## Summary
By following these steps, you will configure Artifactory, install your dependencies from a virtual PyPI repository, build your Python distribution artifacts, upload them to Artifactory, and record build information that can be tracked via the Artifactory build browser.

Happy Building!