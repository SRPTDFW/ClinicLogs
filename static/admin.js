function escapeHtml(str){
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

let range = {min:158, max:167};

async function api(url){
  const res = await fetch(url);
  if(!res.ok) throw new Error('failed');
  return res.json();
}

async function renderHistory(){
  const filter = document.getElementById('clinicFilter').value;
  const body = document.getElementById('historyBody');
  const emptyMsg = document.getElementById('historyEmpty');
  let rows = [];
  try{
    range = await api('/api/range');
    rows = await api(`/api/history?clinic_id=${filter}`);
  }catch(e){ rows = []; }
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
    tr.innerHTML = `<td>${row.date}</td><td>${escapeHtml(row.clinic)}</td><td>${tempsStr}</td><td>${chemStr}</td><td>${taskStr}</td>`;
    body.appendChild(tr);
  });
}

document.getElementById('clinicFilter').addEventListener('change', renderHistory);
document.getElementById('exportBtn').addEventListener('click', ()=>{
  const filter = document.getElementById('clinicFilter').value;
  window.location = `/api/export.csv?clinic_id=${filter}`;
});

renderHistory();
