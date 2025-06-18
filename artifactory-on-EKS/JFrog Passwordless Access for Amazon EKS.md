# 🔐 JFrog Passwordless Access with AssumeRole for Amazon EKS – Workflow Diagram

This diagram illustrates the end-to-end workflow for enabling **Passwordless Access** to JFrog Artifactory from **Amazon EKS**, based on the official JFrog guide:

📄 https://jfrog.com/help/r/jfrog-installation-setup-documentation/passwordless-access-for-amazon-eks

---

## 🔄 Workflow: Passwordless Access in EKS using IRSA + JFrog Registry Operator

```text
+--------------------------+
|   1. EKS Pod Starts      |
|  (has IRSA-enabled SA)   |
+--------------------------+
            |
            | IAM Roles Service Accounts
            v
+-------------------------------+
| 2. AWS STS (OIDC + IRSA)     |
|  Pod calls STS:AssumeRole    |
|  with WebIdentity Token      |
+-------------------------------+
            |
            | STS returns:
            | - AccessKeyId
            | - SecretAccessKey
            | - SessionToken
            v
+------------------------------+
| 3. JFrog Registry Operator   |
| - Watches IRSA-enabled SA   |
| - Uses STS creds to call    |
|   JFrog Artifactory         |
| - Retrieves docker token    |
+------------------------------+
            |
            | Creates/updates
            | imagePullSecret:
            |  registry-credentials-<hash>
            v
+------------------------------+
| 4. Kubernetes Pod Pulls      |
|    Image using Secret        |
+------------------------------+
            |
            v
+------------------------------+
| 5. JFrog Artifactory         |
| Validates IAM identity,      |
| authorizes image pull        |
+------------------------------+
```

---

## ✅ Summary

- No password or API key required
- Secure authentication via IAM + IRSA + STS
- Secret is auto-managed and rotated by operator
- Pod uses generated imagePullSecret to pull securely

