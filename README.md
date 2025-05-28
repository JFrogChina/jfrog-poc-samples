# 🏗️ JFrog SaaS Trial Workshop Guide

Welcome to the **JFrog SaaS Trial Workshop!** 🎓  
This guide will help you get started with JFrog SaaS, set up your trial environment, and practice building a Maven project using our GitHub sample repository.

---

## 📝 Prerequisites

- **Java** 8 or above
- **Maven** 3.6.x or above

---

## 🚀 1. Apply for a JFrog SaaS Trial

1. [Apply for JFrog SaaS Trial](https://jfrog.com/start-free/)
2. After registering, you will receive access to your own JFrog Platform instance in the cloud.  
   Please ensure you have access to:
   - ✅ **JFrog Artifactory (SaaS)**
   - ✅ **JFrog Xray** 
   - ✅ **JFrog Advanced Security** 

---

## 📦 2. Clone the Sample Maven Project

1. Clone the project:
   ```bash
   git clone https://github.com/JFrogChina/jfrog-poc-samples.git
   cd jfrog-poc-samples/maven-sample
   ```
2. Review the project structure (a simple Java Maven project for demonstration).

---

## 🏗️ 3. Create Maven Repositories (Quick Repository Creation)

1. Log in to your JFrog SaaS Platform.
2. Click **Quick Repository Creation** (top-right).
3. Select **Maven** as the package type.
4. Follow the prompts to create:
   - Local Repository (e.g., `sample-maven-local`)
   - Remote Repository (e.g., `sample-maven-remote`)
   - Virtual Repository (e.g., `sample-maven`, combining the above)
5. **Verify:**
   - Local Repo: `sample-maven-local`
   - Remote Repo: `sample-maven-remote`
   - Virtual Repo: `sample-maven` (for builds and dependency resolution)

---

## 🔗 4. Configure JFrog CLI

We will use JFrog CLI to interact with the JFrog SaaS environment.

1. [Download JFrog CLI](https://jfrog.com/getcli/)
2. Configure your SaaS environment (replace `<YOUR_DOMAIN>` with your JFrog SaaS domain):

   ```shell
   jf c add saas
   ```

   Follow the prompts:
   ```
   JFrog Platform URL: https://<YOUR_DOMAIN>.jfrog.io
   Username: <your-username>
   Password: <your-encrypted-password>
   ```

   > **How to get your Encrypted Password:**  
   > Log in to your JFrog SaaS UI → Profile (top-right) → Edit Profile → Generate Encrypted Password.

---

## 🛠️ 5. Configure Maven with `jf mvnc`

1. Run the following to configure Maven:
   ```shell
   cd maven-sample
   jf mvnc
   ```
2. Follow the prompts to set up repositories and deployment.
3. `jf mvnc` will automatically generate a `settings.xml` pointing to your SaaS repositories.

---

## 🏗️ 6. Build and Deploy the Maven Project

Run the following commands to build and deploy the project to your SaaS instance:

```shell
jf mvn clean install -f pom.xml --build-name=sample-maven-build --build-number=1
jf mvn deploy --build-name=sample-maven-build --build-number=1
jf rt bp sample-maven-build 1
```

- Compiles and packages the project
- Uploads artifacts (e.g., `.jar` files) to `sample-maven-local`
- Records build information

---

## 🔍 7. Verify in JFrog Platform

- Log in to your JFrog SaaS instance:
  - Go to **Artifactory → Artifacts** to see your deployed artifacts.
  - Go to **Builds** to view build information (`sample-maven-build`).

---

## 🔒 8. Enable Xray Indexing for Security Scanning

1. Go to **JFrog Xray → Index Resource**.
2. Add the following resources to the watch:
   - Repositories: `sample-maven-local`
   - Builds: `sample-maven-build`
3. Xray will now scan both the repository and your build for vulnerabilities, licenses, and compliance issues.

---

## 🛡️ 9. Demonstrate and Remediate log4j Vulnerability

### 9.1 Review the log4j Vulnerability

![img_1.png](img_1.png)


### Review the JFrog advanced security result to reduce the false positives
   ![image.png](image.png)

> **Great! JFrog advanced security found out 86% of critical/high vulnerabilities are false positives.**


![image-1.png](image-1.png)

---
### 9.2 Curation: Block log4j-2.14.0.jar

1. **Create a condition to block `log4j-2.14.0.jar`:**  
   Administrator → Curation Settings → Create Condition  
   ![img.png](img.png)

2. **Create a curation policy containing this condition:**  
   ![img_2.png](img_2.png)

3. **Clean the local and remote repository cache:**
   ```bash
   rm -rf ~/.m2/repository/org/apache/logging/log4j/*
   ```

4. **Try to pull `log4j-2.14.0.jar` again:**  
   You should see an error indicating the artifact is blocked.

   ```shell
   [main] ERROR org.apache.maven.cli.MavenCli - Failed to execute goal on project app-boot: Could not resolve dependencies for project com.example.jfrog:app-boot:war:1.0.2: Could not transfer artifact org.apache.logging.log4j:log4j-core:jar:2.14.0 from/to artifactory-release (https://demo.jfrogchina.com/artifactory/alex-maven): authorization failed for https://demo.jfrogchina.com/artifactory/alex-maven/org/apache/logging/log4j/log4j-core/2.14.0/log4j-core-2.14.0.jar, status: 403 Forbidden -> [Help 1]
   ...
   ```
   ![img_3.png](img_3.png)

5. **Upgrade the log4j version to 2.17 to fix the issue:**  
   Edit `pom.xml`:
   ```xml
   <dependency>
       <groupId>org.apache.logging.log4j</groupId>
       <artifactId>log4j-core</artifactId>
       <version>2.17.1</version>
   </dependency>
   ```

6. **Rebuild and redeploy to see the scan results:**
   ```shell
   jf mvn clean
   jf mvn deploy --build-name=sample-maven-build --build-number=2
   jf rt bp sample-maven-build 2
   ```

---

> **Happy building and stay secure! 🚀**