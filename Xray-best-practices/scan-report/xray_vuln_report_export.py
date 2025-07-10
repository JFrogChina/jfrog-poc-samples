import requests
import argparse
import pandas as pd
import urllib3
import subprocess
import tempfile
from shutil import which

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CLI arguments
parser = argparse.ArgumentParser(description="Export vulnerable artifact paths from JFrog Xray report")
parser.add_argument('--url', required=True, help='JFrog base URL, e.g., https://demo.jfrogchina.com')
parser.add_argument('--report-id', required=True, help='Xray report ID to export')
parser.add_argument('--token', required=True, help='Access token')
parser.add_argument('--target-repo', required=True, help='Target repo to move artifacts into')
parser.add_argument('--output', default='vulnerable_paths.xlsx', help='Output file name (should end in .xlsx or .csv)')
args = parser.parse_args()

BASE_URL = args.url.rstrip('/')
API = f"{BASE_URL}/xray/api/v1/reports/vulnerabilities/{args.report_id}"
HEADERS = {
    "Authorization": f"Bearer {args.token}"
}

rows = []
page = 1

print(f"📄 Fetching page {page} ...")
while True:
    params = {"page_num": page, "num_of_rows": 100, "direction": "asc"}
    response = requests.post(API, headers=HEADERS, params=params, verify=False)
    response.raise_for_status()
    data = response.json()
    if not data.get("rows"):
        break

    for entry in data["rows"]:
        path = entry.get("path")
        if path:
            rows.append(path)

    page += 1
    print(f"📄 Fetching page {page} ...")

if not rows:
    print("⚠️ No vulnerable paths found.")
    exit(0)

# Exporting
EXPORT_FILE = args.output
print(f"💾 Exporting {len(rows)} vulnerable paths to {EXPORT_FILE} ...")
df = pd.DataFrame(rows)

if EXPORT_FILE.endswith('.csv'):
    df.to_csv(EXPORT_FILE, index=False, header=False)
else:
    try:
        import openpyxl
        df.to_excel(EXPORT_FILE, index=False, header=False, engine='openpyxl')
    except ImportError:
        print("❌ 'openpyxl' not installed. Install it using: pip install openpyxl")
        exit(1)

print("✅ Export complete.")

# Cache remote repo types
print("🔍 Fetching repository types for remote detection...")
repo_types = {}
try:
    repos_resp = requests.get(f"{BASE_URL}/artifactory/api/repositories", headers=HEADERS, verify=False)
    repos_resp.raise_for_status()
    for repo_info in repos_resp.json():
        repo_name = repo_info.get("key")
        repo_type = repo_info.get("rclass")  # local, remote, virtual
        if repo_name and repo_type:
            repo_types[repo_name] = repo_type
except Exception as e:
    print(f"⚠️ Failed to fetch repository types: {e}")

# Move files to target repo
jfrog_cli = which("jf")
if not jfrog_cli:
    print("❌ 'jfrog' CLI not found in PATH. Please install it and make sure it's accessible.")
    exit(1)

print(f"🚚 Moving vulnerable artifacts to repo: {args.target_repo}")
for path in rows:
    parts = path.split('/', 1)
    if len(parts) != 2:
        print(f"❌ Invalid path format: {path}")
        continue
    repo, relative_path = parts

    # Always append -cache to source repo name
    repo_cache = f"{repo}-cache"
    full_source_path = f"{repo_cache}/{relative_path}"
    target_path = f"{args.target_repo}/{relative_path}"

    cmd = [jfrog_cli, "rt", "mv", full_source_path, target_path]
    print(f"🔁 {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Failed to move: {full_source_path}")
