from fastapi import APIRouter, Query
from utils.log_generator import generate_batch
from utils.store import add_logs, get_logs, add_anomalies
from services.anomaly_detector import detect_anomalies

router = APIRouter()

@router.get("/generate")
def generate_logs(
    n: int = Query(50, ge=10, le=200),
    anomaly_ratio: float = Query(0.1, ge=0, le=1)
):
    logs      = generate_batch(n=n, anomaly_ratio=anomaly_ratio)
    anomalies = detect_anomalies(logs)
    add_logs(logs)
    add_anomalies(anomalies)
    return {
        "generated":       len(logs),
        "anomalies_found": len(anomalies),
        "logs":            logs[:20],
    }

@router.get("/")
def list_logs(limit: int = Query(100, ge=1, le=500)):
    return {"logs": get_logs(limit=limit), "count": limit}