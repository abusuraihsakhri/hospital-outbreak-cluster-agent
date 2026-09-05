# Hospital Outbreak Cluster Agent

> **Domain:** Infectious Disease Surveillance & Microbiology
> **Reference Guidelines & Standards:** `CLSI M100, EUCAST & CDC NHSN Clinical Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Hospital Outbreak Cluster Agent** is an advanced analytical and computational platform implementing Spatial-Temporal Nosocomial Outbreak & Transmission Tracker. It detects healthcare-associated infection (HAI) outbreaks including C. diff, MRSA, VRE, and Candida auris using EARS algorithms and multi-agent consensus.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`Severity`** — dedicated module for severity evaluation and state verification.
- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks.
- **`AgentAlert`** — dedicated module for agent alert evaluation and state verification.
- **`SpatialWardClusterAgent`**: Specialized Sub-Agent 1 for hospital-outbreak-cluster-agent
- **`TemporalAberrationAgent`**: Specialized Sub-Agent 2 for hospital-outbreak-cluster-agent
- **`GenomicTransmissionMatcherAgent`**: Specialized Sub-Agent 3 for hospital-outbreak-cluster-agent

### 🛡️ Enrichment Modules

- **Genomic Epidemiology Transmission Graph Builder** — cgMLST/WGS linkage analysis
- **Real-Time EARS-3 Algorithm** — CDC Early Aberration Reporting System
- **Candida Auris Contact Tracing Module** — Dedicated outbreak management
- **Ward Bed-Layout Spatial Heatmap** — Infection density visualization
- **Automated NHSN Reporting Pipeline** — CDC NHSN HAI report generation
- **Hand Hygiene Compliance Correlation** — Contributing factor analysis
- **Environmental Contamination Sampling Advisor** — Targeted sampling strategies
- **Post-Outbreak Debrief Automation** — Root-cause analysis generation

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/hospital-outbreak-cluster-agent.git
cd hospital-outbreak-cluster-agent

# Install dependencies
pip install pydantic pytest fastapi uvicorn
```

---

## 💻 CLI Quickstart & Usage

### 1. Guided Interactive Mode
```bash
python cli.py
```

### 2. Direct Parameterized Evaluation
```bash
python cli.py audit --task-id <value> --target <value> --primary <value> --secondary <value>
```

### Parameter Reference
- `--task-id`: Unique task / case identifier
- `--target`: Entity, patient key, or genomic target
- `--primary`: Primary domain measurement or score (float)
- `--secondary`: Secondary kinetic or confidence score (float)
- `--critical`: Emergency escalation flag
- `--status`: Status code or phenotype descriptor

### Batch Processing
```bash
# Process CSV file
python cli.py batch -i sample.csv -o results.csv
```

### Audit Verification
```bash
# Verify HMAC audit trail integrity
python cli.py verify-audit
```

---

## 🌐 REST API Server

```bash
# Launch FastAPI server
python cli.py serve --host 127.0.0.1 --port 8000
```

### API Endpoints

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/health` | GET | Service health check |
| `/metrics` | GET | Prometheus-compatible metrics |
| `/api/audit` | POST | Submit evaluation task |
| `/api/chat` | POST | Query supervisory assistant |
| `/api/audit/logs` | GET | Retrieve audit trail |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, and patient identifiers. All violations are logged to the tamper-evident audit trail.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition. **Set `AUDIT_SECRET_KEY` environment variable in production.**
* **Input Validation:** Automatic detection of non-finite numeric values (NaN, Infinity) in all metric inputs.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
docker build -t hospital-outbreak-cluster-agent .
docker run -p 8000:8000 hospital-outbreak-cluster-agent
```

---

## 📁 Project Structure

```
hospital-outbreak-cluster-agent/
├── agents/                          # Core multi-agent system
│   ├── api.py                       # FastAPI REST endpoints
│   ├── base.py                      # Security, PHI guard, audit trail
│   ├── llm_factory.py              # LLM provider abstraction
│   ├── metrics.py                   # Prometheus metrics collector
│   ├── models.py                    # Pydantic data models
│   ├── streamer.py                  # WebSocket telemetry
│   ├── supervisor.py                # Master orchestrator
│   ├── workers.py                   # Domain worker agents
│   └── learning.py                  # Bayesian calibration engine
├── tests/                           # Test suite
│   ├── test_hospital_outbreak_cluster_agent.py
│   └── test_enrichment.py
├── hospital_outbreak_cluster_agent/ # Package distribution module
├── cli.py                           # Main CLI entry point
├── simulator.py                     # High-throughput simulation
├── enrichment.py                    # Domain enrichment engines
├── outbreak_pulse.py               # Spatial-temporal clustering
├── pyproject.toml                   # Project configuration
└── Dockerfile                       # Container definition
```
