# KubeVisualnetes


1. To run uvicorn app.main:app --reload

  ✅ Get All Pods with Metrics

Here kind-hello-service is sameple cluster running replace it with the cluster you need metrics for
curl "http://localhost:8000/clusters/kind-hello-service/resources/pod"

✅ Get All Nodes with Metrics

curl "http://localhost:8000/clusters/kind-hello-service/resources/node"

✅ Get Cluster Summary Metrics

curl "http://localhost:8000/clusters/kind-hello-service/metrics/summary"

✅ Get Deployment Set information

curl "http://localhost:8000/clusters/kind-hello-service/deployments"

✅ Get  Replicate set information

curl "http://localhost:8000/clusters/kind-hello-service/replicatesets"
