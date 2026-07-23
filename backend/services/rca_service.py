import os
import uuid
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_rca(anomalies, logs):
    if not anomalies:
        return None

    affected_services = list(set(a["service"] for a in anomalies))
    anomaly_types = list(set(a["anomaly_type"] for a in anomalies))

    summary_lines = [
        f"- Service: {a['service']} | Type: {a['anomaly_type']} | Score: {a['anomaly_score']} | Time: {a['timestamp']}"
        for a in anomalies[:10]
    ]
    anomaly_text = "\n".join(summary_lines)

    prompt = f"""You are a senior Site Reliability Engineer. Analyze the following anomalies and provide root-cause analysis.

Anomalies:
{anomaly_text}

Affected Services: {', '.join(affected_services)}
Anomaly Types: {', '.join(anomaly_types)}

Respond ONLY in this JSON format:
{{
  "root_cause": "one clear sentence",
  "impact_summary": "one sentence on impact",
  "suggested_fix": "two to three concrete steps",
  "severity": "LOW or MEDIUM or HIGH or CRITICAL"
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content.strip())
    except Exception:
        data = _rule_based_rca(anomalies, anomaly_types)

    return {
        "incident_id": str(uuid.uuid4())[:8],
        "affected_services": affected_services,
        "root_cause": data.get("root_cause", "Unknown"),
        "impact_summary": data.get("impact_summary", "Multiple services affected"),
        "suggested_fix": data.get("suggested_fix", "Investigate service logs"),
        "severity": data.get("severity", "MEDIUM"),
        "generated_at": datetime.utcnow().isoformat(),
    }

def _rule_based_rca(anomalies, anomaly_types):
    if "cascade_failure" in anomaly_types:
        return {
            "root_cause": "Cascade failure — one service failure is propagating to downstream services.",
            "impact_summary": f"{len(anomalies)} anomalies across multiple services.",
            "suggested_fix": "1. Isolate the failing service. 2. Check DB connections. 3. Roll back recent deployments.",
            "severity": "CRITICAL",
        }
    if "latency_spike" in anomaly_types:
        return {
            "root_cause": "Abnormal response latency — possible DB bottleneck or network congestion.",
            "impact_summary": "Services are responding slowly, degrading user experience.",
            "suggested_fix": "1. Check DB query performance. 2. Review recent config changes. 3. Scale up if needed.",
            "severity": "HIGH",
        }
    return {
        "root_cause": "Elevated error rate detected across services.",
        "impact_summary": "Error burst affecting service reliability.",
        "suggested_fix": "1. Review error logs. 2. Check third-party dependencies. 3. Enable circuit breaker.",
        "severity": "MEDIUM",
    }