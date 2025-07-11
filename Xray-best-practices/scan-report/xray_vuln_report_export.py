import requests
import argparse
import pandas as pd
import urllib3
import subprocess
import time
import json
from shutil import which
from pathlib import Path
from datetime import datetime
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

severity_order = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

parser = argparse.ArgumentParser(description="Generate and export JFrog Xray report")
parser.add_argument('--url', required=True, help='JFrog base URL')
parser.add_argument('--token', required=True, help='Access token')
parser.add_argument('--source-repo', required=True, help='Source repository to copy files from')
parser.add_argument('--target-repo', required=True, help='Target repository to copy files into')
parser.add_argument('--severity', default='critical', choices=['low', 'medium', 'high', 'critical'],
                    help='Minimum severity to include (default: critical, for vulnerability report only)')
parser.add_argument('--report-type', default='vulnerability', choices=['vulnerability', 'license'],
                    help='Report type: vulnerability or license')
parser.add_argument('--license-names', nargs='*', help='Required license name filters for license report')
parser.add_argument('--output', default='xray_report.xlsx', help='Output file name (.xlsx or .csv)')
parser.add_argument('--action', default='cp', choices=['cp', 'mv'], help='jfrog CLI action (cp or mv), default cp')
parser.add_argument('--dry-run', action='store_true', help='Only print actions without executing jfrog CLI commands')
args = parser.parse_args()

if args.report_type == 'license' and not args.license_names:
    print("❌ --license-names is required when --report-type is 'license'")
    exit(1)

BASE_URL = args.url.rstrip('/')
REPORT_API_PATH = {
    "vulnerability": "vulnerabilities",
    "license": "licenses"
}[args.report_type]
API_CREATE = f"{BASE_URL}/xray/api/v1/reports/{REPORT_API_PATH}"
HEADERS = {
    "Authorization": f"Bearer {args.token}",
    "Content-Type": "application/json"
}

report_name = f"xray-report-{args.source_repo}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
report_payload = {
    "name": report_name,
    "resources": {
        "repositories": [
            {"name": args.source_repo}
        ]
    }
}

if args.report_type == "vulnerability":
    SEVERITY_THRESHOLD = severity_order[args.severity.lower()]
    report_payload["filters"] = {
        "severities": [sev.title() for sev in severity_order if severity_order[sev] >= SEVERITY_THRESHOLD]
    }
elif args.report_type == "license":
    report_payload["filters"] = {
        "license_names": args.license_names
    }

MAX_RETRIES = 5
RETRY_INTERVAL = 10

print(f"🛠️ Creating Xray {args.report_type} report: {report_name}")
for attempt in range(1, MAX_RETRIES + 1):
    resp = requests.post(API_CREATE, headers=HEADERS, json=report_payload, verify=False)
    if resp.status_code == 429:
        print(f"⚠️ 429 Too Many Requests - retrying in {RETRY_INTERVAL}s (attempt {attempt}/{MAX_RETRIES})...")
        time.sleep(RETRY_INTERVAL)
    else:
        break

resp.raise_for_status()
report_id = resp.json()["report_id"]
print(f"✅ Report created. ID = {report_id}")

print("\n--- 获取报告状态命令 ---")
print(f"curl -k -X POST '{BASE_URL}/xray/api/v1/reports/{REPORT_API_PATH}/{report_id}?page_num=1&num_of_rows=100' ")
print(f"  -H \"Authorization: Bearer $ARTIFACTORY_TOKEN\" ")
print("  -H 'Content-Type: application/json'\n")

print("📤 Exporting report data...")
rows = []
page = 1

while True:
    export_url = f"{BASE_URL}/xray/api/v1/reports/{REPORT_API_PATH}/{report_id}?page_num={page}&num_of_rows=100"
    print(f"🔍 Attempting export: curl -k -X POST '{export_url}'")

    try:
        result = subprocess.run([
            "curl", "-sk", "-X", "POST", export_url,
            "-H", f"Authorization: Bearer {args.token}",
            "-H", "Content-Type: application/json"
        ], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        data = json.loads(output)

        print("📦 data[\"rows\"]:")
        print(json.dumps(data.get("rows", []), indent=2))

        if not data.get("rows"):
            print("✅ No more data to export.")
            break

        for entry in data["rows"]:
            if args.report_type == "license" and entry.get("package_type") != "maven":
                continue

            path = entry.get("path")
            if args.report_type == "vulnerability":
                severity_raw = entry.get("severity", "low")
                severity = severity_raw.lower()
                sev_rank = severity_order.get(severity)
                if sev_rank is None or sev_rank < SEVERITY_THRESHOLD:
                    continue
                rows.append((path, severity))
            else:
                license_name = entry.get("license") or entry.get("license_key") or ""
                rows.append((path, license_name))
        page += 1
    except Exception as e:
        print(f"⚠️ Error during export: {e}")
        time.sleep(5)
        continue

if not rows:
    print("⚠️ No matching data found in report.")
    exit(0)

print(f"💾 Exporting {len(rows)} paths to {args.output}")
df = pd.DataFrame(rows, columns=["path", "severity_or_license"])
if args.output.endswith(".csv"):
    df.to_csv(args.output, index=False)
else:
    import openpyxl
    df.to_excel(args.output, index=False, engine="openpyxl")

jfrog_cli = which("jf")
if not jfrog_cli:
    print("❌ 'jf' CLI not found. Please install it and ensure it is in your PATH.")
    exit(1)

print(f"📁 Copying related files from '{args.source_repo}' to '{args.target_repo}' ...")
visited = set()

for path, info in rows:
    print(f"➡️ Processing: path={path}, info={info}")
    parts = path.split("/", 1)
    if len(parts) != 2:
        print(f"❌ Invalid path format: {path}")
        continue
    _repo_from_report, relative_path = parts

    full_path = Path(relative_path)
    filename = full_path.name
    if not filename or "." not in filename:
        print(f"⚠️ Skipping invalid filename: {filename}")
        continue

    if filename.endswith("-sources.jar") or filename.endswith("-javadoc.jar"):
        print(f"⚠️ Skipping source/doc jar: {filename}")
        continue

    source_path = f"{args.source_repo}-cache/{relative_path}"
    target_path = f"{args.target_repo}/{filename}"
    key = (source_path, target_path)
    if key in visited:
        continue
    visited.add(key)
    cmd = [jfrog_cli, "rt", args.action, source_path, target_path]
    print(f"🔁 ({info}) {' '.join(cmd)}")
    if not args.dry_run:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to {args.action}: {source_path}")

    # 追加 POM 拷贝逻辑
    if args.report_type == "license" and filename.endswith(".jar"):
        pom_name = filename.replace(".jar", ".pom")
        pom_source_path = f"{args.source_repo}-cache/{full_path.parent}/{pom_name}"
        pom_target_path = f"{args.target_repo}/{pom_name}"
        pom_key = (pom_source_path, pom_target_path)
        if pom_key not in visited:
            visited.add(pom_key)
            pom_cmd = [jfrog_cli, "rt", args.action, str(pom_source_path), str(pom_target_path)]
            print(f"📎 Also copying POM: {' '.join(pom_cmd)}")
            if not args.dry_run:
                try:
                    subprocess.run(pom_cmd, check=True)
                except subprocess.CalledProcessError:
                    print(f"⚠️ Failed to {args.action}: {pom_source_path}")

print(f"✅ Xray {args.report_type} report export completed!")
