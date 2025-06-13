
# 🧩 Azure DevOps 與 JFrog Artifactory/Xray 整合詳解（使用 JFrog CLI）

本文件說明如何將 JFrog Artifactory 與 Azure DevOps 整合，並使用 JFrog CLI 完成制品管理與建置安全掃描，實現 DevSecOps 流程。

---

## 📋 前提條件

- ✅ Azure DevOps 專案已建立
- ✅ 擁有 JFrog SaaS 訂閱（Artifactory + Xray 功能）
- ✅ 已建立可用於 CLI 的使用者（API Key 或 Access Token）
- ✅ 建立 Azure DevOps Secure Variable Group：`JFROG_USER`、`JFROG_TOKEN`

---

## ⚙️ 步驟一：安裝 JFrog CLI 至 Azure DevOps Agent

```yaml
steps:
- script: |
    curl -fL https://getcli.jfrog.io | sh
    ./jf --version
  displayName: 'Install JFrog CLI'
```

---

## 📁 步驟二：設定 Artifactory 連線資訊

```yaml
steps:
- script: |
    ./jf config add artifactory-server \
      --url https://<your-domain>.jfrog.io/artifactory \
      --user $(JFROG_USER) \
      --password $(JFROG_TOKEN) \
      --interactive=false
  displayName: 'Configure JFrog CLI'
```

---

## 📦 步驟三：上傳建置產出至 Artifactory

```yaml
steps:
- script: |
    ./jf rt upload "build/libs/*.jar" libs-release-local/$(Build.BuildId)/ \
      --build-name=sample-app \
      --build-number=$(Build.BuildId)
  displayName: 'Upload Artifacts to Artifactory'
```

---

## 🧱 步驟四：收集建置資訊並發布 Build Info

```yaml
steps:
- script: |
    ./jf rt build-collect-env sample-app $(Build.BuildId)
    ./jf rt build-add-git sample-app $(Build.BuildId)
    ./jf rt build-publish sample-app $(Build.BuildId)
  displayName: 'Publish Build Info'
```

---

## 🛡️ 步驟五：執行 JFrog Xray 掃描

```yaml
steps:
- script: |
    ./jf xr scan sample-app $(Build.BuildId) || exit 1
  displayName: 'Scan with Xray and Block on Fail'
```

---

## 🔐 進階：整合 Watch + Policy 進行建置守門

1. 登入 JFrog Platform → `Xray > Watches`
2. 建立 Watch 並選擇關聯的 Build 名稱或 Repository
3. 關聯一條 Policy（範例）：
   - CVSS ≥ 8.0 → Block
   - 授權為 GPLv2 → Block
4. 建置時自動觸發掃描，根據策略中止或通過

---

## 🧪 測試範例

- 專案引入 `log4j:1.2.17`
- 建置並觸發 `jf xr scan`
- 應顯示 CVE 並中止建置

---

## ✅ 完整 YAML Pipeline 範例

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

variables:
  JFROG_USER: $(JFROG_USER)
  JFROG_TOKEN: $(JFROG_TOKEN)

steps:
- script: |
    curl -fL https://getcli.jfrog.io | sh
    ./jf config add artifactory-server \
      --url https://<your-domain>.jfrog.io/artifactory \
      --user $JFROG_USER \
      --password $JFROG_TOKEN \
      --interactive=false
  displayName: 'Install & Configure JFrog CLI'

- script: |
    ./jf rt upload "build/libs/*.jar" libs-release-local/$(Build.BuildId)/ \
      --build-name=sample-app \
      --build-number=$(Build.BuildId)
  displayName: 'Upload Artifacts to Artifactory'

- script: |
    ./jf rt build-collect-env sample-app $(Build.BuildId)
    ./jf rt build-add-git sample-app $(Build.BuildId)
    ./jf rt build-publish sample-app $(Build.BuildId)
  displayName: 'Publish Build Info'

- script: |
    ./jf xr scan sample-app $(Build.BuildId) || exit 1
  displayName: 'Scan Build with Xray'
```

---

## 🧠 小結

| 階段 | 功能 |
|------|------|
| 安裝 CLI | 自動化構建與部署命令 |
| 上傳制品 | 上傳任意格式制品至 Artifactory |
| 發布 Build Info | 提供 Xray 掃描元資料 |
| Xray 掃描 | 分析漏洞與授權合規性 |
| 阻擋建置 | 當風險超出策略門檻時終止建置 |
