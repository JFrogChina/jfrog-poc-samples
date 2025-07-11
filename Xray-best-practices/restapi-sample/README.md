curl -H "Authorization: Bearer $ARTIFACTORY_TOKEN"  -X POST "https://$DEMO_ARTIFACTORY/xray/api/v1/configuration/export" \
  -H "Content-Type: application/json" \
  -d @export.json
