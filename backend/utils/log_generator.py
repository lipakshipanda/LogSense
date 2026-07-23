import random
import uuid
from datetime import datetime
from faker import Faker

fake = Faker()

SERVICES = [
    "auth-service",
    "payment-service",
    "order-service",
    "inventory-service",
    "notification-service"
]

LOG_TEMPLATES = {
    "INFO":     [
        "User {user} logged in successfully",
        "Order {id} created",
        "Payment processed for {id}",
        "Cache refreshed",
        "Health check OK"
    ],
    "WARN":     [
        "High memory usage: {val}%",
        "Slow DB query: {ms}ms",
        "Retry attempt {n} for {id}",
        "Rate limit approaching"
    ],
    "ERROR":    [
        "Connection refused to DB",
        "Timeout after {ms}ms for {id}",
        "Null pointer in {func}",
        "Failed to send notification"
    ],
    "CRITICAL": [
        "Service crash detected",
        "DB connection pool exhausted",
        "Out of memory error",
        "Disk full on node {n}"
    ],
}

def generate_log(inject_anomaly=False):
    service = random.choice(SERVICES)

    if inject_anomaly:
        level = random.choice(["ERROR", "CRITICAL"])
        latency = random.uniform(2000, 8000)
        status = random.choice([500, 502, 503])
    else:
        level = random.choices(
            ["INFO", "WARN", "ERROR", "CRITICAL"],
            weights=[70, 20, 8, 2]
        )[0]
        latency = random.uniform(10, 400)
        status = 200 if level == "INFO" else random.choice([200, 400, 500])

    template = random.choice(LOG_TEMPLATES[level])
    message = template.format(
        user=fake.user_name(),
        id=str(uuid.uuid4())[:8],
        val=random.randint(80, 99),
        ms=int(latency),
        n=random.randint(1, 5),
        func=fake.word()
    )

    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "service": service,
        "level": level,
        "message": message,
        "latency_ms": round(latency, 2),
        "status_code": status,
    }

def generate_batch(n=50, anomaly_ratio=0.1):
    logs = []
    for _ in range(n):
        inject = random.random() < anomaly_ratio
        logs.append(generate_log(inject_anomaly=inject))
    return logs