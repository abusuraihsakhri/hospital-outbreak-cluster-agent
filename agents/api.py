"""
FastAPI REST API Server for Hospital Outbreak Cluster Agent.
"""
from typing import Dict, Any, List
import os
import hmac
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Hospital Outbreak Cluster Agent API",
    description="Synthetic-record demonstration of three configurable rule workers",
    version="3.0.0-ENTERPRISE",
)


def require_api_token(x_api_key: str = Header(default="")):
    """Require a deployment-configured token for all data-bearing API routes."""
    configured = os.getenv("API_ACCESS_TOKEN", "")
    if not configured:
        raise HTTPException(status_code=503, detail="API_ACCESS_TOKEN is not configured")
    if not hmac.compare_digest(x_api_key, configured):
        raise HTTPException(status_code=401, detail="Invalid API key")


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "hospital-outbreak-cluster-agent", "domain": "Antimicrobial Stewardship & Microbiology", "standard": "Demonstration rules only; not a clinical guideline", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit", dependencies=[Depends(require_api_token)])
def api_audit(payload: SystemTaskPayload):
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


@app.post("/api/chat", dependencies=[Depends(require_api_token)])
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except Exception:
        raise HTTPException(status_code=400, detail="Query rejected or unavailable")


@app.get("/api/audit/logs", dependencies=[Depends(require_api_token)])
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
