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

Your Maven builds and resolutions will typically point to `maven-virtual`.

## Step-by-Step Instructions
### Configure Artifactory (JFrog CLI config)
```bash
jf c add
```
Follow the interactive prompts to add your Artifactory URL, credentials, and default repository settings.

### Configure the project's resolution repository (`maven-virtual`)
```bash
jf mvnc
```
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

##  Docker build and scan
```
docker login acme.jfrog.io
docker build -t jas-demo:v1 .
docker tag jas-demo:v1 acme.jfrog.io/alexwang-docker/jas-demo:v1
docker push acme.jfrog.io/alexwang-docker/jas-demo:v1
jf docker push acme.jfrog.io/alex-docker/jas-demo:v1 --build-name=docker-app --build-number=1
jf rt bp docker-app 1
```
