
# ☁️ Integrating CloudBees with JFrog SaaS Using JFrog CLI

This guide walks you through integrating **CloudBees CI/CD** pipelines with **JFrog SaaS** using **JFrog CLI**, including verification steps for each action.

---

## 🔧 Prerequisites

- A running CloudBees CI controller with access to the internet.
- A JFrog SaaS instance (e.g., `https://yourcompany.jfrog.io`).
- JFrog CLI installed on CloudBees agents.
- Access Token or Username/Password credentials for JFrog.

---

## 🪪 Step 1: Configure JFrog CLI on CloudBees Agent

```bash
jf config add jfrog-server \
  --url=https://yourcompany.jfrog.io \
  --access-token=<YOUR_ACCESS_TOKEN> \
  --interactive=false
```

✅ **Verify configuration:**

```bash
jf config show
```

Expected output includes:

```
Server ID: jfrog-server
URL: https://yourcompany.jfrog.io
```

---

## 📦 Step 2: Upload Build Artifacts to JFrog Artifactory

```bash
jf rt u "build-output/*" generic-local/ci-builds/ --build-name=my-build --build-number=1
```

✅ **Verify artifact upload:**

```bash
jf rt s "generic-local/ci-builds/*"
```

Expected result shows the uploaded files.

---

## 🔐 Step 3: Collect Build Info

```bash
jf rt bce my-build 1
jf rt bp my-build 1
```

✅ **Verify build published:**

```bash
jf rt curl /api/build/my-build/1
```

Expected JSON with module info and artifact list.

---

## 🛡️ Step 4: Scan Build with Xray

```bash
jf xr bscan my-build 1
```

✅ **Verify scan status:**

```bash
jf xr bs my-build 1
```

Expected:

```
Scan completed successfully
```

Or results showing violations or vulnerabilities.

---

## 🧪 Step 5: Block Pipeline on Critical Vulnerabilities (Optional)

Use shell/Jenkins step to fail on policy violation:

```bash
result=$(jf xr bs my-build 1 --output=json)
echo "$result" | jq '.summary.fail_build' | grep true && exit 1
```

✅ **Expected behavior:**

- Pipeline exits with error if critical vulnerabilities found.

---

## 📤 Step 6: Promote or Distribute Build (Optional)

```bash
jf rt bpr my-build 1 generic-release-local --status=Released
```

✅ **Verify promotion:**

```bash
jf rt curl /api/build/promotions/my-build/1
```

---

## 🧠 Summary Table

| Step | Action                            | Verification                     |
|------|-----------------------------------|----------------------------------|
| 1    | Configure JFrog CLI               | `jf config show`                 |
| 2    | Upload Artifacts                  | `jf rt s`                        |
| 3    | Publish Build Info                | `jf rt curl /api/build/...`      |
| 4    | Scan with Xray                    | `jf xr bs`                       |
| 5    | Optional: Fail on Violation       | `jq '.summary.fail_build'`       |
| 6    | Promote or Distribute Build       | `jf rt curl /api/build/promotions/...` |

---

## 🔁 Bonus: Use in Jenkinsfile

```groovy
pipeline {
  agent any
  environment {
    JFROG_CLI_BUILD_NAME = "my-build"
    JFROG_CLI_BUILD_NUMBER = "${BUILD_NUMBER}"
  }
  stages {
    stage('Upload') {
      steps {
        sh 'jf rt u "build/*" generic-local/ci-builds/'
      }
    }
    stage('Publish Build Info') {
      steps {
        sh 'jf rt bce'
        sh 'jf rt bp'
      }
    }
    stage('Scan') {
      steps {
        sh 'jf xr bscan'
        sh 'jf xr bs'
      }
    }
  }
}
```

This enables end-to-end integration with verification for every step using JFrog CLI in a CloudBees environment.
