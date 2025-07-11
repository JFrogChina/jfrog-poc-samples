# 🛡️ JFrog Xray Report Export Tool

This Python tool automates the process of generating, polling, exporting, and processing JFrog Xray **vulnerability** or **license** reports.\
It extracts the affected artifact paths and copies them (and optional `.pom` files) from a remote-cache repository to a target repository using the `jf` CLI.

---

## 📋 Features

- Supports both `vulnerability` and `license` reports
- Uses `curl` for exporting report data to ensure accurate results
- Filters vulnerabilities by severity and licenses by name
- Automatically skips `-sources.jar` and `-javadoc.jar` files
- Copies `.pom` files along with `.jar` (for license reports)
- Supports dry-run and copy/move options

---

## 🛠️ Requirements

- Python 3.6+
- `jf` CLI installed and available in `PATH`
- A valid access token for your JFrog instance

---

## 🚀 Usage

```bash
python3 xray_vuln_report_export.py \
  --url https://your.jfrog.instance \
  --token YOUR_ACCESS_TOKEN \
  --source-repo fan-maven-remote \
  --target-repo insecure-maven-local \
  --report-type vulnerability \
  --severity critical \
  --output report_vulnerabilities.xlsx
```

```bash
python3 xray_vuln_report_export.py \
  --url https://your.jfrog.instance \
  --token YOUR_ACCESS_TOKEN \
  --source-repo fan-maven-remote \
  --target-repo insecure-maven-local \
  --report-type license \
  --license-names MIT Apache-2.0 \
  --output report_licenses.xlsx
```

---

## 🧾 Command Arguments

| Argument          | Description                                                                |
| ----------------- | -------------------------------------------------------------------------- |
| `--url`           | Base URL of JFrog instance (e.g., `https://demo.jfrogchina.com`)           |
| `--token`         | Access token for authentication                                            |
| `--source-repo`   | Base name of source repository (e.g., `fan-maven-remote`)                  |
| `--target-repo`   | Target local repository to copy files into                                 |
| `--report-type`   | Type of report to generate (`vulnerability` or `license`)                  |
| `--severity`      | Minimum severity for vulnerabilities (`low`, `medium`, `high`, `critical`) |
| `--license-names` | List of license names (for license reports only)                           |
| `--output`        | Output file name (`.xlsx` or `.csv`)                                       |
| `--action`        | `cp` to copy (default), or `mv` to move                                    |
| `--dry-run`       | Only print actions without executing jfrog CLI                             |

---

## 📦 Export Logic

- Calls Xray API to create a report (`POST /xray/api/v1/reports/...`)
- Waits until the report is ready (polls export endpoint with `curl`)
- Retrieves artifact paths page by page
- Skips invalid paths and documentation/source files
- Uses `jf rt cp` or `jf rt mv` to transfer `.jar` and `.pom` files

---

## 📁 Example Output

```bash
✅ Report created. ID = 357
⏳ Waiting for report to complete...
📄 Exporting report data...
➡️ Processing: path=fan-maven-remote/org/example/lib/1.0/lib-1.0.jar, info=MIT
🔁 (MIT) jf rt cp fan-maven-remote-cache/org/example/lib/1.0/lib-1.0.jar insecure-maven-local/lib-1.0.jar
📎 Also copying POM: jf rt cp fan-maven-remote-cache/org/example/lib/1.0/lib-1.0.pom insecure-maven-local/lib-1.0.pom
```

---

## 📌 Notes

- License reports require `--license-names` to be provided.
- Only `maven` packages are processed for license reports.
- Report polling ensures the report is fully generated before export.
- Results are saved to `.csv` or `.xlsx`, and printed in terminal for verification.

