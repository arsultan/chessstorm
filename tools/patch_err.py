import sys

HELPERS = r"""let ERRQ=null;
function errKey(){ return 'chstorm_err_'+CFG.id+'_'+String(store.get('chstorm_name')||opt.name||'').trim().toLowerCase(); }
function errLoad(){ try{ return JSON.parse(store.get(errKey())||'[]')||[]; }catch(e){ return []; } }
function errSave(a){ store.set(errKey(), JSON.stringify(a.slice(-400))); }
function errAdd(q,w){ if(!q||CFG.rep) return; const a=errLoad().filter(x=>x.f!==q.fen); a.push({f:q.fen,w:w,d:Date.now()}); errSave(a); }
function errDel(q){ if(!q) return; const a=errLoad(); const b=a.filter(x=>x.f!==q.fen); if(b.length!==a.length) errSave(b); }
function errList(){ return errLoad().map(e=>({e:e,i:ALL.findIndex(q=>q.fen===e.f)})).filter(x=>x.i>=0); }
function showErrList(){ const L=errList(); card.classList.remove('wide');
  card.innerHTML=`<div class="cardhead"><div style="flex:1;min-width:0"><h2>Мои ошибки</h2><div class="sub">${CFG.short} · ${L.length} поз. Позиция уходит из списка, когда вы её решите.</div></div></div>
    ${L.length?`<div class="faillist">${L.map((x,k)=>`<button class="chip" type="button" data-k="${k}">${CFG.item} ${ALL[x.i].lab||ALL[x.i].n}</button>`).join('')}</div>
    <button class="btn" id="errPlay2" type="button">Решать эти позиции заново</button>`:'<p class="sub">Ошибок нет.</p>'}
    <button class="btn ghost" id="errBack" type="button">Назад</button>`;
  overlay.hidden=false;
  $('errBack').onclick=()=>showStart();
  if($('errPlay2')) $('errPlay2').onclick=()=>{ ERRQ=errList().map(x=>ALL[x.i]); showStart(); $('startBtn').click(); };
  card.querySelectorAll('.faillist .chip').forEach(b=>b.onclick=()=>{ const x=L[+b.dataset.k];
    openMemo(ALL[x.i],x.e.w,`<div class="row2"><button class="btn ghost" id="mBack" type="button">К списку ошибок</button></div>`);
    $('mBack').onclick=()=>showErrList(); });
}
function start(){"""

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'function errAdd' in s:
        print('skip', f); continue
    a = "function start(){\n  const queue=PUZ.slice();"
    assert a in s
    s = s.replace(a, HELPERS + "\n  const queue=(ERRQ||PUZ).slice(); ERRQ=null;", 1)
    b = "S.fails.push({n:cur.n,w:{from:mv.from,to:mv.to,promotion:mv.promotion}});"
    assert b in s
    s = s.replace(b, b + " errAdd(P,{from:mv.from,to:mv.to,promotion:mv.promotion});", 1)
    c = "function solved(){\n"
    assert c in s
    s = s.replace(c, c + "  errDel(ALL[cur.n-1]);\n", 1)
    d = '    <p id="nameErr" class="err-msg" hidden>'
    assert d in s
    s = s.replace(d, '    <div id="errBox"></div>\n' + d, 1)
    e = "  if(ci) ci.addEventListener('input',()=>{ci.classList.remove('bad'); $('codeErr').hidden=true});"
    assert e in s
    s = s.replace(e, e + """
  { const L=errList(); const box=$('errBox'); if(box&&L.length&&!CFG.rep){ box.innerHTML=`<div class="lbl">Мои ошибки в этой книге: ${L.length}</div><div class="opts"><button class="chip" id="errView" type="button">Посмотреть</button><button class="chip" id="errPlay" type="button">Решать заново</button></div>`;
    $('errView').onclick=()=>{ store.set('chstorm_name', nm.value.trim()||store.get('chstorm_name')||''); showErrList(); };
    $('errPlay').onclick=()=>{ ERRQ=errList().map(x=>ALL[x.i]); $('startBtn').click(); }; } }""", 1)
    open(f, 'w', encoding='utf-8').write(s)
    print('ok', f)
