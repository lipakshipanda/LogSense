from fastapi import APIRouter
from utils.store import get_stats, get_anomalies

router = APIRouter()

@router.get("/")
def dashboard_stats():
    return get_stats()

@router.get("/anomaly-types")
def anomaly_type_breakdown():
    anomalies = get_anomalies(limit=200)
    counts = {}
    for a in anomalies:
        t = a.get("anomaly_type", "unknown")
        counts[t] = counts.get(t, 0) + 1
    return {"breakdown": counts}

@router.get("/service-health")
def service_health():
    anomalies = get_anomalies(limit=200)
    health = {}
    for a in anomalies:
        s = a["service"]
        health[s] = health.get(s, 0) + 1
    return {"service_health": health}