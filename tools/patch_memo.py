import sys,re
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:60],s.count(a)); s=s.replace(a,b)
css='''.card.wide{max-width:560px}
.memo{display:flex;flex-direction:column;gap:10px}
.memohead h2{font-size:20px;line-height:1.1}
.memobody{display:flex;flex-direction:column;align-items:center;gap:6px}
.mbwrap{width:min(100%,260px)}
.mb{display:grid;grid-template-columns:repeat(8,1fr);aspect-ratio:1;border-radius:4px;overflow:hidden;box-shadow:0 0 0 1px var(--line)}
.msq{position:relative}.msq.l{background:var(--sq-light)}.msq.d{background:var(--sq-dark)}
.msq.ml{box-shadow:inset 0 0 0 999px rgba(242,201,76,.45)}
.msq svg{position:absolute;inset:0;width:100%;height:100%}
.mctl{display:flex;align-items:center;gap:10px}
.btn.sm{padding:6px 14px;font-size:15px}
.mline{line-height:1.9;font-size:15px}
.mline .mn{color:var(--muted);font-variant-numeric:tabular-nums}
.mm{border:0;background:none;color:var(--ink);font:700 15px var(--font-body);padding:1px 4px;border-radius:5px;cursor:pointer}
.mm.key{color:var(--accent)}
.mm.on{background:var(--accent);color:var(--accent-ink)}
.msec{border-top:1px solid var(--line);padding-top:8px}
.msec b{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:3px}
.msec p{margin:0;line-height:1.45}
.faillist{display:flex;flex-wrap:wrap;gap:6px}
.faillist .chip{cursor:pointer}
.card.wide>#memoGo,.card.wide>.row2{position:sticky;bottom:0;box-shadow:0 10px 0 6px var(--panel),0 -6px 10px -2px var(--panel)}
'''
rep('.lbl{display:block;font-size:12px;color:var(--muted);margin-bottom:4px}', css+'.lbl{display:block;font-size:12px;color:var(--muted);margin-bottom:4px}')
rep("let opt={minutes:10, order:'seq', block:0};","let opt={minutes:10, order:'seq', block:0, review:'now'};")
memo=open('/home/claude/storm/memo.js',encoding='utf-8').read()
rep('function showStart(){', memo+'\nfunction showStart(){\n  card.classList.remove(\'wide\');')
# options chips
rep('''<button class="chip" type="button" data-v="seq">По порядку</button><button class="chip" type="button" data-v="rnd">Вперемешку</button></div></div>
    </div>''','''<button class="chip" type="button" data-v="seq">По порядку</button><button class="chip" type="button" data-v="rnd">Вперемешку</button></div></div>
    </div>
    <div><div class="lbl">Разбор нерешённой позиции</div><div class="opts" id="optRev">
      <button class="chip" type="button" data-v="now">Сразу, часы на паузе</button><button class="chip" type="button" data-v="end">После тренировки</button></div></div>''')
rep("""    card.querySelectorAll('#optOrd .chip').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.v===opt.order)));""","""    card.querySelectorAll('#optOrd .chip').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.v===opt.order)));
    card.querySelectorAll('#optRev .chip').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.v===opt.review)));""")
rep("""  card.querySelectorAll('#optOrd .chip').forEach(b=>b.onclick=()=>{opt.order=b.dataset.v;sync()});""","""  card.querySelectorAll('#optOrd .chip').forEach(b=>b.onclick=()=>{opt.order=b.dataset.v;sync()});
  card.querySelectorAll('#optRev .chip').forEach(b=>b.onclick=()=>{opt.review=b.dataset.v;store.set('chstorm_review',opt.review);sync()});""")
rep("""      <li>Серия решений добавляет время: 5 → +3 с, 12 → +5 с, 20 → +7 с.</li></ul>""","""      <li>Серия решений добавляет время: 5 → +3 с, 12 → +5 с, 20 → +7 с.</li>
      <li>Если позиция не решена, откроется памятка: полное решение, идея и план. Часы в это время стоят.</li></ul>""")
