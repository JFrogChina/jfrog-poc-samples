# 🛡️ JFrog Xray Best Practices Guide

This document outlines best practices for using **JFrog Xray** to ensure software supply chain security. It includes configuration recommendations, CI/CD integration, policy/watch setup, role-based access control, and more.

---

## 🔍 Table of Contents

1. [User Groups and Permissions](#user-groups-and-permissions)
2. [Environment Preparation](#environment-preparation)
3. [Component Indexing and Scan Configuration](#component-indexing-and-scan-configuration)
4. [Policies and Watches](#policies-and-watches)
5. [CI/CD Integration](#cicd-integration)
6. [Risk Management](#risk-management)
7. [Performance Optimization](#performance-optimization)
8. [Compliance and Licensing](#compliance-and-licensing)
9. [Monitoring and Auditing](#monitoring-and-auditing)
10. [References](#references)

---

## 👥 User Groups and Permissions

### 🔧 Create User Groups
![](2025-06-06-14-52-57.png)


#### Group: `app-dev`

* Role: Developer
* Permissions:

  * Deploy, Read, Annotate, Delete on selected repos (e.g., `app-dev-local`)
  * No access to Xray metadata configuration

#### Group: `app-security`

* Role: Security Engineer
* Permissions:

  * Manage Xray Policies, Watches
  * Manage Xray metadata on repos
  * Read access to necessary repos (optional)

### 🔐 Add Users to Groups

1. Go to **Identity & Access > Users**
2. Edit user `app-dev`, assign group `app-dev`
3. Edit user `app-security`, assign group `app-security`

---

## 📁 Repository and Permission Setup

### 🔐 Create Permission Target
![](2025-06-06-14-54-28.png)
1. Go to **administration & User Management > Permissions**
2. Create new target: `app-dev-permission`
3. Attach `app-dev-local` repository
4. Set group permissions:

| Group          | Read | Deploy | Delete | Annotate | Manage Xray Metadata |
| -------------- | ---- | ------ | ------ | -------- | -------------------- |
| `app-dev`      | ✔️   | ✔️     | ✔️     | ✔️       | ❌                    |
| `app-security` | ✔️   | ❌      | ❌      | ❌        | ✔️                   |


---

## 📦 Indexing Repository and Builds
![](2025-06-06-14-56-31.png)
### Resource Types

| Resource Type | Description |
|--------------|-------------|
| Repositories | Indexes artifacts stored in JFrog Artifactory repositories. |
| Builds | Indexes CI/CD-generated builds, including all dependencies. |
| Release Bundles | Indexes software packaged for distribution. |

* Enable Xray indexing on key repositories like `app-dev-local`, `maven-local`, `docker-prod`.
* Avoid indexing temp/cached repositories like `*-cache`.

---

## 📝 Policies and Watches

### 🔧 Creating Policies

1. Navigate to **Platform -> Xray -> Policies**.
2. Click **Create Policy**, then:

   * Name: `backend-prod-vuln-policy`
   * Type: `Security`, `License`, or `Operational Risk`
3. Add rules:

   * Security: CVE severity ≥ High or CVSS ≥ 9.0
   * License: Not in whitelist
   * Operational: Unscannable component
4. Set actions: Fail Build, Block

### 📖 Policy Naming Convention

```
<team>-<context>-<type>  e.g., frontend-prod-license-policy
```

### 🔍 Creating Watches
![](2025-06-06-15-12-29.png)
1. Navigate to **Platform -> Xray -> Watches**
2. Click **Create Watch**, set name and scope (repositories, builds, or bundles)
3. Attach previously created policies


### 📊 Policy + Watch Examples

| Use Case             | Target        | Rules                    | Action      |
| -------------------- | ------------- | ------------------------ | ----------- |
| Production security  | `app-dev-local` | CVSS Score = 10               | Block download  |
| CI License blocking  | `Build: ci-*` | License not in whitelist | Fail Build  |
| Audit-only licensing | All repos     | License is GPL           | Notify only |

---

## 🚀 CI/CD Integration

* 创建 Maven build
参考 [Maven Build Sample](https://github.com/JFrogChina/jfrog-poc-samples/tree/main/maven-sample)

* Use **JFrog CLI** to trigger build scans:

```bash
 jf bs sample-maven-build 1 --rescan=true 
```
* Pipeline steps:

  1. Build & Upload Artifacts
  2. Upload Build Info
  3. Trigger Xray scan via CLI
  4. Enforce result-based gating (fail if policy violated)

---

## ⚡ Risk Management

* Log all unscannable components for investigation.
* Use **Contextual Analysis** to reduce false positives.
* Enable "Reachable Vulnerabilities" for advanced CVE tracing.


---

## 📄 Compliance and Licensing

* Maintain a **license whitelist** (MIT, Apache-2.0, BSD-3-Clause).
* Block GPL, AGPL, and unknown licenses via policy.
* Use Xray to export SBOMs in SPDX or CycloneDX format.

---


## 📃 References

* [JFrog Xray Documentation](https://jfrog.com/help/r/jfrog-security-user-guide/products/xray)

---


