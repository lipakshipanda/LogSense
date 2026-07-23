from fastapi import APIRouter
from utils.store import get_anomalies, get_logs, add_rca, get_rcas
from services.rca_service import generate_rca
from services.jira_service import create_jira_ticket
from services.qdrant_service import upsert_incident, search_similar

router = APIRouter()

@router.post("/generate")
def trigger_rca():
    anomalies = get_anomalies(limit=20)
    logs = get_logs(limit=100)
    if not anomalies:
        return {"message": "No anomalies found. Generate logs first.", "report": None}

    report = generate_rca(anomalies, logs)
    if report:
        add_rca(report)
        upsert_incident(report["incident_id"], report["root_cause"], report)
        jira_key = create_jira_ticket(report)
        report["jira_ticket"] = jira_key

    return {"message": "RCA generated successfully", "report": report}

@router.get("/history")
def rca_history():
    reports = get_rcas()
    return {"reports": reports, "count": len(reports)}

@router.get("/similar")
def find_similar(query: str, top_k: int = 5):
    return {"results": search_similar(query, top_k)}