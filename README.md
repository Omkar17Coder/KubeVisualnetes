# KubeVisualnetes


1. To run uvicorn app.main:app --reload

  ✅ Get All Pods with Metrics

curl "http://localhost:8000/clusters/kind-hello-service/resources/pod"

✅ Get All Nodes with Metrics

curl "http://localhost:8000/clusters/kind-hello-service/resources/node"

✅ Get Cluster Summary Metrics

curl "http://localhost:8000/clusters/kind-hello-service/metrics/summary"
