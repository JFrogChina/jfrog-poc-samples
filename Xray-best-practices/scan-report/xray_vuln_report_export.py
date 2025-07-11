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

parser = argparse.ArgumentParser(description="Generate and export JFrog Xray vulnerability report")
parser.add_argument('--url', required=True, help='JFrog base URL')
parser.add_argument('--token', required=True, help='Access token')
parser.add_argument('--source-repo', required=True, help='Source repository to copy files from')
parser.add_argument('--target-repo', required=True, help='Target repository to copy files into')
parser.add_argument('--severity', default='low', choices=['low', 'medium', 'high', 'critical'],
                    help='Minimum severity to include (default: low)')
parser.add_argument('--output', default='vulnerable_paths.xlsx', help='Output file name (.xlsx or .csv)')
parser.add_argument('--action', default='cp', choices=['cp', 'mv'], help='jfrog CLI action (cp or mv), default cp')
parser.add_argument('--dry-run', action='store_true', help='Only print actions without executing jfrog CLI commands')
args = parser.parse_args()

BASE_URL = args.url.rstrip('/')
API_CREATE = f"{BASE_URL}/xray/api/v1/reports/vulnerabilities"
HEADERS = {
    "Authorization": f"Bearer {args.token}",
    "Content-Type": "application/json"
}
SEVERITY_THRESHOLD = severity_order[args.severity.lower()]

report_name = f"xray-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
report_payload = {
    "name": report_name,
    "resources": {
        "repositories": [
            {"name": args.source_repo}
        ]
    },
    "filters": {
        "severities": [severity.title() for severity in severity_order if severity_order[severity] >= SEVERITY_THRESHOLD]
    }
}

MAX_RETRIES = 5
RETRY_INTERVAL = 10

print(f"🛠️ Creating Xray report: {report_name}")
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
print(f"curl -k -X POST '{BASE_URL}/xray/api/v1/reports/vulnerabilities/{report_id}?page_num=1&num_of_rows=100' ")
print("  -H 'Authorization: Bearer $ARTIFACTORY_TOKEN' ")
print("  -H 'Content-Type: application/json'\n")

MAX_WAIT_SECONDS = 300
WAIT_INTERVAL = 5
elapsed = 0

print("⏳ Waiting for report to complete...")
while elapsed < MAX_WAIT_SECONDS:
    try:
        check_url = f"{BASE_URL}/xray/api/v1/reports/vulnerabilities/{report_id}?page_num=1&num_of_rows=100"
        result = subprocess.run([
            "curl", "-sk", "-X", "POST", check_url,
            "-H", f"Authorization: Bearer {args.token}",
            "-H", "Content-Type: application/json"
        ], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        print(f"🧪 Report status check: {output.strip()}")
        data = json.loads(output)
        if data.get("total_rows", 0) > 0:
            print("✅ Report is ready.")
            break
        elif data.get("rows") == []:
            print("⌛ Report not yet populated, retrying...")
        else:
            print(f"❌ Unexpected response: {output.strip()}")
    except Exception as e:
        print(f"⚠️ Error while polling report status: {e}")
    time.sleep(WAIT_INTERVAL)
    elapsed += WAIT_INTERVAL
else:
    print("❌ Timeout waiting for report to become available.")
    exit(1)

print("📤 Exporting report data...")
rows = []
page = 1

while True:
    export_url = f"{BASE_URL}/xray/api/v1/reports/vulnerabilities/{report_id}?page_num={page}&num_of_rows=100"
    print(f"🔍 Attempting export: curl -k -X POST '{export_url}'")

    try:
        result = subprocess.run([
            "curl", "-sk", "-X", "POST", export_url,
            "-H", f"Authorization: Bearer {args.token}",
            "-H", "Content-Type: application/json"
        ], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        data = json.loads(output)
        if not data.get("rows"):
            print("✅ No more data to export.")
            break

        for entry in data["rows"]:
            path = entry.get("path")
            severity_raw = entry.get("severity", "low")
            severity = severity_raw.lower()
            sev_rank = severity_order.get(severity)
            if sev_rank is None:
                print(f"⚠️ Unknown severity: {severity_raw} for path {path}")
                continue
            if path and sev_rank >= SEVERITY_THRESHOLD:
                rows.append((path, severity))
        page += 1
    except Exception as e:
        print(f"⚠️ Error during export: {e}")
        time.sleep(WAIT_INTERVAL)
        continue

if not rows:
    print(f"⚠️ No vulnerable paths found with severity >= {args.severity}")
    exit(0)

print(f"💾 Exporting {len(rows)} paths to {args.output}")
df = pd.DataFrame(rows, columns=["path", "severity"])
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
related_suffixes = [".jar", ".pom", ".jar.asc", ".pom.asc"]

for path, severity in rows:
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

    relative_dir = str(full_path.parent)
    basename = filename.rsplit(".", 1)[0]
    if not basename.strip():
        continue

    for suffix in related_suffixes:
        full_name = f"{basename}{suffix}"
        source_path = f"{args.source_repo}-cache/{relative_dir}/{full_name}"
        target_path = f"{args.target_repo}/{relative_dir}/{full_name}"
        cmd = [jfrog_cli, "rt", args.action, source_path, target_path]
        print(f"🔁 ({severity}) {' '.join(cmd)}")
        if not args.dry_run:
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to {args.action}: {source_path}")

print("✅ Xray vulnerability report export completed!")
