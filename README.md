# 🏗️ JFrog SaaS Trial Workshop Guide

Welcome to the JFrog SaaS Trial Workshop! 🎓 This guide will help you get started with JFrog SaaS, set up your trial environment, and practice building a Maven project using our GitHub sample repository.

---

## Prerequisite
- Java 8 and above
- Maven 3.6.x

## 🚀 1. Apply for a JFrog SaaS Trial

Before we begin, please apply for a JFrog SaaS trial environment:

👉 [Apply for JFrog SaaS Trial](https://jfrog.com/start-free/)

After registering, you will receive access to your own JFrog Platform instance in the cloud. Please ensure you have access to:

✅ **JFrog Artifactory (SaaS)**  
✅ **JFrog Xray (Optional)**

---

## 📦 2. Clone the Sample Maven Project

We will use a pre-prepared Maven project from the JFrog China GitHub repository as an example.

1️⃣ Clone the project:
```bash
git clone https://github.com/JFrogChina/jfrog-poc-samples.git
cd jfrog-poc-samples/maven-sample
2️⃣ Review the project structure:



maven-sample/
├── pom.xml
├── src/
│   └── ...
└── ...
This is a simple Java Maven project for demonstration purposes.

🏗️ 3. Create Maven Repositories Using Quick Repository Creation
🔹 3.1 Use Quick Repository Creation (Recommended for New Users)
1️⃣ Log in to your JFrog SaaS Platform.
2️⃣ In the top-right corner, click the Quick Repository Creation.
3️⃣ Select Maven as the package type.
4️⃣ Follow the prompts to quickly create:

A Local Repository (e.g., sample-maven-local)

A Remote Repository (e.g., sample-maven-remote, pointing to https://repo.maven.apache.org/maven2/)

A Virtual Repository (e.g., sample-maven, combining sample-maven-local and sample-maven-remote)

The Quick Setup will automatically configure the repositories and generate helpful examples.

✅ Verify that:

Local Repo: sample-maven-local

Remote Repo: sample-maven-remote

Virtual Repo: sample-maven (used for builds and dependency resolution)

🔗 4. Configure JFrog CLI
We will use JFrog CLI to interact with the JFrog SaaS environment.

1️⃣ Download JFrog CLI:
👉 JFrog CLI Download

2️⃣ Configure your SaaS environment (replace <YOUR_DOMAIN> with your JFrog SaaS domain):

bash

jf c add saas
Follow the prompts:

JFrog Platform URL: https://<YOUR_DOMAIN>.jfrog.io

Username: <your-username>

Password: <your-encrypted-password> (not plain password, but the encrypted password generated in JFrog UI)

🔑 How to get your Encrypted Password
Login to your JFrog SaaS UI.

Go to Profile (top-right) → Edit Profile → Generate Encrypted Password.

Copy the generated encrypted password and use it in the CLI configuration.

🛠️ 5. Configure Maven with jf mvnc
Run the following to configure Maven:

bash

cd maven-sample
jf mvnc
Follow the prompts:

pgsql

Resolve dependencies from Artifactory? (y/n) [y]?
Set Artifactory server ID [saas]: 
Set resolution repository for release dependencies [sample-maven]: 
Set resolution repository for snapshot dependencies [sample-maven]: 
Deploy project artifacts to Artifactory? (y/n) [y]?
Set Artifactory server ID [saas]: 
Set repository for release artifacts deployment [sample-maven-local]: 
Set repository for snapshot artifacts deployment [sample-maven-local]: 
Would you like to filter out some of the deployed artifacts? (y/n) [n]? 
Use Maven wrapper? (y/n) [y]? 
✅ jf mvnc will automatically generate a settings.xml that points to your SaaS repositories.

🏗️ 6. Build and Deploy the Maven Project
Run the following commands to build and deploy the project to your SaaS instance:

bash

jf mvn clean install -f pom.xml --build-name=sample-maven-build --build-number=1
jf mvn deploy --build-name=sample-maven-build --build-number=1
jf rt bp sample-maven-build 1
This will:

Compile and package the project.

Upload artifacts (e.g., .jar files) to the sample-maven-local repository.

Record build information.

🔍 7. Verify in JFrog Platform
Login to your JFrog SaaS instance:

✅ Navigate to Artifactory → Artifacts to see your deployed artifacts.
✅ Navigate to Builds to view the build information (sample-maven-build).

