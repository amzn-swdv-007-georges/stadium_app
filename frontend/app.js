// ─────────────────────────────────────────────────────────────────────────────
// app.js — Security Command Dashboard
// STUB FILE — OpenCode will implement the function bodies below.
// Read the comments to understand what each function must do.
// ─────────────────────────────────────────────────────────────────────────────

// The backend API base URL.
// Flask runs on port 3000 and serves /api/entries.
const API_BASE = '';  // same origin — no need for a full URL when served by Flask


// ─── fetchEntries(gate) ───────────────────────────────────────────────────────
//
// Sends a GET request to the backend and passes the results to renderTable().
//
// Parameters:
//   gate — string, e.g. "A", "B", "C", "D", or "" for all gates
//
// What it must do:
//   1. Build the URL:
//      - If gate is empty → fetch('/api/entries')
//      - If gate is set   → fetch('/api/entries?gate=A')
//   2. Call fetch() with that URL
//   3. Parse the JSON response
//   4. Pass the entries array to renderTable()
//   5. Update #count-value with the number of entries returned
//   6. Update #status-badge to show "Backend Connected" (add class "connected")
//   7. On error: log the error and update #status-badge to show "Backend Offline"
//
// OpenCode will implement this function body.
//
async function fetchEntries(gate = '') {
  try {
    const url = gate ? `/api/entries?gate=${encodeURIComponent(gate)}` : '/api/entries';
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
//
// Clears the table body and renders one <tr> per entry.
//
// Parameters:
//   entries — array of objects from the backend, each with:
//             { id, person_id, gate, hour, bag }
//
// What it must do:
//   1. Clear #entries-body (remove all existing rows)
//   2. If entries is empty → show #empty-state, hide the table rows
//   3. For each entry, create a <tr> with five <td> cells:
//      - id
//      - person_id
//      - gate  (wrapped in a <span class="gate-badge gate-A"> etc.)
//      - hour
//      - bag
//   4. Append each row to #entries-body
//   5. Hide #empty-state once rows are rendered
//
// OpenCode will implement this function body.
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
    const cells = [
      entry.id,
      entry.person_id,
      entry.gate,
      entry.hour,
      entry.bag,
    ];
    cells.forEach((value, i) => {
      const td = document.createElement('td');
      if (i === 2) {
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


// ─── Event listeners ──────────────────────────────────────────────────────────
//
// OpenCode will attach these once the DOM is ready.
//
// 1. Gate filter dropdown — onchange → fetchEntries(selectedValue)
// 2. Refresh button       — onclick  → fetchEntries(currentFilterValue)
// 3. On page load         → fetchEntries('') to populate the table immediately
//
// OpenCode will implement this section.
//
document.addEventListener('DOMContentLoaded', () => {
  const filter = document.getElementById('gate-filter');
  const refresh = document.getElementById('refresh-btn');

  filter.addEventListener('change', () => fetchEntries(filter.value));
  refresh.addEventListener('click', () => fetchEntries(filter.value));

  fetchEntries('');
});