# mistake: second failure
rep("""  setTimeout(()=>{marks={};busy=false;nextPuzzle()},900);
}""","""  const P=ALL[cur.n-1]; S.fails=S.fails||[]; S.fails.push({n:cur.n,w:{from:mv.from,to:mv.to,promotion:mv.promotion}});
  if(opt.review==='now'&&P){
    setTimeout(()=>{ marks={}; S.paused=Date.now();
      openMemo(P,{from:mv.from,to:mv.to,promotion:mv.promotion},`<button class="btn" id="memoGo" type="button">Понятно, дальше</button>`);
      $('memoGo').onclick=()=>{ card.classList.remove('wide'); overlay.hidden=true; if(S.paused){S.end+=Date.now()-S.paused; S.paused=null;} busy=false; nextPuzzle(); requestAnimationFrame(tick); };
    },700);
    return;
  }
  setTimeout(()=>{marks={};busy=false;nextPuzzle()},900);
}""")
rep("""  if(!S||!S.running) return;
  const left=Math.max(0,S.end-Date.now());""","""  if(!S||!S.running) return;
  if(S.paused) return;
  const left=Math.max(0,S.end-Date.now());""")
rep("""  S.running=false; SND.end();""","""  if(S.paused){S.end+=Date.now()-S.paused; S.paused=null;} busy=false;
  S.running=false; SND.end();""")
# results card: wrap into function
rep("""  card.innerHTML=`<button class="xbtn" id="closeRes\"""","""  const fails=(S.fails||[]).filter((f,i,a)=>a.findIndex(x=>x.n===f.n)===i);
  const showRes=()=>{ card.classList.remove('wide');
  card.innerHTML=`<button class="xbtn" id="closeRes\"""")
rep("""    ${failed.length?`<div class="sub">Повторить: ${failed.join(', ')}</div>`:''}""","""    ${failed.length?`<div class="sub">Повторить: ${failed.join(', ')}</div>`:''}
    ${fails.length?`<button class="btn ghost" id="revBtn" type="button">Разбор ошибок (${fails.length})</button>`:''}""")
rep("""  $('closeRes').onclick=()=>{ overlay.hidden=true; $('resultsBtn').hidden=false; $('newBtn').hidden=false; };""","""  $('closeRes').onclick=()=>{ overlay.hidden=true; $('resultsBtn').hidden=false; $('newBtn').hidden=false; };
  if($('revBtn')) $('revBtn').onclick=()=>showList();
  $('report').textContent=txt; $('waBtn').href='https://wa.me/?text='+encodeURIComponent(txt);
  $('copyBtn').onclick=copyFn; };
  const showList=()=>{ card.classList.remove('wide');
    card.innerHTML=`<button class="xbtn" id="closeRes" type="button" aria-label="Назад">×</button><h2>Разбор ошибок</h2>
      <div class="sub">Нажмите на позицию, чтобы открыть памятку с решением, идеей и планом.</div>
      <div class="faillist">${fails.map((f,i)=>`<button class="chip" type="button" data-i="${i}">${CFG.item} ${ALL[f.n-1].lab||f.n}</button>`).join('')}</div>
      <button class="btn ghost" id="backRes" type="button">Назад к итогам</button>`;
    $('closeRes').onclick=showRes; $('backRes').onclick=showRes;
    card.querySelectorAll('.faillist .chip').forEach(b=>b.onclick=()=>{ const i=+b.dataset.i; const f=fails[i];
      openMemo(ALL[f.n-1],f.w,`<div class="row2">${i+1<fails.length?`<button class="btn" id="mNextPos" type="button">Следующая ошибка</button>`:'<span></span>'}<button class="btn ghost" id="mBack" type="button">К списку</button></div>`);
      $('mBack').onclick=showList; if($('mNextPos')) $('mNextPos').onclick=()=>{ showList(); card.querySelectorAll('.faillist .chip')[i+1].click(); }; }); };""")
# move report building before showRes call: original code sets report etc after; convert
rep("""  $('report').textContent=txt;
  $('waBtn').href='https://wa.me/?text='+encodeURIComponent(txt);
  $('copyBtn').onclick=async()=>{""","""  const copyFn=async()=>{""")
rep("""$('copyBtn').textContent='Выделено, нажмите «Копировать»'; } };
}""","""$('copyBtn').textContent='Выделено, нажмите «Копировать»'; } };
  showRes();
}""")
# report text: add note about reviewed
rep("""  S={running:true,queue,idx:0,""","""  S={running:true,fails:[],queue,idx:0,""")
rep("""let opt={minutes:10, order:'seq', block:0, review:'now'};""","""let opt={minutes:10, order:'seq', block:0, review:'now'}; try{ if(localStorage.getItem('chstorm_review')==='end') opt.review='end'; }catch(e){}""")
open(f,'w',encoding='utf-8').write(s); print('ok',f)
