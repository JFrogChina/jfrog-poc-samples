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



#### Group: `tfs-dev`

* Role: Developer
* Permissions:

  * Deploy, Read, Annotate, Delete on selected repos (e.g., `tfs-dev-local`)
  * No access to Xray metadata configuration

#### Group: `tfs-security`

* Role: Security Engineer
* Permissions:

  * Manage Xray Policies, Watches
  * Manage Xray metadata on repos
  * Read access to necessary repos (optional)

### 🔐 Add Users to Groups

1. Go to **Identity & Access > Users**
2. Edit user `tfs-dev`, assign group `tfs-dev`
3. Edit user `tfs-security`, assign group `tfs-security`

---

## 📁 Repository and Permission Setup

### 🔐 Create Permission Target

1. Go to **Identity & Access > Permissions**
2. Create new target: `tfs-dev-permission`
3. Attach `tfs-dev-local` repository
4. Set group permissions:

| Group          | Read | Deploy | Delete | Annotate | Manage Xray Metadata |
| -------------- | ---- | ------ | ------ | -------- | -------------------- |
| `tfs-dev`      | ✔️   | ✔️     | ✔️     | ✔️       | ❌                    |
| `tfs-security` | ✔️   | ❌      | ❌      | ❌        | ✔️                   |


---

## 📦 Component Indexing and Scan Configuration

### Resource Types

| Resource Type | Description |
|--------------|-------------|
| Repositories | Indexes artifacts stored in JFrog Artifactory repositories. |
| Builds | Indexes CI/CD-generated builds, including all dependencies. |
| Release Bundles | Indexes software packaged for distribution. |

* Enable Xray indexing on key repositories like `tfs-dev-local`, `maven-local`, `docker-prod`.
* Avoid indexing temp/cached repositories like `*-cache`.
* Configure indexing filters to include only security-relevant files (`.jar`, `.tgz`, `.whl`, `.tar.gz`).
* Prefer build-based scan over per-file scan to optimize performance.

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
4. Set actions: Fail Build, Notify, Webhook

### 📖 Policy Naming Convention

```
<team>-<context>-<type>  e.g., frontend-prod-license-policy
```

### 🔍 Creating Watches

1. Navigate to **Platform -> Xray -> Watches**
2. Click **Create Watch**, set name and scope (repositories, builds, or bundles)
3. Attach previously created policies
4. Configure optional notifications (email/webhook/Slack)

### 📊 Policy + Watch Examples

| Use Case             | Target        | Rules                    | Action      |
| -------------------- | ------------- | ------------------------ | ----------- |
| Production security  | `tfs-dev-local` | CVSS Score = 10               | Block download  |
| CI License blocking  | `Build: ci-*` | License not in whitelist | Fail Build  |
| Audit-only licensing | All repos     | License is GPL           | Notify only |

---

## 🚀 CI/CD Integration

* Use **JFrog CLI** to trigger build scans:

```bash
 jf bs sample-maven-build 10 --rescan=true 
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

## ⚙️ Performance Optimization

* Exclude irrelevant file types from indexing (`.md`, `.txt`, `.log`).
* Regularly clean up old scan results and build info.

---

## 📄 Compliance and Licensing

* Maintain a **license whitelist** (MIT, Apache-2.0, BSD-3-Clause).
* Block GPL, AGPL, and unknown licenses via policy.
* Use Xray to export SBOMs in SPDX or CycloneDX format.

---


## 📃 References

* [JFrog Xray Documentation](https://docs.jfrog.com/xray/)
* [Xray REST API](https://jfrog.com/help/r/xray-rest-apis/)
* [Build Integration with Xray](https://jfrog.com/help/r/xray-documentation/build-integration)
* [Create Policies and Watches](https://jfrog.com/help/r/jfrog-platform-administration-documentation/create-xray-policies-and-watches)
* [Manage Permissions](https://jfrog.com/help/r/jfrog-platform-administration-documentation/permission-targets)

---

> 📌 Tip: Align Xray governance with internal security frameworks (e.g., ISO 27001, SLSA, SBOM strategy) to build a resilient supply chain.

