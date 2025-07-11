# 🐸 JFrog Xray Vulnerability Report Exporter

This Python script automates:

- Generation of JFrog Xray vulnerability reports
- Export of vulnerable artifact paths to Excel/CSV
- Copying or moving artifacts using the JFrog CLI (`jf`)
- Optional `--dry-run` for testing actions

## 🔧 Features

- Generate vulnerability reports filtered by severity
- Export artifact paths to `.csv` or `.xlsx`
- Copy (`cp`) or move (`mv`) files with `jf rt`
- Support for Maven-related suffixes: `.jar`, `.pom`, `.jar.asc`, `.pom.asc`

## 📦 Requirements

- Python 3.x
- `jf` CLI installed and configured
- Python packages: `pandas`, `openpyxl` (optional)

Install dependencies:

```bash
pip install pandas openpyxl
```

## 🛠️ CLI Usage

```bash
python3 xray_export.py \
  --url https://your.jfrog.url \
  --token YOUR_ACCESS_TOKEN \
  --source-repo my-maven-remote \
  --target-repo insecure-maven-local \
  --severity critical \
  --output vulnerable_paths.xlsx \
  --action cp \
  --dry-run
```

## 🎛️ Parameters

| Argument       | Description |
|----------------|-------------|
| `--url`        | Base URL of your JFrog Platform (e.g. `https://artifactory.com`) |
| `--token`      | Access token with Xray and Artifactory permissions |
| `--source-repo`| Remote repo to scan and copy from |
| `--target-repo`| Local repo to copy/move vulnerable artifacts to |
| `--severity`   | Minimum severity to filter (`low`, `medium`, `high`, `critical`) |
| `--output`     | File name for results (`.csv` or `.xlsx`) |
| `--action`     | `cp` (default) or `mv` to copy or move artifacts |
| `--dry-run`    | Print CLI commands without executing |

## 📤 Output

- Generates a report via Xray API
- Exports vulnerable paths to file
- Prints or executes `jf rt cp|mv` commands

## ✅ Example  Command

```bash
python3 xray_vuln_report_export.py \                
  --url https://demo.jfrogchina.com \
  --token $ARTIFACTORY_TOKEN \
  --target-repo alex-ignored-insecure-maven-repo \
  --output vulnerable_paths.xlsx --severity critical --source-repo alex-maven-remote
```

## 📎 Notes

- Uses `curl` for pagination export due to Xray API behavior
- `jf` CLI must be installed and configured in PATH
- `--dry-run` lets you preview what would be copied

