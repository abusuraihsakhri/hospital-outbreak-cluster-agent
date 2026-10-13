/* Browser-only demonstration of the Python workers' illustrative thresholds.
   This does not calculate CDC NHSN outbreak classifications. */
(function (root) {
  "use strict";
  function containsSensitive(value) {
    const text = String(value == null ? "" : value);
    return [
      /\b(?:MRN)[:#\s-]*\d{4,10}\b/i,
      /\b\d{3}-\d{2}-\d{4}\b/,
      /\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/,
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/,
      /\b(?:DOB|Date of Birth)[:\s]*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b/i
    ].some(function (pattern) { return pattern.test(text); });
  }

  function evaluate(input) {
    if (!input || typeof input !== "object") throw new TypeError("A synthetic task is required.");
    const taskId = String(input.task_id || "").trim();
    const target = String(input.target_identifier || "").trim();
    const descriptor = String(input.status_descriptor || "NOMINAL").trim();
    if (!taskId || !target || taskId.length > 128 || target.length > 128) {
      throw new Error("Task and target identifiers must contain 1–128 characters.");
    }
    if ([taskId, target, descriptor].some(containsSensitive)) {
      throw new Error("Possible personal identifier detected. Use synthetic identifiers only.");
    }
    if (typeof input.primary_metric !== "number" || typeof input.secondary_metric !== "number") {
      throw new Error("Both measurements must be numeric.");
    }
    if (typeof input.is_critical_flag !== "boolean") {
      throw new Error("The critical flag must be a boolean.");
    }
    const alerts = [];
    function add(worker, urgency, summary, details) {
      alerts.push({
        origin_worker: worker, urgency: urgency, summary: summary,
        technical_details: details, actionable_remediation: "Review this synthetic example; no clinical action is inferred."
      });
    }
    if (!Number.isFinite(input.primary_metric)) {
      add("InputValidation", "ELEVATED_RISK", "Invalid primary measurement", "A finite number is required.");
    } else if (input.primary_metric > 25) {
      add("InvariantQCWorker", "ELEVATED_RISK", "Primary threshold exceeded", "Illustrative boundary: primary > 25.");
    }
    if (!Number.isFinite(input.secondary_metric)) {
      add("InputValidation", "ELEVATED_RISK", "Invalid secondary measurement", "A finite number is required.");
    } else if (input.is_critical_flag || input.secondary_metric > 12) {
      add("SafetyEscalationWorker", input.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
          "Safety flag or secondary threshold", "Illustrative boundary: secondary > 12, or manual critical flag.");
    }
    if (["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"].some(function (word) {
      return descriptor.toUpperCase().includes(word);
    })) {
      add("ProtocolConformanceWorker", "ELEVATED_RISK", "Descriptor flagged", "Keyword match in synthetic status descriptor.");
    }
    const critical = alerts.filter(function (a) { return a.urgency === "CRITICAL_STAT_PANIC"; }).length;
    const urgency = critical ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE";
    return {
      task_id: taskId, target_identifier: target,
      overall_urgency: urgency,
      integrity_status: critical ? "RECALIBRATION_REQUIRED" : alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL",
      total_alerts: alerts.length, critical_alerts_count: critical,
      alerts: alerts, execution: "local_browser_demo",
      note: "Demonstration thresholds only. Not an outbreak detection, NHSN surveillance, or clinical decision tool."
    };
  }
  const api = Object.freeze({ evaluate: evaluate, containsSensitive: containsSensitive });
  root.OutbreakDemo = api;
  if (typeof module === "object" && module.exports) module.exports = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
