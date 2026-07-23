from firebase_config import db
from google.cloud.firestore_v1 import FieldFilter

LOGS_COL = db.collection("logs")
ANOMALIES_COL = db.collection("anomalies")
RCA_COL = db.collection("rca_reports")

def add_logs(logs):
    batch = db.batch()
    for log in logs:
        ref = LOGS_COL.document(log["id"])
        batch.set(ref, log)
    batch.commit()

def add_anomalies(anomalies):
    batch = db.batch()
    for a in anomalies:
        ref = ANOMALIES_COL.document(a["log_id"])
        batch.set(ref, a)
    batch.commit()

def add_rca(report):
    RCA_COL.document(report["incident_id"]).set(report)

def get_logs(limit=100):
    docs = LOGS_COL.order_by("timestamp", direction="DESCENDING").limit(limit).stream()
    return [d.to_dict() for d in docs]

def get_anomalies(limit=50):
    docs = ANOMALIES_COL.order_by("timestamp", direction="DESCENDING").limit(limit).stream()
    return [d.to_dict() for d in docs]

def get_rcas(limit=10):
    docs = RCA_COL.order_by("generated_at", direction="DESCENDING").limit(limit).stream()
    return [d.to_dict() for d in docs]

def get_stats():
    total_logs = len(list(LOGS_COL.limit(500).stream()))
    anomalies = [d.to_dict() for d in ANOMALIES_COL.limit(200).stream()]
    total_anomalies = len(anomalies)
    anomaly_rate = round((total_anomalies / total_logs * 100), 2) if total_logs else 0
    services = set(a["service"] for a in anomalies)
    critical_count = sum(1 for a in anomalies if a.get("anomaly_type") == "cascade_failure")
    return {
        "total_logs": total_logs,
        "total_anomalies": total_anomalies,
        "anomaly_rate": anomaly_rate,
        "services_affected": len(services),
        "critical_count": critical_count,
    }