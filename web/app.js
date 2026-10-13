"use strict";
(function () {
  const el = function (id) { return document.getElementById(id); };
  const status = el("status");
  const list = el("alert-list");
  const exportButton = el("export");
  let latest = null;
  let count = 0;
  let alertCount = 0;
  let criticalCount = 0;

  el("audit-form").addEventListener("submit", function (event) {
    event.preventDefault();
    list.replaceChildren();
    latest = null;
    exportButton.disabled = true;
    try {
      const readNumber = function (id) {
        const field = el(id);
        if (!field.value.trim()) throw new Error("Both metrics are required.");
        const n = Number(field.value);
        if (!Number.isFinite(n)) throw new Error("Both metrics must be finite numbers.");
        return n;
      };
      const result = OutbreakDemo.evaluate({
        task_id: el("task-id").value,
        target_identifier: el("target-id").value,
        primary_metric: readNumber("primary"),
        secondary_metric: readNumber("secondary"),
        status_descriptor: el("descriptor").value,
        is_critical_flag: el("critical").checked
      });
      latest = result;
      count += 1;
      alertCount += result.total_alerts;
      criticalCount += result.critical_alerts_count;
      el("count").textContent = String(count);
      el("alerts-count").textContent = String(alertCount);
      el("critical-count").textContent = String(criticalCount);
      status.replaceChildren();
      const heading = document.createElement("strong");
      heading.textContent = result.overall_urgency.replaceAll("_", " ");
      const detail = document.createElement("span");
      detail.textContent = result.total_alerts + " rule(s) triggered · " + result.integrity_status.replaceAll("_", " ");
      status.append(heading, detail);
      result.alerts.forEach(function (alert) {
        const item = document.createElement("li");
        item.textContent = alert.origin_worker + ": " + alert.summary;
        list.appendChild(item);
      });
      el("json-output").textContent = JSON.stringify(result, null, 2);
      exportButton.disabled = false;
    } catch (error) {
      status.textContent = error.message;
      status.classList.add("error");
      el("json-output").textContent = "No result.";
      return;
    }
    status.classList.remove("error");
  });

  exportButton.addEventListener("click", function () {
    if (!latest) return;
    const blob = new Blob([JSON.stringify(latest, null, 2) + "\n"], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "synthetic-outbreak-audit.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  });
})();
