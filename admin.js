:root{
  --bg:#F7F5F1; --surface:#FFFFFF; --ink:#1E2B2E; --ink-soft:#57696B;
  --teal:#2D6A6A; --teal-deep:#1F4A4A; --clay:#C9622D; --sage:#93A69B;
  --sage-pale:#E9EEE9; --ok:#4C7A5B; --line:#DEDACE; --radius:14px;
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'IBM Plex Sans',sans-serif;padding:28px 20px 60px;}
.wrap{max-width:1120px;margin:0 auto;}
a{color:var(--teal);}

header{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px;
  border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:24px;}
header h1{font-family:'Fraunces',serif;font-weight:700;font-size:clamp(24px,4vw,36px);margin:0 0 4px;letter-spacing:-0.01em;}
header p{margin:0;color:var(--ink-soft);font-size:14px;}
.header-controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}

select,input[type=date],input[type=number],input[type=text],input[type=time],input[type=password]{
  font-family:'IBM Plex Sans',sans-serif;border:1.5px solid var(--line);background:var(--surface);
  border-radius:8px;padding:8px 10px;font-size:14px;color:var(--ink);
}
select:focus,input:focus{outline:2px solid var(--teal);outline-offset:1px;}

.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
@media (max-width:820px){.grid{grid-template-columns:1fr;}}

.panel{background:var(--surface);border-radius:var(--radius);border:1px solid var(--line);padding:22px;position:relative;overflow:hidden;}
.panel::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--teal);}
.panel.chem::before{background:var(--clay);}
.panel h2{font-family:'Fraunces',serif;font-size:19px;margin:4px 0 2px;font-weight:600;}
.eyebrow{text-transform:uppercase;font-size:11px;letter-spacing:0.12em;color:var(--sage);font-weight:600;}
.panel .desc{color:var(--ink-soft);font-size:13px;margin:0 0 16px;}

.therm-row{display:flex;gap:22px;align-items:center;}
.therm{width:34px;height:150px;border-radius:17px;background:var(--sage-pale);border:2px solid var(--line);position:relative;overflow:hidden;flex-shrink:0;}
.therm-fill{position:absolute;bottom:0;left:0;right:0;background:var(--ok);transition:height .4s ease,background .3s ease;}
.therm-bulb{width:44px;height:44px;border-radius:50%;background:var(--ok);border:2px solid var(--line);margin:-24px auto 0;position:relative;display:flex;align-items:center;justify-content:center;transition:background .3s ease;}
.therm-bulb span{color:#fff;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;}
.therm-wrap{display:flex;flex-direction:column;align-items:center;}
.readout{flex:1;}
.readout .value{font-family:'IBM Plex Mono',monospace;font-size:42px;font-weight:600;line-height:1;}
.readout .status{font-size:13px;font-weight:600;margin-top:6px;display:inline-block;padding:3px 10px;border-radius:20px;}
.status.ok{background:#E4EEE6;color:var(--ok);}
.status.bad{background:#FBE7DA;color:var(--clay);}
.status.none{background:var(--sage-pale);color:var(--sage);}
.range-note{font-size:12px;color:var(--ink-soft);margin-top:10px;}

form.entry-form{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;}
form.entry-form input,form.entry-form select{flex:1;min-width:90px;}
.btn{background:var(--teal);color:#fff;border:none;border-radius:8px;padding:9px 16px;font-size:14px;font-weight:600;cursor:pointer;font-family:'IBM Plex Sans',sans-serif;}
.btn:hover{background:var(--teal-deep);}
.btn.clay{background:var(--clay);}
.btn.clay:hover{background:#a94f21;}
.btn.ghost{background:none;border:1.5px solid var(--line);color:var(--ink-soft);}
.btn.ghost:hover{border-color:var(--teal);color:var(--teal);}

ul.log-list{list-style:none;margin:16px 0 0;padding:0;display:flex;flex-direction:column;gap:8px;max-height:220px;overflow:auto;}
ul.log-list li{display:flex;justify-content:space-between;align-items:center;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:8px 12px;font-size:13px;}
ul.log-list li .meta{color:var(--ink-soft);font-size:12px;}
ul.log-list li .del{background:none;border:none;color:var(--clay);cursor:pointer;font-size:13px;}
.empty{color:var(--sage);font-size:13px;font-style:italic;padding:10px 0;}

.tasks-panel{margin-top:20px;}
.task-row{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);}
.task-row:last-child{border-bottom:none;}
.task-row input[type=checkbox]{width:18px;height:18px;accent-color:var(--teal);}
.task-row.done label{text-decoration:line-through;color:var(--sage);}
.task-row label{flex:1;font-size:14px;}

.history{margin-top:20px;}
.history-controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;}
th{text-transform:uppercase;font-size:11px;letter-spacing:0.08em;color:var(--ink-soft);font-weight:600;background:var(--sage-pale);}
td.bad-cell{color:var(--clay);font-weight:600;}
.table-wrap{overflow-x:auto;}
footer{margin-top:30px;text-align:center;color:var(--sage);font-size:12px;}

/* login page */
.login-card{max-width:420px;margin:80px auto;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:32px;}
.login-card h1{font-family:'Fraunces',serif;font-size:26px;margin:0 0 6px;}
.login-card p{color:var(--ink-soft);font-size:14px;margin:0 0 20px;}
.login-card form{display:flex;flex-direction:column;gap:12px;}
.login-card .btn{width:100%;padding:11px;}
.error{background:#FBE7DA;color:var(--clay);padding:10px 12px;border-radius:8px;font-size:13px;margin-bottom:14px;}
.login-toggle{text-align:center;margin-top:16px;font-size:13px;color:var(--ink-soft);}
.login-toggle button{background:none;border:none;color:var(--teal);text-decoration:underline;cursor:pointer;font-size:13px;}

/* admin */
.admin-clinic-row{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--line);flex-wrap:wrap;}
.admin-clinic-row .name{flex:1;font-weight:600;min-width:140px;}
