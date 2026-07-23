import os
import requests
from requests.auth import HTTPBasicAuth

def create_jira_ticket(rca_report: dict):
    if rca_report["severity"] not in ("CRITICAL", "HIGH"):
        return None

    url = f"{os.getenv('JIRA_BASE_URL')}/rest/api/3/issue"
    auth = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    payload = {
        "fields": {
            "project": {"key": os.getenv("JIRA_PROJECT_KEY")},
            "summary": f"[{rca_report['severity']}] {rca_report['root_cause'][:80]}",
            "description": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [
                    {"type": "text", "text": f"{rca_report['impact_summary']}\n\nFix: {rca_report['suggested_fix']}"}
                ]}],
            },
            "issuetype": {"name": "Bug"},
        }
    }
    try:
        r = requests.post(url, json=payload, auth=auth, headers={"Accept": "application/json"})
        return r.json().get("key")
    except Exception:
        return None