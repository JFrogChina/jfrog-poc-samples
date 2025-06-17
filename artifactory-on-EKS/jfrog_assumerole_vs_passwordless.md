# 🔐 AWS AssumeRole vs JFrog Passwordless Access on Amazon EKS

This document compares **AWS IAM AssumeRole** with **JFrog's Passwordless Access** mechanism, especially in the context of using JFrog Artifactory from Amazon EKS.

---

## 🧩 Conceptual Difference

| Concept         | AssumeRole                                     | Passwordless Access                                |
|-----------------|------------------------------------------------|----------------------------------------------------|
| What is it?     | AWS IAM feature: assume an identity via STS    | JFrog feature: authenticate using IAM identity     |
| Who handles it? | AWS client assumes a role                      | JFrog maps IAM identity to a JFrog user            |
| Credential type | Temporary STS token                            | No credentials stored in workload                  |

For more information about:
- AWS IAM AssumeRole capabilities, see [Setting Up JFrog's AssumeRole Capabilities in AWS](https://jfrog.com/help/r/setting-up-jfrog-s-assumerole-capabilities-in-aws/artifactory-setting-up-jfrog-s-assumerole-capabilities-in-aws)
- Passwordless Access, see [Passwordless Access for Amazon EKS](https://jfrog.com/help/r/jfrog-installation-setup-documentation/passwordless-access-for-amazon-eks)

---

## 🔁 Relationship

✅ **Passwordless access is built on top of AWS AssumeRole**  
EKS IRSA uses `sts:AssumeRoleWithWebIdentity` to assume an IAM Role. JFrog maps that role to a user, enabling passwordless access.

---


## 🎯 Use Case Scenarios

| Scenario                                        | Use AssumeRole | Use Passwordless |
|------------------------------------------------|----------------|------------------|
| EC2 or Lambda accessing Artifactory            | ✅ Yes         | ❌ No             |
| EKS Pod pulling Docker image                   | ✅ Yes         | ✅ Best         

---

## ✅ Summary Table

| Feature                | AssumeRole                           | Passwordless Access                        |
|------------------------|--------------------------------------|---------------------------------------------|
| Mechanism              | AWS STS + temporary credentials      | IAM Role via IRSA mapped to JFrog user      |
| Scope                  | Broad AWS (EC2, Lambda, EKS, CLI)    | EKS with IRSA only                       
| Secrets required       | Temporary credentials (exported)     | ❌ None                                      |
| Best for               | CI/CD, general AWS services          | Kubernetes-native container access          |

---
