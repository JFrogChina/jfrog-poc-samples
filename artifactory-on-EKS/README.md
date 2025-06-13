
# 🛠️ Creating a Docker Registry Secret for JFrog Artifactory in EKS Using IAM Role

This guide explains how to securely generate a `docker-registry` Kubernetes secret in EKS using **IAM Role for Service Account (IRSA)** + **AWS Secrets Manager** + **External Secrets Operator**, for authenticating with JFrog Artifactory's Docker registry.

---

## ✅ Architecture Overview

1. IAM Role is attached to an EKS ServiceAccount (IRSA)
2. The IAM Role has permissions to read AWS Secrets Manager
3. External Secrets Operator uses IRSA to sync secrets into Kubernetes
4. Pods use `imagePullSecrets: regcred` to pull from Artifactory securely

---

## 🔐 Step 1: Store Artifactory Credentials in AWS Secrets Manager

Create secret using:

```bash
aws secretsmanager create-secret \
  --name artifactory-docker-cred \
  --secret-string '{"username":"your-user","password":"your-token"}' \
  --region ap-east-1
```

✅ **Verify it was created:**

```bash
aws secretsmanager get-secret-value --secret-id artifactory-docker-cred --region ap-east-1
```

**Expected output (partial):**

```json
{
  "Name": "artifactory-docker-cred",
  "SecretString": "{\"username\":\"your-user\",\"password\":\"your-token\"}"
}
```

---

## 🔑 Step 2: Create IAM Policy

Create a JSON file `policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:<region>:<account-id>:secret:artifactory-docker-cred*"
    }
  ]
}
```

Then:

```bash
aws iam create-policy --policy-name JFrogDockerCredPolicy --policy-document file://policy.json
```

✅ **Verify policy exists:**

```bash
aws iam list-policies --query "Policies[?PolicyName=='JFrogDockerCredPolicy']"
```

---

## 🧾 Step 3: Bind IAM Role to ServiceAccount (IRSA)

```bash
eksctl create iamserviceaccount \
  --name artifactory-secret-sa \
  --namespace default \
  --cluster <your-cluster-name> \
  --attach-policy-arn arn:aws:iam::<account-id>:policy/JFrogDockerCredPolicy \
  --approve
```

✅ **Verify ServiceAccount is created:**

```bash
kubectl get sa artifactory-secret-sa -n default -o yaml
```

Should include:

```yaml
annotations:
  eks.amazonaws.com/role-arn: arn:aws:iam::<account-id>:role/...
```

---

## 📦 Step 4: Install External Secrets Operator

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets --create-namespace
```

✅ **Verify pods are running:**

```bash
kubectl get pods -n external-secrets
```

Expected:

```bash
NAME                                READY   STATUS    RESTARTS   AGE
external-secrets-...                1/1     Running   0          1m
```

---

## 🧩 Step 5: Create SecretStore

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: jfrog-secret-store
  namespace: default
spec:
  provider:
    aws:
      service: SecretsManager
      region: ap-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: artifactory-secret-sa
```

Apply it:

```bash
kubectl apply -f secretStore.yaml
```

✅ **Verify:**

```bash
kubectl get secretstore jfrog-secret-store -n default
```

---

## 🔁 Step 6: Create ExternalSecret for Docker Login

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: artifactory-docker-secret
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: jfrog-secret-store
    kind: SecretStore
  target:
    name: regcred
    template:
      type: kubernetes.io/dockerconfigjson
      data:
        .dockerconfigjson: |
          {
            "auths": {
              "https://<your-subdomain>.jfrog.io": {
                "username": "{{ .username }}",
                "password": "{{ .password }}",
                "auth": "{{ printf "%s:%s" .username .password | b64enc }}"
              }
            }
          }
  data:
    - secretKey: username
      remoteRef:
        key: artifactory-docker-cred
        property: username
    - secretKey: password
      remoteRef:
        key: artifactory-docker-cred
        property: password
```

✅ **Apply and check:**

```bash
kubectl apply -f externalSecret.yaml
kubectl get secret regcred -n default
```

You should see:

```
NAME      TYPE                             DATA   AGE
regcred   kubernetes.io/dockerconfigjson   1      30s
```

---

## 🚀 Step 7: Use the Docker Secret in Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-artifactory
spec:
  serviceAccountName: artifactory-secret-sa
  containers:
    - name: app
      image: <your-subdomain>.jfrog.io/alex-docker-local/jas-demo:v1
  imagePullSecrets:
    - name: regcred
```

✅ **Verify image pull:**

```bash
kubectl describe pod test-artifactory
```

Ensure there is **no `ImagePullBackOff` or `ErrImagePull`** and the container becomes `Running`.

---

## ✅ Summary Table

| Component           | Purpose                                  |
|---------------------|------------------------------------------|
| AWS Secrets Manager | Stores Artifactory credentials           |
| IAM Role (IRSA)     | Grants fine-grained access to secrets    |
| External Secrets    | Syncs secret into Kubernetes             |
| imagePullSecrets    | Used by Pod to authenticate to registry  |

---

This setup avoids hardcoding credentials in manifests and enables secure, auto-updated docker login to JFrog Artifactory via IAM.
