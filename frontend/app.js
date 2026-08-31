// ─────────────────────────────────────────────────────────────────────────────
// app.js — Security Command Dashboard
// ─────────────────────────────────────────────────────────────────────────────
// Fetches entry data from the backend API and renders it in the table.
// This file performs HTTP requests and DOM rendering only — it has zero
// knowledge of the database schema or SQL. All data comes from the backend
// as JSON arrays of entry objects: { id, person_id, gate, hour, bag }.
// ─────────────────────────────────────────────────────────────────────────────

// The backend API base URL — same origin, since Flask serves both the UI
// and the /api/* endpoints.
const API_BASE = '';


// ─── fetchEntries(gate) ───────────────────────────────────────────────────────
// Sends a GET request to the backend and passes the results to renderTable().
//
// Parameters:
//   gate — string, e.g. "A", "B", "C", "D", or "" for all gates
//
// Always hits GET /api/entries. When a gate is selected it appends
// ?gate=<gate> so the backend can filter server-side.
//
async function fetchEntries(gate = '') {
  try {
    const url = gate ? `${API_BASE}/api/entries?gate=${encodeURIComponent(gate)}`
                     : `${API_BASE}/api/entries`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const entries = await res.json();
    renderTable(entries);

    document.getElementById('count-value').textContent = entries.length;

    const badge = document.getElementById('status-badge');
    badge.textContent = 'Backend Connected';
    badge.classList.add('connected');
  } catch (err) {
    console.error(err);
    const badge = document.getElementById('status-badge');
    badge.textContent = 'Backend Offline';
    badge.classList.remove('connected');
  }
}


// ─── renderTable(entries) ─────────────────────────────────────────────────────
// Clears the table body and renders one <tr> per entry.
//
// Parameters:
//   entries — array of objects: { id, person_id, gate, hour, bag }
//
function renderTable(entries) {
  const body = document.getElementById('entries-body');
  const emptyState = document.getElementById('empty-state');
  body.innerHTML = '';

  if (!entries || entries.length === 0) {
    emptyState.style.display = 'block';
    return;
  }

  emptyState.style.display = 'none';

  entries.forEach(entry => {
    const tr = document.createElement('tr');
    const cells = [entry.id, entry.person_id, entry.gate, entry.hour, entry.bag];

    cells.forEach((value, i) => {
      const td = document.createElement('td');
      if (i === 2) {
        // Gate column — wrap in a coloured badge (gate-A, gate-B, …)
        const badge = document.createElement('span');
        badge.className = `gate-badge gate-${value}`;
        badge.textContent = value;
        td.appendChild(badge);
      } else {
        td.textContent = value;
      }
      tr.appendChild(td);
    });

    body.appendChild(tr);
  });
}


// ─── Event wiring ─────────────────────────────────────────────────────────────
// 1. Gate filter dropdown — on change, re-fetch with the selected gate.
// 2. Refresh button       — on click, re-fetch with the current filter.
// 3. On page load         — fetch all entries immediately.
//
document.addEventListener('DOMContentLoaded', () => {
  const filter = document.getElementById('gate-filter');
  const refresh = document.getElementById('refresh-btn');

  filter.addEventListener('change', () => fetchEntries(filter.value));
  refresh.addEventListener('click', () => fetchEntries(filter.value));

  fetchEntries('');
});
