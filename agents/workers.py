"""
Specialized Domain Worker Agents for Hospital Outbreak Cluster Agent.
Domain: Antimicrobial Stewardship & Microbiology
Standard: CLSI M100 / EUCAST / CDC NHSN Guidelines
"""
import math
import uuid
from typing import List
from .models import SystemTaskPayload, AgentAlert, UrgencyLevel


def _validate_numeric(value: float, field_name: str) -> List[AgentAlert]:
    """Validate that a numeric metric is finite and within acceptable bounds."""
    alerts = []
    if math.isnan(value) or math.isinf(value):
        alerts.append(AgentAlert(
            alert_id=f"QC-{uuid.uuid4().hex[:6]}",
            origin_worker="InputValidation",
            urgency=UrgencyLevel.ELEVATED,
            summary=f"Invalid numeric value in {field_name}",
            technical_details=f"Field '{field_name}' contains non-finite value ({value}). All metrics must be finite real numbers.",
            actionable_remediation="Verify input data source and ensure measurements are properly recorded as finite numeric values.",
        ))
    return alerts


class InvariantQCWorker:
    """Worker 1: Primary Mathematical & Protocol Boundary Auditor."""

    @classmethod
    def evaluate(cls, payload: SystemTaskPayload) -> List[AgentAlert]:
        alerts = []
        alerts.extend(_validate_numeric(payload.primary_metric, "primary_metric"))
        if alerts:
            return alerts
        if payload.primary_metric > 25.0:
            alerts.append(AgentAlert(
                alert_id=f"QC-{uuid.uuid4().hex[:6]}",
                origin_worker="InvariantQCWorker",
                urgency=UrgencyLevel.ELEVATED,
                summary="Primary Metric Threshold Exceeded",
                technical_details=f"Primary measurement ({payload.primary_metric:.2f}) exceeds illustrative boundary (25.00); this is not a guideline-derived clinical limit.",
                actionable_remediation="Review the synthetic input and the illustrative boundary.",
            ))
        return alerts


class SafetyEscalationWorker:
    """Worker 2: Safety Boundary, Toxicity & Emergency Interlock Worker."""

    @classmethod
    def evaluate(cls, payload: SystemTaskPayload) -> List[AgentAlert]:
        alerts = []
        alerts.extend(_validate_numeric(payload.secondary_metric, "secondary_metric"))
        if alerts:
            return alerts
        if payload.is_critical_flag or payload.secondary_metric > 12.0:
            alerts.append(AgentAlert(
                alert_id=f"SAFE-{uuid.uuid4().hex[:6]}",
                origin_worker="SafetyEscalationWorker",
                urgency=UrgencyLevel.CRITICAL_STAT if payload.is_critical_flag else UrgencyLevel.ELEVATED,
                summary="Critical Safety Interlock Triggered",
                technical_details=f"CriticalFlag={payload.is_critical_flag} with secondary index {payload.secondary_metric:.2f}.",
                actionable_remediation="Review the synthetic input and manual flag; do not use this output for clinical escalation.",
            ))
        return alerts


class ProtocolConformanceWorker:
    """Worker 3: Spec Conformance, Anomaly Triage & Discordance Checker."""

    @classmethod
    def evaluate(cls, payload: SystemTaskPayload) -> List[AgentAlert]:
        alerts = []
        desc_upper = str(payload.status_descriptor).upper()
        if any(w in desc_upper for w in ["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"]):
            alerts.append(AgentAlert(
                alert_id=f"CONF-{uuid.uuid4().hex[:6]}",
                origin_worker="ProtocolConformanceWorker",
                urgency=UrgencyLevel.ELEVATED,
                summary="Protocol Conformance Discordance Detected",
                technical_details=f"Descriptor '{payload.status_descriptor}' matches demonstration keywords; no guideline conformance assessment is performed.",
                actionable_remediation="Inspect the synthetic descriptor and its keyword match.",
            ))
        return alerts
