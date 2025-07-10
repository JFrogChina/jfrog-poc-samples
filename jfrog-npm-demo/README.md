
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
## Step 2: Create NPM repo and Set Up NPM and Install Dependencies

1. Create NPM repo
<img width="971" alt="image" src="https://github.com/user-attachments/assets/65c2f1b1-8fe0-4010-8932-8faaa2af0431" />

<img width="964" alt="image" src="https://github.com/user-attachments/assets/f24a2d4d-6ac9-4e48-bc91-0535b29ef5a5" />

```
jf npmc
jf npm install --build-name=npm-build --build-number=1  
```
<img width="741" alt="image" src="https://github.com/user-attachments/assets/9e685d47-cc77-4f24-be25-2d3fe883fdb2" />

<img width="603" alt="image" src="https://github.com/user-attachments/assets/29a5183f-b8be-4d22-8f5f-3ed98b1bd9e4" />

## Step 3: Publish the Package with Build Info

# Publish the package to Artifactory
 jf npm publish --build-name=npm-build --build-number=1  
<img width="1270" alt="image" src="https://github.com/user-attachments/assets/ce76c1ea-14d4-47b3-8daa-93c4e105c09c" />

# Publish the build info to Artifactory
 jf rt bp npm-build 1   
 <img width="1276" alt="image" src="https://github.com/user-attachments/assets/48310c9b-6458-4894-96ce-8cd09db6ee26" />

<img width="1529" alt="image" src="https://github.com/user-attachments/assets/8f1f7dec-54dc-4531-8f35-083b1476c59a" />
<img width="1518" alt="image" src="https://github.com/user-attachments/assets/bece7660-8151-4026-922e-d6666d81160a" />

