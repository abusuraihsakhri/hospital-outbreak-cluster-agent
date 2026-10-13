"""Regression tests for security, parsing, and API authentication."""
import csv

import pytest
from fastapi.testclient import TestClient

from agents.base import AuditTrail
from agents.api import app
from agents.llm_factory import LLMFactory
from cli import parse_boolean, main


def test_hmac_detects_signature_tampering():
    trail = AuditTrail(secret_key="synthetic-test-secret")
    trail.log("worker", "test", "EVENT", {"status": "ok"})
    assert trail.verify_integrity()
    trail.logs[0]["actor"] = "attacker"
    assert not trail.verify_integrity()


def test_hmac_detects_chain_and_hash_tampering():
    trail = AuditTrail(secret_key="synthetic-test-secret")
    trail.log("worker", "test", "EVENT", {"status": "ok"})
    trail.log("worker", "test", "EVENT", {"status": "ok"})
    assert trail.verify_integrity()
    trail.logs[0]["current_hash"] = "0" * 64
    assert not trail.verify_integrity()


def test_audit_log_access_returns_copy():
    trail = AuditTrail(secret_key="synthetic-test-secret")
    trail.log("worker", "test", "EVENT", {"status": "ok"})
    trail.get_trail()[0]["actor"] = "mutated-by-caller"
    assert trail.verify_integrity()


@pytest.mark.parametrize("value,expected", [
    ("False", False), ("false", False), ("0", False), ("no", False),
    ("true", True), ("YES", True), ("1", True), (False, False), (True, True)
])
def test_csv_boolean_parsing(value, expected):
    assert parse_boolean(value) is expected


def test_unrecognized_boolean_is_error():
    with pytest.raises(ValueError):
        parse_boolean("not-sure")


def test_batch_does_not_escalate_false_string(tmp_path):
    source, dest = tmp_path / "cases.csv", tmp_path / "results.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,status_descriptor,is_critical_flag\n"
        "T001,SYNTH-01,10,2,NOMINAL,False\n",
        encoding="utf-8",
    )
    assert main(["batch", "-i", str(source), "-o", str(dest)]) == 0
    with dest.open(newline="", encoding="utf-8") as stream:
        row = next(csv.DictReader(stream))
    assert row["overall_urgency"] == "ROUTINE"


def test_unsupported_llm_is_not_silently_mocked():
    with pytest.raises(ValueError, match="Unsupported"):
        LLMFactory.create("openai")


def test_api_requires_configured_token(monkeypatch):
    client = TestClient(app)
    monkeypatch.delenv("API_ACCESS_TOKEN", raising=False)
    assert client.get("/health").status_code == 200
    assert client.get("/api/audit/logs").status_code == 503
    monkeypatch.setenv("API_ACCESS_TOKEN", "synthetic-access-token")
    assert client.get("/api/audit/logs").status_code == 401
    assert client.get("/api/audit/logs", headers={"X-API-Key": "synthetic-access-token"}).status_code == 200
    payload = {
        "task_id": "TEST-001", "target_identifier": "SYNTH-01",
        "primary_metric": 10, "secondary_metric": 2
    }
    assert client.post("/api/audit", json=payload).status_code == 401
    resp = client.post("/api/audit", headers={"X-API-Key": "synthetic-access-token"}, json=payload)
    assert resp.status_code == 200
    assert resp.json()["overall_urgency"] == "ROUTINE"
