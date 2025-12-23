helm upgrade --install jfrog-platform jfrog/jfrog-platform \
  -n jfrog \
  --create-namespace \
  -f values.yaml


kubectl port-forward svc/jfrog-platform-artifactory-nginx 8080:80 -n jfrog-platform