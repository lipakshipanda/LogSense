from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import logs, anomalies, rca, stats

app = FastAPI(title="LogSense AIOps API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["Anomalies"])
app.include_router(rca.router, prefix="/api/rca", tags=["RCA"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])

@app.get("/")
def root():
    return {"message": "LogSense AIOps API is running"}