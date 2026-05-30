<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Today</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
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
  .goal-row.done .check-box i{color:#111}
  .check-box{width:26px;height:26px;border:1.5px solid #444;border-radius:6px;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all .15s}
  .check-box i{font-size:15px;color:transparent}
  .goal-text{font-size:16px;font-weight:400;flex:1;line-height:1.5;color:#e8e8e8}
  .del-btn{background:none;border:none;color:#444;cursor:pointer;padding:8px;font-size:18px;line-height:1;flex-shrink:0;transition:color .15s}
  .del-btn:active{color:#fff}
  .empty{font-size:13px;color:#444;padding:16px 0;font-style:italic}
  .add-row{display:flex;align-items:center;gap:12px;margin-top:12px;padding:14px 0;border-bottom:1px solid #1e1e1e}
  .add-input{background:none;border:none;padding:0;color:#f0f0f0;font-family:'Inter',sans-serif;font-size:16px;font-weight:300;flex:1;outline:none}
  .add-input::placeholder{color:#444}
  .add-btn{background:#ffffff;border:none;border-radius:8px;color:#111;cursor:pointer;width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;transition:all .15s}
  .add-btn:active{background:#ccc}
  .divider{height:1px;background:#1e1e1e;margin:40px 0}
  .loading{text-align:center;font-size:13px;color:#555;padding:40px 0}
  .toast{position:fixed;bottom:36px;left:50%;transform:translateX(-50%);background:#222;border:1px solid #333;border-radius:8px;padding:12px 24px;font-size:13px;color:#ccc;opacity:0;transition:opacity .3s;pointer-events:none;white-space:nowrap;z-index:99}
  .toast.show{opacity:1}
</style>
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
  <div id="app-content">
    <div class="loading">loading...</div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
let goals=[];
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000);}
async function loadGoals(){try{const res=await fetch('/api/goals');goals=await res.json();render();}catch(e){document.getElementById('app-content').innerHTML='<div class="loading">could not connect</div>';}}
async function addGoal(type){const inp=document.getElementById(type+'-input');const v=inp.value.trim();if(!v)return;inp.value='';try{const res=await fetch('/api/goals',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:v,type})});const goal=await res.json();goals.push(goal);render();}catch{toast('error saving');}}
async function toggle(id){const g=goals.find(x=>x.id===id);if(!g)return;g.done=g.done?0:1;render();try{await fetch('/api/goals/'+id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({done:g.done})});if(g.type==='todo'&&g.done){setTimeout(async()=>{await fetch('/api/goals/'+id,{method:'DELETE'});goals=goals.filter(x=>x.id!==id);render();},500);}}catch{toast('error saving');}}
async function del(id){goals=goals.filter(x=>x.id!==id);render();try{await fetch('/api/goals/'+id,{method:'DELETE'});}catch{toast('error deleting');}}
function render(){
  const daily=goals.filter(g=>g.type==='daily');
  const todos=goals.filter(g=>g.type==='todo');
  const allDone=goals.filter(g=>g.done).length;
  const pct=goals.length?Math.round(allDone/goals.length*100):0;
  document.getElementById('prog-fill').style.width=pct+'%';
  document.getElementById('prog-pct').textContent=pct+'%';
  const dc=daily.filter(g=>g.done).length;
  const tc=todos.filter(g=>g.done).length;
  document.getElementById('app-content').innerHTML=`
    <div class="section-header"><span class="section-name">DAILY</span><span class="section-count">${dc}/${daily.length}</span></div>
    <div id="daily-list">${renderList(daily,'daily')}</div>
    <div class="add-row"><input class="add-input" id="daily-input" placeholder="add a daily goal..." /><button class="add-btn" onclick="addGoal('daily')"><i class="ti ti-plus"></i></button></div>
    <div class="divider"></div>
    <div class="section-header"><span class="section-name">TO DO</span><span class="section-count">${tc}/${todos.length}</span></div>
    <div id="todo-list">${renderList(todos,'todo')}</div>
    <div class="add-row"><input class="add-input" id="todo-input" placeholder="add a one-off task..." /><button class="add-btn" onclick="addGoal('todo')"><i class="ti ti-plus"></i></button></div>
  `;
  document.getElementById('daily-input').addEventListener('keydown',e=>{if(e.key==='Enter')addGoal('daily');});
  document.getElementById('todo-input').addEventListener('keydown',e=>{if(e.key==='Enter')addGoal('todo');});
}
function renderList(list,type){
  if(!list.length)return '<div class="empty">nothing here yet</div>';
  return list.map(g=>`<div class="goal-row${g.done?' done':''}" id="goal-${g.id}"><div class="check-box" onclick="toggle(${g.id})"><i class="ti ti-check"></i></div><span class="goal-text" onclick="toggle(${g.id})">${g.text}</span><button class="del-btn" onclick="del(${g.id})"><i class="ti ti-x"></i></button></div>`).join('');
}
const days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const now=new Date();
document.getElementById('top-date').textContent=days[now.getDay()]+' · '+months[now.getMonth()]+' '+now.getDate();
loadGoals();
</script>
</body>
</html>
