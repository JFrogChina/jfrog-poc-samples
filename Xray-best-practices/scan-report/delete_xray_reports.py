import argparse
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 解析参数
parser = argparse.ArgumentParser(description="Batch delete JFrog Xray reports by ID range")
parser.add_argument('--url', required=True, help='JFrog base URL (e.g., https://your.jfrog.io)')
parser.add_argument('--token', required=True, help='Access token')
parser.add_argument('--start-id', type=int, required=True, help='Start report ID')
parser.add_argument('--end-id', type=int, required=True, help='End report ID')
args = parser.parse_args()

BASE_URL = args.url.rstrip('/')
HEADERS = {
    "Authorization": f"Bearer {args.token}"
}

print(f"🚀 Deleting reports from ID {args.start_id} to {args.end_id}")

for report_id in range(args.start_id, args.end_id + 1):
    delete_url = f"{BASE_URL}/xray/api/v1/reports/{report_id}"
    print(f"🗑️  Deleting report ID {report_id} ... ", end='')

    try:
        resp = requests.delete(delete_url, headers=HEADERS, verify=False)
        if resp.status_code == 204:
            print("✅ Deleted")
        elif resp.status_code == 404:
            print("⚠️ Not Found")
        else:
            print(f"❌ Failed (HTTP {resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
