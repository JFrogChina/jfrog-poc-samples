# Signing and Verifying Docker Images with Cosign on macOS

This document provides a complete guide for signing Docker images using [Sigstore Cosign](https://docs.sigstore.dev/cosign/overview/) on **macOS**, including keyless signing and verification.

Example Docker image:
```
test.jfrog.io/alex-docker-local/jas-demo:v4
```

---

## 📦 1. Environment Setup

### 1.1 Install Cosign

```bash
brew install cosign
```

Check installation:

```bash
cosign version
```

Expected output:
```
GitVersion:    v2.2.4
GitCommit:     ...
GoVersion:     go1.22
```

---

### 1.2 Login to JFrog Artifactory Docker Registry

```bash
docker login test.jfrog.io
```

Provide username and password (or API Key / Access Token).

---

## 🔐 2. Signing Docker Images with Cosign

### 2.1 Keyless Signing (Recommended)

Cosign supports OIDC-based authentication (e.g., Google, GitHub) without manual key management.

```bash
export COSIGN_EXPERIMENTAL=1

cosign sign test.jfrog.io/alex-docker-local/jas-demo:v4
```

A browser window will open for authentication (e.g., Google account). Successful output:

```
Generating ephemeral keys...
Retrieving signed certificate...
Successfully verified SCT...
tlog entry created with index: 12709320
Pushed signature to: test.jfrog.io/alex-docker-local/jas-demo
```

The image signature is now stored in the remote registry.

---

## 🔍 3. Verifying Signatures

### 3.1 Automatic Verification

```bash
COSIGN_EXPERIMENTAL=1 cosign verify test.jfrog.io/alex-docker-local/jas-demo:v4
```

Successful output example:

```
Verification for test.jfrog.io/alex-docker-local/jas-demo:v4 --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - The signatures were verified against the transparency log
  - The certificate was verified against the Fulcio root CA
  - Certificate subject: yourmail@gmail.com
  - Certificate issuer: https://accounts.google.com
```

---

### 3.2 Specify Signer Identity for Verification

If you encounter:
```
Error: --certificate-identity or --certificate-identity-regexp is required for verification in keyless mode
```

You need to specify the signer identity:

```bash
COSIGN_EXPERIMENTAL=1 cosign verify \
  --certificate-identity "your-email@example.com" \
  --certificate-oidc-issuer "https://accounts.google.com" \
  test.jfrog.io/alex-docker-local/jas-demo:v4
```

---

### 3.3 Handling Identity Mismatch Errors

Common error:
```
no matching signatures: none of the expected identities matched what was in the certificate, got subjects [yourmail@gmail.com] with issuer https://accounts.google.com
```

✅ **Cause:** The signing account differs from the verification identity.

✅ **Solution:**

1️⃣ Check the actual signer identity:
```bash
COSIGN_EXPERIMENTAL=1 cosign verify --insecure-ignore-tlog test.jfrog.io/alex-docker-local/jas-demo:v4
```

2️⃣ Use the correct identity from the output:
```bash
COSIGN_EXPERIMENTAL=1 cosign verify \
  --certificate-identity "yourmail@gmail.com" \
  --certificate-oidc-issuer "https://accounts.google.com" \
  test.jfrog.io/alex-docker-local/jas-demo:v4
```

---

## 📋 4. Advanced Usage

### 4.1 Output Signature Information as JSON

```bash
COSIGN_EXPERIMENTAL=1 cosign verify \
  --certificate-identity "yourmail@gmail.com" \
  --certificate-oidc-issuer "https://accounts.google.com" \
  --output json \
  test.jfrog.io/alex-docker-local/jas-demo:v4 | jq
```

### 4.2 Use Regular Expression for Identity (Team Scenario)

```bash
COSIGN_EXPERIMENTAL=1 cosign verify \
  --certificate-identity-regexp ".*@jfrog\.com" \
  --certificate-oidc-issuer "https://accounts.google.com" \
  test.jfrog.io/alex-docker-local/jas-demo:v4
```

---

## 🧩 5. Common Issues Summary

| Issue | Cause | Solution |
|------|------|-----------|
| `--certificate-identity required` | Identity not specified | Add `--certificate-identity` parameter |
| `no matching signatures` | Signer email mismatch | Use the actual signing email |
| `nil certificate provided` | Image not signed or pull failed | Confirm the image is signed successfully |
| `tlog not found` | Network or transparency log issue | Use `--insecure-ignore-tlog` to bypass temporarily |

---

## ✅ 6. References

- [Sigstore Cosign Official Documentation](https://docs.sigstore.dev/cosign/overview/)
- [JFrog Docker Registry User Guide](https://jfrog.com/help/r/jfrog-artifactory-documentation/docker-registry)
- [Fulcio Root CA and OIDC Signing Mechanism](https://fulcio.sigstore.dev)

---

**Last Updated: 2025-10-23**  
macOS 13+  |  Cosign v2.x, Docker 24+, JFrog Artifactory 7.x+
