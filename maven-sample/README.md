# Maven-demo

## Prerequisites for Mac Users
Install Maven 3 and JFrog CLI
```sh
# Install Maven 3
brew install maven

# Install JFrog CLI
brew install jfrog-cli
```
   Otherwise, refer to the JFrog CLI documentation for other installation methods.

## Setting Up Repositories in Artifactory
Before proceeding with the commands below, ensure that you have configured three repositories in Artifactory:
- `maven-local`: A local repository for internal packages.
- `maven-remote`: A remote repository pointing to an external maven registry.
- `maven-virtual`: A virtual repository that aggregates both `maven-local` and `maven-remote`.
Set the `maven-local` as the default deployment repository.
<img width="961" alt="image" src="https://github.com/user-attachments/assets/739a4333-7cfc-4b0d-91e7-656ca9604bf8" />

<img width="790" alt="image" src="https://github.com/user-attachments/assets/695f4190-60d3-413c-9315-737ad59fd781" />

Your Maven builds and resolutions will typically point to `maven-virtual`.



## Step-by-Step Instructions
### Configure Artifactory (JFrog CLI config)
```bash
jf c add
```
<img width="530" alt="image" src="https://github.com/user-attachments/assets/24f208db-695b-48b9-bbf2-d6f27de2afcf" />

Follow the interactive prompts to add your Artifactory URL, credentials, and default repository settings.

### Configure the project's resolution repository (`maven-virtual`)
```bash
jf mvnc
```
<img width="1276" alt="image" src="https://github.com/user-attachments/assets/a9cda200-7031-4b8b-b8fe-5fd1ebd4456c" />

When prompted, specify the virtual repository name (e.g., `maven-virtual`).

## Index build by API
```dtd
 curl -u ${ARTIFACTORY_USER}:${artifactory_apikey_jfrog_io} -X POST "=https://${artifactory-server}/xray/api/v1/binMgr/builds" \
        -H "Content-Type: application/json" \
        -d '{
        "names": ["jas-demo"]
        }'

```

## Maven build and publish build info to Artifactory
Build the project, while deploying artifacts to Artifactory
```dtd
<!--jf mvn package-->
jf mvn clean install --build-name jas-demo --build-number 1
jf rt bag
jf rt bce jas-demo  1 
jf rt bp  jas-demo  1
```
<img width="1030" alt="image" src="https://github.com/user-attachments/assets/d2498229-b7f6-4b49-9d41-9c03d47b0e08" />
<img width="1273" alt="image" src="https://github.com/user-attachments/assets/062f4e38-a47f-4b05-aaa1-83c1bfc23b47" />

View Xray scan results from the out put of this command.
<img width="1537" alt="image" src="https://github.com/user-attachments/assets/2a5f2e64-3d9a-4862-9dcb-152951b5a104" />

<img width="1526" alt="image" src="https://github.com/user-attachments/assets/e2e84aea-570a-483b-bf72-3c571c85c926" />
<img width="1497" alt="image" src="https://github.com/user-attachments/assets/2a0a2c62-82e8-4278-8b42-6739580ee935" />


##  Docker build and scan
```
docker login acme.jfrog.io
docker build -t jas-demo:v1 .
docker tag jas-demo:v1 acme.jfrog.io/alexwang-docker/jas-demo:v1
docker push acme.jfrog.io/alexwang-docker/jas-demo:v1
jf docker push acme.jfrog.io/alex-docker/jas-demo:v1 --build-name=docker-app --build-number=1
jf rt bp docker-app 1
```
