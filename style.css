const dateSelect = document.getElementById('dateSelect');
const todayStr = new Date().toISOString().slice(0,10);
dateSelect.value = todayStr;

let range = {min:158, max:167};
let currentData = {temps:[], chemicals:[], tasks:[]};

function escapeHtml(str){
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

async function api(url, opts){
  const res = await fetch(url, Object.assign({headers:{'Content-Type':'application/json'}}, opts));
  if(!res.ok) throw new Error('Request failed: ' + res.status);
  return res.json();
}

async function loadRange(){
  try{ range = await api('/api/range'); }catch(e){ /* keep defaults */ }
  document.getElementById('rangeDisplay').textContent = `${range.min}–${range.max}°F`;
}

async function loadEntries(){
  const d = dateSelect.value;
  try{
    currentData = await api(`/api/entries?date=${d}`);
  }catch(e){
    currentData = {temps:[], chemicals:[], tasks:[]};
  }
  renderAll();
}

function renderThermometer(){
  const temps = currentData.temps;
  const latest = temps.length ? temps[temps.length-1] : null;
  const fill = document.getElementById('thermFill');
  const bulb = document.getElementById('thermBulb');
  const bulbLabel = document.getElementById('thermBulbLabel');
  const valueEl = document.getElementById('latestTemp');
  const statusEl = document.getElementById('tempStatus');

  if(!latest){
    fill.style.height = '0%'; fill.style.background = 'var(--sage)';
    bulb.style.background = 'var(--sage)'; bulbLabel.textContent = '--';
    valueEl.textContent = '--';
    statusEl.textContent = 'No reading yet'; statusEl.className = 'status none';
    return;
  }
  const val = latest.value;
  const lo = range.min - 15, hi = range.max + 15;
  const pct = Math.max(4, Math.min(100, ((val - lo) / (hi - lo)) * 100));
  const inRange = val >= range.min && val <= range.max;
  fill.style.height = pct + '%';
  fill.style.background = inRange ? 'var(--ok)' : 'var(--clay)';
  bulb.style.background = inRange ? 'var(--ok)' : 'var(--clay)';
  bulbLabel.textContent = Math.round(val);
  valueEl.textContent = val;
  statusEl.textContent = inRange ? 'Within safe range' : 'Out of range';
  statusEl.className = 'status ' + (inRange ? 'ok' : 'bad');
}

function renderTempList(){
  const list = document.getElementById('tempList');
  list.innerHTML = '';
  if(!currentData.temps.length){ list.innerHTML = '<p class="empty">No temperature checks logged for this day.</p>'; return; }
  [...currentData.temps].reverse().forEach(t=>{
    const inRange = t.value >= range.min && t.value <= range.max;
    const li = document.createElement('li');
    li.innerHTML = `<span><strong>${t.value}°F</strong> at ${t.time}${t.note ? ' — '+escapeHtml(t.note):''}
      <span class="meta">${inRange ? 'in range' : 'out of range'}</span></span>
      <button class="del" data-id="${t.id}">Remove</button>`;
    list.appendChild(li);
  });
  list.querySelectorAll('.del').forEach(btn=>{
    btn.addEventListener('click', async ()=>{
      await api(`/api/temps/${btn.dataset.id}`, {method:'DELETE'});
      await loadEntries(); await renderHistory();
    });
  });
}

function renderChemList(){
  const list = document.getElementById('chemList');
  list.innerHTML = '';
  if(!currentData.chemicals.length){ list.innerHTML = '<p class="empty">No chemical usage logged for this day.</p>'; return; }
  [...currentData.chemicals].reverse().forEach(c=>{
    const li = document.createElement('li');
    li.innerHTML = `<span><strong>${escapeHtml(c.name)}</strong> — ${c.qty} ${c.unit}
      <span class="meta">${escapeHtml(c.category||'')}</span></span>
      <button class="del" data-id="${c.id}">Remove</button>`;
    list.appendChild(li);
  });
  list.querySelectorAll('.del').forEach(btn=>{
    btn.addEventListener('click', async ()=>{
      await api(`/api/chemicals/${btn.dataset.id}`, {method:'DELETE'});
      await loadEntries(); await renderHistory();
    });
  });
}

function renderTasks(){
  const wrap = document.getElementById('taskList');
  wrap.innerHTML = '';
  if(!currentData.tasks.length){ wrap.innerHTML = '<p class="empty">No tasks added yet today.</p>'; return; }
  currentData.tasks.forEach(task=>{
    const row = document.createElement('div');
    row.className = 'task-row' + (task.done ? ' done' : '');
    row.innerHTML = `<input type="checkbox" ${task.done ? 'checked':''} data-id="${task.id}">
      <label>${escapeHtml(task.text)}</label>
      <button class="del" data-id="${task.id}">Remove</button>`;
    wrap.appendChild(row);
  });
  wrap.querySelectorAll('input[type=checkbox]').forEach(cb=>{
    cb.addEventListener('change', async ()=>{
      await api(`/api/tasks/${cb.dataset.id}`, {method:'PATCH', body:JSON.stringify({done:cb.checked})});
      await loadEntries(); await renderHistory();
    });
  });
  wrap.querySelectorAll('.del').forEach(btn=>{
    btn.addEventListener('click', async ()=>{
      await api(`/api/tasks/${btn.dataset.id}`, {method:'DELETE'});
      await loadEntries(); await renderHistory();
    });
  });
}

function renderAll(){ renderThermometer(); renderTempList(); renderChemList(); renderTasks(); }

document.getElementById('tempForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const time = document.getElementById('tempTime').value;
  const value = parseFloat(document.getElementById('tempValue').value);
  const note = document.getElementById('tempNote').value.trim();
  if(!time || isNaN(value)) return;
  await api('/api/temps', {method:'POST', body:JSON.stringify({date:dateSelect.value, time, value, note})});
  e.target.reset();
  await loadEntries(); await renderHistory();
});

