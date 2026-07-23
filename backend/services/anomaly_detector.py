import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

_model      = IsolationForest(contamination=0.1, random_state=42, n_estimators=100)
_le_service = LabelEncoder()
_le_level   = LabelEncoder()
_is_trained = False

SERVICES = ["auth-service", "payment-service", "order-service", "inventory-service", "notification-service"]
LEVELS   = ["INFO", "WARN", "ERROR", "CRITICAL"]

_le_service.fit(SERVICES)
_le_level.fit(LEVELS)

def _extract_features(logs):
    rows = []
    for log in logs:
        svc = _le_service.transform([log["service"]])[0] if log["service"] in SERVICES else 0
        lvl = _le_level.transform([log["level"]])[0]     if log["level"]   in LEVELS   else 0
        rows.append([svc, lvl, log.get("latency_ms", 0), log.get("status_code", 200)])
    return np.array(rows)

def train_model(logs):
    global _model, _is_trained
    if len(logs) < 10:
        return
    X = _extract_features(logs)
    _model.fit(X)
    _is_trained = True

def _classify_anomaly(log, score):
    if log.get("latency_ms", 0) > 1500:
        return "latency_spike"
    if log.get("level") in ["ERROR", "CRITICAL"]:
        return "error_burst"
    if score < -0.3:
        return "cascade_failure"
    return "unknown_anomaly"

def detect_anomalies(logs):
    global _is_trained
    if not _is_trained:
        train_model(logs)
    if not logs:
        return []

    X      = _extract_features(logs)
    preds  = _model.predict(X)
    scores = _model.score_samples(X)

    results = []
    for i, log in enumerate(logs):
        if preds[i] == -1:
            norm_score = float(np.clip(-scores[i], 0, 1))
            results.append({
                "log_id":        log["id"],
                "service":       log["service"],
                "timestamp":     log["timestamp"],
                "anomaly_score": round(norm_score, 3),
                "is_anomaly":    True,
                "anomaly_type":  _classify_anomaly(log, scores[i]),
            })
    return results