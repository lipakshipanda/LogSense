from fastapi import APIRouter, Query
from utils.store import get_anomalies

router = APIRouter()

@router.get("/")
def list_anomalies(limit: int = Query(50, ge=1, le=200)):
    anomalies = get_anomalies(limit=limit)
    return {"anomalies": anomalies, "count": len(anomalies)}

@router.get("/by-service/{service_name}")
def anomalies_by_service(service_name: str):
    all_anomalies = get_anomalies(limit=200)
    filtered = [a for a in all_anomalies if a["service"] == service_name]
    return {"service": service_name, "anomalies": filtered, "count": len(filtered)}