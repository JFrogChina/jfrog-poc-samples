# 🔄 AWS STS Authentication Workflows: AssumeRole (with JFrog Operator) vs Passwordless IRSA (ASCII Diagrams)

This document shows and compares the workflows for:

1. **AssumeRole + JFrog Operator** (CI/CLI with auto secret rotation)
2. **Passwordless Access via IRSA** (for EKS Pods)

---

## 🔐 1. AssumeRole + JFrog Registry Operator (e.g., CI/CD with Secret Rotation)

```text
+------------------------+
| AWS CLI / CI Tool      |
+------------------------+
            |
            | 1. Call sts:AssumeRole
            v
+------------------------+
|   AWS STS Service      |
+------------------------+
            |
            | 2. Return temporary credentials:
            |    - AccessKeyId
            |    - SecretAccessKey
            |    - SessionToken
            v
+------------------------+
| JFrog Registry Operator|
| watches secret      |
+------------------------+
            |
            | 3. Operator uses creds to:
            |    - Authenticate to JFrog
            |    - Generate docker token
            |    - Update imagePullSecret
            v
+------------------------+
| Kubernetes Secret      |
| (type: dockerconfigjson)|
+------------------------+
            |
            | 4. Pod/container or CI job pulls image
            v
+------------------------+
|   JFrog Artifactory    |
+------------------------+
```

> ✅ Useful when your CI or automation has credentials and wants JFrog Operator to manage docker secrets for you.

---

## 🔐 2. Passwordless Access in EKS via IRSA (Native Mode)

```text
+------------------------+
|   Kubernetes Pod       |
| (uses IRSA + SA token) |
+------------------------+
            |
            | 1. Web Identity Token (JWT)
            v
+------------------------+
|  AWS OIDC Provider     |
+------------------------+
            |
            | 2. AssumeRoleWithWebIdentity
            v
+------------------------+
|   AWS STS Service      |
+------------------------+
            |
            | 3. Return temporary credentials
            v
+------------------------+
| JFrog Registry Operator|
| auto-injects dockercfg |
+------------------------+
            |
            | 4. Create imagePullSecret
            v
+------------------------+
| Kubernetes pulls image |
|  from JFrog registry   |
+------------------------+
```

---

## ✅ Comparison Summary

| Feature                   | AssumeRole + JFrog Operator       | IRSA Passwordless Mode         |
|---------------------------|-----------------------------------|-------------------------------|
| Use Case                  | CI pipelines, external automation | EKS-native workloads         
| Registry Operator used    | ✅ Yes                             | ✅ Yes                         |
| imagePullSecret created   | ✅ Yes                             | ✅ Yes                         |
| Secrets stored in pod     | ⚠️ Possibly (if manual export)     | ❌ No                          |
| Rotation handled          | ✅ By Operator                     | ✅ By Operator                 |

For more information about:
- AWS IAM AssumeRole capabilities, see [Setting Up JFrog's AssumeRole Capabilities in AWS](https://jfrog.com/help/r/setting-up-jfrog-s-assumerole-capabilities-in-aws/artifactory-setting-up-jfrog-s-assumerole-capabilities-in-aws)
- Passwordless Access, see [Passwordless Access for Amazon EKS](https://jfrog.com/help/r/jfrog-installation-setup-documentation/passwordless-access-for-amazon-eks)
