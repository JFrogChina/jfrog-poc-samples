
## 🛠️ Prerequisites

- Node.js and NPM installed
- JFrog CLI installed:  
  [Install JFrog CLI](https://jfrog.com/getcli)

## 🔧 Step 1: Configure JFrog CLI

1. Set Up JFrog CLI Configuration:

```bash
jf config add artifactory-server \
  --url=https://your-artifactory-domain/artifactory \
  --user=your-username \
  --password=your-password
```
## Step 2: Set Up NPM and Install Dependencies
jf npmc
jf npm install --build-name=npm-build --build-number=1  

## Step 3: Publish the Package with Build Info

# Publish the package to Artifactory
 jf npm publish --build-name=npm-build --build-number=1  

# Publish the build info to Artifactory
 jf rt bp npm-build 1   
