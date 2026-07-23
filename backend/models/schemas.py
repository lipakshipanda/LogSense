from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LogEntry(BaseModel):
    id: str
    timestamp: datetime
    service: str
    level: str
    message: str
    latency_ms: float
    status_code: int

class AnomalyResult(BaseModel):
    log_id: str
    service: str
    timestamp: datetime
    anomaly_score: float
    is_anomaly: bool
    anomaly_type: Optional[str]

class RCAReport(BaseModel):
    incident_id: str
    affected_services: List[str]
    root_cause: str
    impact_summary: str
    suggested_fix: str
    severity: str
    generated_at: datetime

class DashboardStats(BaseModel):
    total_logs: int
    total_anomalies: int
    anomaly_rate: float
    services_affected: int
    critical_count: int