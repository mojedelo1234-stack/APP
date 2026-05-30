<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Today</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
  html,body{min-height:100%;background:#111111;color:#f0f0f0;font-family:'Inter',sans-serif}
  .wrap{max-width:540px;margin:0 auto;padding:48px 24px 80px}
  .top{margin-bottom:40px}
  .date{font-size:13px;color:#888;letter-spacing:.04em;margin-bottom:8px}
  .title{font-family:'Bebas Neue',sans-serif;font-size:64px;letter-spacing:.05em;line-height:1;color:#ffffff}
  .prog-wrap{margin-bottom:48px}
  .prog-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
  .prog-label{font-size:12px;color:#666;letter-spacing:.08em;font-weight:500}
  .prog-pct{font-family:'Bebas Neue',sans-serif;font-size:28px;color:#ffffff}
  .prog-track{height:3px;background:#2a2a2a;border-radius:3px}
  .prog-fill{height:100%;background:#ffffff;border-radius:3px;transition:width .4s}
  .section-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}
  .section-name{font-size:12px;letter-spacing:.12em;color:#ffffff;font-weight:600}
  .section-count{font-size:12px;color:#666;font-weight:400}
  .goal-row{display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid #1e1e1e;cursor:pointer;user-select:none;transition:opacity .15s}
  .goal-row:active{opacity:.5}
  .goal-row:last-child{border-bottom:none}
  .goal-row.done .goal-text{color:#444;text-decoration:line-through}
  .goal-row.done .check-box{background:#ffffff;border-color:#ffffff}
  .goal-row.done .check-box svg{opacity:1}
  .check-box{width:26px;height:26px;border:1.5px solid #444;border-radius:6px;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all .15s}
  .check-box svg{width:14px;height:14px;opacity:0;transition:opacity .15s}
  .goal-text{font-size:16px;font-weight:400;flex:1;line-height:1.5;color:#e8e8e8;word-break:break-word}
  .goal-actions{display:flex;gap:4px;opacity:0;transition:opacity .15s}
  .goal-row:hover .goal-actions{opacity:1}
  .action-btn{background:none;border:none;color:#444;cursor:pointer;padding:6px;font-size:16px;line-height:1;flex-shrink:0;transition:color .15s;display:flex;align-items:center;justify-content:center}
  .action-btn:hover{color:#fff}
  .action-btn.delete:hover{color:#8b5a5a}
  .empty{font-size:13px;color:#444;padding:16px 0;font-style:italic}
  .add-row{display:flex;align-items:center;gap:12px;margin-top:12px;padding:14px 0;border-bottom:1px solid #1e1e1e}
  .add-input{background:none;border:none;padding:0;color:#f0f0f0;font-family:'Inter',sans-serif;font-size:16px;font-weight:300;flex:1;outline:none}
  .add-input::placeholder{color:#444}
  .add-btn{background:#ffffff;border:none;border-radius:8px;color:#111;cursor:pointer;width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;transition:all .15s}
  .add-btn:active{background:#ccc}
  .add-btn svg{width:18px;height:18px}
  .divider{height:1px;background:#1e1e1e;margin:40px 0}
  .loading{text-align:center;font-size:13px;color:#555;padding:40px 0}
  .toast{position:fixed;bottom:36px;left:50%;transform:translateX(-50%);background:#222;border:1px solid #333;border-radius:8px;padding:12px 24px;font-size:13px;color:#ccc;opacity:0;transition:opacity .3s;pointer-events:none;white-space:nowrap;z-index:99}
  .toast.show{opacity:1}
  .edit-input{background:transparent;border:none;border-bottom:1px solid #555;color:#e8e8e8;font-family:'Inter',sans-serif;font-size:16px;flex:1;outline:none;padding:2px 0}
  .goal-row.editing .goal-actions{opacity:1}
  @media(max-width:480px){.goal-actions{opacity:1}}
</style>
<base target="_blank">
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="date" id="top-date"></div>
    <div class="title">Today</div>
  </div>
  <div class="prog-wrap">
    <div class="prog-meta">
      <span class="prog-label">PROGRESS</span>
      <span class="prog-pct" id="prog-pct">0%</span>
    </div>
    <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
  </div>
  <div id="app-content"></div>
</div>
<div class="toast" id="toast"></div>

<script>
const STORAGE_KEY = 'today_app_v1';

function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return getDefaultData();
    const data = JSON.parse(raw);
    const today = new Date().toDateString();
    if (data.lastDate !== today) {
      data.daily.forEach(g => g.done = false);
      data.lastDate = today;
      saveData(data);
    }
    return data;
  } catch {
    return getDefaultData();
  }
}

function getDefaultData() {
  return { daily: [], todo: [], lastDate: new Date().toDateString() };
}

function saveData(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

let data = loadData();

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

function genId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

function addGoal(type) {
  const inp = document.getElementById(type + '-input');
  const v = inp.value.trim();
  if (!v) return;
  inp.value = '';
  const goal = { id: genId(), text: v, done: false, created: Date.now() };
  data[type].push(goal);
  saveData(data);
  render();
  inp.focus();
}

function toggle(id) {
  const g = data.daily.find(x => x.id === id) || data.todo.find(x => x.id === id);
  if (!g) return;
  g.done = !g.done;
  saveData(data);
  render();
  if (g.type === 'todo' && g.done) {
    setTimeout(() => {
      data.todo = data.todo.filter(x => x.id !== id);
      saveData(data);
      render();
    }, 400);
  }
}

function del(id) {
  data.daily = data.daily.filter(x => x.id !== id);
  data.todo = data.todo.filter(x => x.id !== id);
  saveData(data);
  render();
}

function startEdit(id) {
  const g = data.daily.find(x => x.id === id) || data.todo.find(x => x.id === id);
  if (!g) return;
  const row = document.getElementById('goal-' + id);
  if (row.classList.contains('editing')) return;
  row.classList.add('editing');
  const textSpan = row.querySelector('.goal-text');
  const actions = row.querySelector('.goal-actions');
  const orig = g.text;
  const input = document.createElement('input');
  input.type = 'text';
  input.className = 'edit-input';
  input.value = orig;
  textSpan.replaceWith(input);
  actions.style.opacity = '1';
  input.focus();
  input.select();
  function finish(save) {
    const nv = input.value.trim();
    if (save && nv && nv !== orig) {
      g.text = nv;
      saveData(data);
    }
    render();
  }
  input.addEventListener('blur', () => finish(true));
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') input.blur();
    if (e.key === 'Escape') { input.value = orig; input.blur(); }
  });
}

function render() {
  const daily = data.daily;
  const todos = data.todo;
  const all = [...daily, ...todos];
  const done = all.filter(g => g.done).length;
  const pct = all.length ? Math.round(done / all.length * 100) : 0;
  document.getElementById('prog-fill').style.width = pct + '%';
  document.getElementById('prog-pct').textContent = pct + '%';
  const dc = daily.filter(g => g.done).length;
  const tc = todos.filter(g => g.done).length;
  document.getElementById('app-content').innerHTML = `
    <div class="section-header"><span class="section-name">DAILY</span><span class="section-count">${dc}/${daily.length}</span></div>
    <div id="daily-list">${renderList(daily, 'daily')}</div>
    <div class="add-row">
      <input class="add-input" id="daily-input" placeholder="add a daily goal..." autocomplete="off" />
      <button class="add-btn" onclick="addGoal('daily')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </button>
    </div>
    <div class="divider"></div>
    <div class="section-header"><span class="section-name">TO DO</span><span class="section-count">${tc}/${todos.length}</span></div>
    <div id="todo-list">${renderList(todos, 'todo')}</div>
    <div class="add-row">
      <input class="add-input" id="todo-input" placeholder="add a one-off task..." autocomplete="off" />
      <button class="add-btn" onclick="addGoal('todo')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </button>
    </div>
  `;
  document.getElementById('daily-input').addEventListener('keydown', e => { if (e.key === 'Enter') addGoal('daily'); });
  document.getElementById('todo-input').addEventListener('keydown', e => { if (e.key === 'Enter') addGoal('todo'); });
}

function renderList(list, type) {
  if (!list.length) return '<div class="empty">nothing here yet</div>';
  return list.map(g => {
    g.type = type;
    return `<div class="goal-row${g.done ? ' done' : ''}" id="goal-${g.id}">
      <div class="check-box" onclick="toggle('${g.id}')"><svg viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg></div>
      <span class="goal-text" onclick="toggle('${g.id}')">${g.text}</span>
      <div class="goal-actions">
        <button class="action-btn" onclick="event.stopPropagation();startEdit('${g.id}')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        </button>
        <button class="action-btn delete" onclick="event.stopPropagation();del('${g.id}')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
      </div>
    </div>`;
  }).join('');
}

const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const now = new Date();
document.getElementById('top-date').textContent = days[now.getDay()] + ' · ' + months[now.getMonth()] + ' ' + now.getDate();

render();

setInterval(() => {
  const today = new Date().toDateString();
  if (data.lastDate !== today) {
    data.daily.forEach(g => g.done = false);
    data.lastDate = today;
    saveData(data);
    render();
    const n = new Date();
    document.getElementById('top-date').textContent = days[n.getDay()] + ' · ' + months[n.getMonth()] + ' ' + n.getDate();
  }
}, 60000);
</script>
</body>
</html>
