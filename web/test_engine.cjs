const { test } = require("node:test");
const assert = require("node:assert/strict");
const { evaluate, containsSensitive } = require("./engine.js");

const record = {
  task_id: "TASK-01", target_identifier: "SYNTH-01",
  primary_metric: 10, secondary_metric: 2,
  status_descriptor: "NOMINAL", is_critical_flag: false
};
test("normal synthetic record", () => {
  const r = evaluate(record);
  assert.equal(r.overall_urgency, "ROUTINE");
  assert.equal(r.total_alerts, 0);
  assert.equal(r.execution, "local_browser_demo");
  assert.ok(!("audit_hash" in r));
});
test("strict threshold boundaries", () => {
  assert.equal(evaluate({ ...record, primary_metric: 25, secondary_metric: 12 }).total_alerts, 0);
  const result = evaluate({ ...record, primary_metric: 26, secondary_metric: 13 });
  assert.equal(result.total_alerts, 2);
  assert.equal(result.overall_urgency, "ELEVATED_RISK");
});
test("manual critical flag and descriptor", () => {
  const r = evaluate({ ...record, is_critical_flag: true, status_descriptor: "DISCORDANT_ANOMALY" });
  assert.equal(r.critical_alerts_count, 1);
  assert.equal(r.total_alerts, 2);
  assert.equal(r.overall_urgency, "CRITICAL_STAT_PANIC");
});
test("invalid numbers and malformed records", () => {
  const r = evaluate({ ...record, primary_metric: Infinity });
  assert.equal(r.total_alerts, 1);
  assert.equal(r.alerts[0].origin_worker, "InputValidation");
  assert.throws(() => evaluate({ ...record, secondary_metric: "13" }), /numeric/);
  assert.throws(() => evaluate({ ...record, is_critical_flag: "false" }), /boolean/);
  assert.throws(() => evaluate({ ...record, task_id: "" }), /identifiers/);
});
test("obvious identifiers are rejected (not deidentification)", () => {
  assert.equal(containsSensitive("MRN-123456"), true);
  assert.throws(() => evaluate({ ...record, target_identifier: "123-45-6789" }), /personal identifier/);
});
