
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
    print(f"📤 License report filter payload: {json.dumps(report_payload['filters'], indent=2)}")

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

# 轮询GET报告状态，直到status为completed
import time

status_url = f"{BASE_URL}/xray/api/v1/reports/vulnerabilities/{report_id}"
print("⏳ Waiting for report to complete...")

while True:
    export_url = f"{BASE_URL}/xray/api/v1/reports/{REPORT_API_PATH}/{report_id}?page_num=1&num_of_rows=1"
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
            print("Report is not ready. Retry in 5 seconds")
            time.sleep(5)
        else:
            print("✅ Report is ready for export.")
            break
    except Exception as e:
        print(f"⚠️ Error during export: {e}")
        time.sleep(5)
        continue
        
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
            # 统一收集dict，保留所有关键字段
            if args.report_type == "license" and entry.get("package_type") != "maven":
                continue
            # 只收集需要的字段
            row = {
                "path": entry.get("path"),
                "package_type": entry.get("package_type", ""),
            }
            if args.report_type == "vulnerability":
                severity_raw = entry.get("severity", "low")
                severity = severity_raw.lower()
                sev_rank = severity_order.get(severity)
                if sev_rank is None or sev_rank < SEVERITY_THRESHOLD:
                    continue
                row["severity"] = severity
            else:
                license_name = entry.get("license") or entry.get("license_key") or ""
                row["license"] = license_name
            rows.append(row)
        page += 1
    except Exception as e:
        print(f"⚠️ Error during export: {e}")
        time.sleep(5)
        continue

if not rows:
    print("⚠️ No matching data found in report.")
    exit(0)

print(f"💾 Exporting {len(rows)} paths to {args.output}")
df = pd.DataFrame(rows)
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

def copy_artifact(source_repo, target_repo, rel_path, dry_run=False):
    src = f"{source_repo}-cache/{rel_path}"
    tgt = f"{target_repo}/"  # 只写仓库名或目标目录
    cmd = [jfrog_cli, "rt", "cp", src, tgt]
    print(f"🔁 jf rt cp {src} {tgt}")
    if not dry_run:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to copy: {src}")

for entry in rows:
    path = entry.get("path")
    package_type = entry.get("package_type", "")
    if not path or not package_type:
        continue
    # Remove leading repo name
    parts = path.split("/", 1)
    if len(parts) != 2:
        print(f"❌ Invalid path format: {path}")
        continue
    rel_path = parts[1]
    # maven
    if package_type == "maven":
        if rel_path.endswith(".jar") or rel_path.endswith(".pom"):
            copy_artifact(args.source_repo, args.target_repo, rel_path, getattr(args, 'dry_run', False))
    # npm
    elif package_type == "npm":
        if rel_path.endswith(".tgz"):
            # copy .tgz
            copy_artifact(args.source_repo, args.target_repo, rel_path, getattr(args, 'dry_run', False))
            # copy package.json in same dir
            pkg_dir = os.path.dirname(rel_path)
            pkg_json_path = f"{pkg_dir}/package.json"
            copy_artifact(args.source_repo, args.target_repo, pkg_json_path, getattr(args, 'dry_run', False))
    # nuget
    elif package_type == "nuget":
        if rel_path.endswith(".nupkg"):
            # copy .nupkg
            copy_artifact(args.source_repo, args.target_repo, rel_path, getattr(args, 'dry_run', False))
            # copy .nuspec in same dir, same base name
            base = os.path.splitext(os.path.basename(rel_path))[0]
            nuspec_path = f"{os.path.dirname(rel_path)}/{base}.nuspec"
            copy_artifact(args.source_repo, args.target_repo, nuspec_path, getattr(args, 'dry_run', False))

print(f"✅ Xray {args.report_type} report export completed!")
