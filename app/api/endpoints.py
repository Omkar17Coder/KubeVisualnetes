from fastapi import APIRouter, HTTPException, Query, Path
from app.watchers.watcher import (
    get_available_clusters,
    watch_resource,
    get_cluster_summary_metrics,
    fetch_deployments,
    fetch_replicasets  
)

router = APIRouter()

@router.get("/clusters")
def list_clusters():
    return get_available_clusters()

@router.get("/clusters/{cluster}/resources/{resource_type}")
def get_resource(cluster: str, resource_type: str, namespace: str = Query(None)):
    try:
        return watch_resource(cluster, resource_type, namespace)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/clusters/{cluster}/metrics/summary")
def get_cluster_metrics(cluster: str):
    try:
        return get_cluster_summary_metrics(cluster)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/clusters/{cluster}/deployments")
def get_deployments(cluster: str = Path(...)):
    return {"deployments": fetch_deployments(cluster)}

@router.get("/clusters/{cluster}/replicasets")
def get_replicasets(cluster: str = Path(...)):
    return {"replicasets": fetch_replicasets(cluster)}

