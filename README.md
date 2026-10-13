# Hospital Outbreak Cluster Agent

A Python rules-engine demonstration and a static browser interface for **synthetic** hospital surveillance records. The supported agent evaluation lives in the agents/ directory, with its CLI in cli.py.

**Scope:** The hard-coded numeric boundaries (primary > 25; secondary > 12), manual critical flag, and descriptor keyword checks are illustrative. They are **not** CDC NHSN outbreak detection criteria, validated EARS calculations, genomic transmission inference, or clinical recommendations. Do not enter real patient data or use outputs for clinical decisions.

## Browser demonstration

The static interface in [web/](web/) runs entirely in the browser using JavaScript rules corresponding to the three Python workers. It needs no API, Pyodide, or runtime server and can be hosted on GitHub Pages. Open web/index.html directly, or serve the directory locally:

    python -m http.server 8080 --directory web

The interface accepts synthetic IDs and two metrics, displays triggered rules, and exports a local JSON summary. Nothing is sent to the application server by this interface. Its basic identifier check is **not** de-identification or an assurance of HIPAA compliance.

## Python installation and usage

Python 3.10–3.12 is exercised in CI; the declared minimum is Python 3.9.

    python -m pip install -e ".[server,test]"
    python cli.py audit --task-id SYNTH-001 --target SYNTH-01 --primary 27 --secondary 13
    python cli.py batch -i sample.csv -o results.csv
    python cli.py verify-audit
    python -m pytest -q
    node --test web/test_engine.cjs

CSV inputs for the root CLI use task_id, target_identifier, primary_metric, secondary_metric, status_descriptor, and is_critical_flag (accepted: true/false, 1/0, yes/no). Invalid rows are skipped with a warning.

## REST API

    export AUDIT_SECRET_KEY="replace-with-a-random-secret-at-least-32-bytes"
    export API_ACCESS_TOKEN="replace-with-an-independent-long-random-token"
    python cli.py serve --host 127.0.0.1 --port 8000

    curl -H "X-API-Key: $API_ACCESS_TOKEN" -H "Content-Type: application/json" \
      -d '{"task_id":"SYNTH-001","target_identifier":"SYNTH-01","primary_metric":27,"secondary_metric":13}' \
      http://127.0.0.1:8000/api/audit

GET /health and GET /metrics are available without a token; POST /api/audit, POST /api/chat, and GET /api/audit/logs require the X-API-Key token. Protected routes return 503 if no token is configured. Run only behind appropriate network controls; rate limiting, persistence, and regulated-data compliance are not provided.

## Security and data handling

- An HMAC-SHA256 in-memory audit ledger signs events and validates both signatures and chain linkage. **This is not durable storage**: entries are lost when the process stops, as is the automatically generated development key.
- The regular-expression identifier guard blocks common formats only and is not comprehensive PHI detection. No actual health records should be submitted.
- The model factory implements a deterministic mock only. Requests for other providers fail explicitly.
- The browser demonstration does not load external JavaScript, use browser storage, or contact the API; its downloadable JSON file remains on the device unless shared.
- Docker Compose binds to loopback and requires AUDIT_SECRET_KEY and API_ACCESS_TOKEN from the environment. Do not commit production keys.

## Container

    export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
    export API_ACCESS_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
    docker compose up --build

## Project layout

- agents/ — Pydantic schemas, rule workers, supervisor, in-memory audit, mock interface, REST API.
- cli.py — root CLI and CSV processor.
- web/ — static browser demonstration and Node regression tests.
- hospital_outbreak_cluster_agent/ and outbreak_pulse.py — separate older example implementations retained for compatibility.
- enrichment.py — generic threshold-engine placeholders; their names do **not** imply the named scientific algorithms are implemented.
- tests/, test_outbreak_pulse.py — Python regression tests.
- .github/workflows/ — CI and browser publication configuration.

## License

MIT; see [LICENSE](LICENSE).
