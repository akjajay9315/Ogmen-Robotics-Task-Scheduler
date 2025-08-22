const API = "http://localhost:8000";

const el = (id) => document.getElementById(id);
let selectedDevice = null;

async function getJSON(url, opts = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
  return res.json();
}

function deviceRow(d) {
  return `<div class="row">
    <button onclick='selectDevice("${d.device_id}","${d.device_name}")'>Select</button>
    <div><strong>${d.device_name}</strong> <span class="muted">(${d.model})</span> <code>${d.device_id}</code></div>
  </div>`;
}

function scheduleRow(s) {
  return `<div class="row">
    <div>⏰ ${new Date(s.scheduled_time).toLocaleString()}</div>
    <div class="status">• ${s.status}</div>
    <button onclick='execute("${s.schedule_id}")'>Execute</button>
    <code>${s.schedule_id}</code>
  </div>`;
}

function logRow(l) {
  return `<div class="row">
    <div>${new Date(l.executed_at).toLocaleString()}</div>
    <div>${l.success ? "✅" : "❌"}</div>
    <div>${l.result}</div>
    <code>${l.log_id}</code>
  </div>`;
}

async function loadDevices() {
  const devices = await getJSON(`${API}/devices/`);
  el("devices").innerHTML =
    devices.map(deviceRow).join("") || "<div class='muted'>No devices</div>";
  const sel = el("device_select");
  sel.innerHTML = devices
    .map((d) => `<option value="${d.device_id}">${d.device_name}</option>`)
    .join("");
  if (devices.length && !selectedDevice)
    selectDevice(devices[0].device_id, devices[0].device_name);
}

async function loadDefinitions() {
  const defs = await getJSON(`${API}/tasks/definitions/`);
  el("definitions").innerHTML =
    defs
      .map(
        (d) =>
          `<div><strong>${d.task_name}</strong> schema: <code>${JSON.stringify(
            d.parameters_schema
          )}</code></div>`
      )
      .join("") || "<div class='muted'>No definitions</div>";
  const sel = el("definition_select");
  sel.innerHTML = defs
    .map((d) => `<option value="${d.task_id}">${d.task_name}</option>`)
    .join("");
}

async function loadSchedules(deviceId) {
  const scheds = await getJSON(`${API}/tasks/${deviceId}/scheduled/`);
  el("schedules").innerHTML =
    scheds.map(scheduleRow).join("") || "<div class='muted'>No schedules</div>";
}

async function loadLogs(deviceId) {
  const logs = await getJSON(`${API}/tasks/${deviceId}/logs/`);
  el("logs").innerHTML =
    logs.map(logRow).join("") || "<div class='muted'>No logs</div>";
}

function selectDevice(id, name) {
  selectedDevice = id;
  el("selDeviceName").textContent = name;
  el("selDeviceNameLogs").textContent = name;
  loadSchedules(id);
  loadLogs(id);
}

async function addDevice() {
  const device_name = el("device_name").value.trim();
  const model = el("device_model").value.trim();
  if (!device_name || !model) return alert("Enter device name and model");
  await getJSON(`${API}/devices/`, {
    method: "POST",
    body: JSON.stringify({ device_name, model }),
  });
  el("device_name").value = "";
  el("device_model").value = "";
  await loadDevices();
}

async function addDefinition() {
  const task_name = el("task_name").value.trim();
  let parameters_schema = {};
  try {
    parameters_schema = JSON.parse(el("schema").value.trim());
  } catch {
    return alert("Invalid JSON for parameters_schema");
  }
  await getJSON(`${API}/tasks/definitions/`, {
    method: "POST",
    body: JSON.stringify({ task_name, parameters_schema }),
  });
  el("task_name").value = "";
  el("schema").value = "";
  await loadDefinitions();
}

async function scheduleTask() {
  const device_id = el("device_select").value;
  const task_id = el("definition_select").value;
  const scheduled_time_local = el("scheduled_time").value; // local datetime
  if (!scheduled_time_local) return alert("Pick a scheduled time");
  const scheduled_time = new Date(scheduled_time_local).toISOString();
  let parameters = {};
  try {
    parameters = JSON.parse(el("params").value || "{}");
  } catch {
    return alert("Invalid JSON for parameters");
  }

  try {
    const resp = await getJSON(`${API}/tasks/${device_id}/schedule/`, {
      method: "POST",
      body: JSON.stringify({ task_id, scheduled_time, parameters }),
    });
    el("schedule_feedback").textContent = `Scheduled ${resp.schedule_id}`;
    if (selectedDevice === device_id) await loadSchedules(device_id);
  } catch (e) {
    el("schedule_feedback").textContent = `Error: ${e.message}`;
  }
}

async function execute(schedule_id) {
  const result = prompt("Enter execution result (text):", "ok");
  if (result === null) return;
  const success = confirm("Mark as SUCCESS? (Cancel = FAILED)");
  await getJSON(`${API}/tasks/${schedule_id}/execute/`, {
    method: "POST",
    body: JSON.stringify({ result, success }),
  });
  if (selectedDevice) {
    await loadSchedules(selectedDevice);
    await loadLogs(selectedDevice);
  }
}

// initial load
loadDevices();
loadDefinitions();

// Poll the selected device every 5s (simple real-time)
setInterval(() => {
  if (selectedDevice) {
    loadSchedules(selectedDevice);
    loadLogs(selectedDevice);
  }
}, 5000);