document.getElementById('chemForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const name = document.getElementById('chemName').value.trim();
  const category = document.getElementById('chemCategory').value;
  const qty = parseFloat(document.getElementById('chemQty').value);
  const unit = document.getElementById('chemUnit').value;
  if(!name || isNaN(qty)) return;
  await api('/api/chemicals', {method:'POST', body:JSON.stringify({date:dateSelect.value, name, category, qty, unit})});
  e.target.reset();
  await loadEntries(); await renderHistory();
});

document.getElementById('taskForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const text = document.getElementById('taskText').value.trim();
  if(!text) return;
  await api('/api/tasks', {method:'POST', body:JSON.stringify({date:dateSelect.value, text})});
  e.target.reset();
  await loadEntries(); await renderHistory();
});

dateSelect.addEventListener('change', loadEntries);

async function renderHistory(){
  const body = document.getElementById('historyBody');
  const emptyMsg = document.getElementById('historyEmpty');
  let rows = [];
  try{ rows = await api('/api/history'); }catch(e){ rows = []; }
  body.innerHTML = '';
  if(!rows.length){ emptyMsg.style.display = 'block'; return; }
  emptyMsg.style.display = 'none';
  rows.forEach(row=>{
    const tempsStr = row.temps.length
      ? row.temps.map(t=>{
          const bad = t.value < range.min || t.value > range.max;
          return `<span class="${bad?'bad-cell':''}">${t.value}°F@${t.time}</span>`;
        }).join(', ')
      : '—';
    const chemStr = row.chemicals.length
      ? row.chemicals.map(c=>`${escapeHtml(c.name)} (${c.qty}${c.unit})`).join(', ')
      : '—';
    const taskStr = row.tasks_total ? `${row.tasks_done}/${row.tasks_total} done` : '—';
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${row.date}</td><td>${tempsStr}</td><td>${chemStr}</td><td>${taskStr}</td>`;
    body.appendChild(tr);
  });
}

document.getElementById('exportBtn').addEventListener('click', ()=>{
  window.location = '/api/export.csv';
});

(async function init(){
  await loadRange();
  await loadEntries();
  await renderHistory();
})();
