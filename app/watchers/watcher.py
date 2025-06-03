from typing import List,Dict,Any ,Optional
from kubernetes import client, config
from kubernetes.config import ConfigException
from kubernetes.stream import stream


def get_available_clusters():
    try:
        contexts, current = config.list_kube_config_contexts()
    except ConfigException:
        raise ValueError("No kubeconfig found or invalid config.")
    return {"available_clusters": [c["name"] for c in contexts], "current_context": current["name"]}


def watch_resource(cluster_name: str, resource_type: str, namespace: Optional[str] = None):
    config.load_kube_config(context=cluster_name)

    if resource_type == "pod":
        return _get_pods_with_metrics(namespace)
    elif resource_type == "node":
        return _get_nodes_with_metrics()
    elif resource_type == "deployment":
        apps = client.AppsV1Api()
        if namespace:
            return {"items": [d.to_dict() for d in apps.list_namespaced_deployment(namespace).items]}
        return {"items": [d.to_dict() for d in apps.list_deployment_for_all_namespaces().items]}
    elif resource_type == "replicaset":
        apps = client.AppsV1Api()
        if namespace:
            return {"items": [r.to_dict() for r in apps.list_namespaced_replica_set(namespace).items]}
        return {"items": [r.to_dict() for r in apps.list_replica_set_for_all_namespaces().items]}
    else:
        raise ValueError(f"Unsupported resource type: {resource_type}")


def _get_pods_with_metrics(namespace: Optional[str] = None):
    v1 = client.CoreV1Api()
    metrics = client.CustomObjectsApi()

    if namespace:
        pods = v1.list_namespaced_pod(namespace)
    else:
        pods = v1.list_pod_for_all_namespaces()

    try:
        metrics_response = metrics.list_cluster_custom_object(
            group="metrics.k8s.io", version="v1beta1", plural="pods"
        )
        metrics_map = {
            (item['metadata']['namespace'], item['metadata']['name']): item
            for item in metrics_response.get("items", [])
        }
    except Exception:
        metrics_map = {}

    result = []
    for pod in pods.items:
        pod_dict = pod.to_dict()
        key = (pod.metadata.namespace, pod.metadata.name)
        pod_metrics = metrics_map.get(key, {})
        pod_dict["metrics"] = pod_metrics
        result.append(pod_dict)

    return {"items": result}


def _get_nodes_with_metrics():
    v1 = client.CoreV1Api()
    metrics = client.CustomObjectsApi()

    nodes = v1.list_node()
    try:
        metrics_response = metrics.list_cluster_custom_object(
            group="metrics.k8s.io", version="v1beta1", plural="nodes"
        )
        metrics_map = {
            item['metadata']['name']: item for item in metrics_response.get("items", [])
        }
    except Exception:
        metrics_map = {}

    result = []
    for node in nodes.items:
        node_dict = node.to_dict()
        node_metrics = metrics_map.get(node.metadata.name, {})
        node_dict["metrics"] = node_metrics
        result.append(node_dict)

    return {"items": result}


def get_cluster_summary_metrics(cluster_name: str):
    config.load_kube_config(context=cluster_name)
    metrics = client.CustomObjectsApi()

    try:
        pod_metrics = metrics.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
        node_metrics = metrics.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
        return {
            "pods": pod_metrics.get("items", []),
            "nodes": node_metrics.get("items", [])
        }
    except Exception as e:
        raise ValueError(f"Failed to get cluster metrics: {str(e)}")






def load_context(cluster: str = None):
    """Load kube config and set context."""
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        raise RuntimeError("No Kubernetes contexts found.")
    config.load_kube_config(context=cluster)

def fetch_deployments(cluster: str) -> List[Dict[str, Any]]:
    load_context(cluster)
    apps_v1 = client.AppsV1Api()
    deployments = apps_v1.list_deployment_for_all_namespaces(watch=False)
    return [{
        "name": d.metadata.name,
        "namespace": d.metadata.namespace,
        "replicas": d.spec.replicas,
        "available_replicas": d.status.available_replicas
    } for d in deployments.items]

def fetch_replicasets(cluster: str) -> List[Dict[str, Any]]:
    load_context(cluster)
    apps_v1 = client.AppsV1Api()
    replicasets = apps_v1.list_replica_set_for_all_namespaces(watch=False)
    return [{
        "name": r.metadata.name,
        "namespace": r.metadata.namespace,
        "replicas": r.spec.replicas,
        "ready_replicas": r.status.ready_replicas
    } for r in replicasets.items]












 
