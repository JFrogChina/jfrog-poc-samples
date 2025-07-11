curl -H "Authorization: Bearer $ARTIFACTORY_TOKEN"  -X POST "https://$DEMO_ARTIFACTORY/xray/api/v1/configuration/export" \
  -H "Content-Type: application/json" \
  -d @export.json

  python3 delete_xray_reports.py \                        
  --url https://demo.jfrogchina.com \
  --token $ARTIFACTORY_TOKEN \
  --start-id 100 \
  --end-id 200
