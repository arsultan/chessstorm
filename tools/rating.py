import sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    if b in s: return
    assert s.count(a)==1,(a[:60],s.count(a),f); s=s.replace(a,b,1)
rep('.stat{border-top:1px solid var(--line);padding-top:8px}','''.stat{border-top:1px solid var(--line);padding-top:8px}
.rtbox{display:flex;align-items:baseline;gap:8px;border-top:1px solid var(--line);padding-top:8px;margin-top:2px}
.rtbox b{font:800 26px/1 var(--font-display);font-variant-numeric:tabular-nums}
.rtbox .lbl{margin:0}
.rtd{font:700 14px var(--font-body);font-variant-numeric:tabular-nums}
.rtd.up{color:var(--good)} .rtd.down{color:var(--bad)}''')
rep('''      <div class="stat"><b id="sBest">—</b><span>Рекорд</span></div>
    </div>''','''      <div class="stat"><b id="sBest">—</b><span>Рекорд</span></div>
    </div>
    <div class="rtbox" id="rtBox"><span class="lbl">Рейтинг</span><b id="sRt">—</b><span class="rtd" id="sRtD"></span></div>''')
# rating logic
rep("function solved(){","""const RBASE={wp:1750,pr:1550,cs:1550,ter:1650,mcs:1850,kas:1800,m3:1500,m5:1750};
function rKey(){ return 'chstorm_rating_'+String(opt.name||'').trim().toLowerCase(); }
function prat(q){ const mv=Math.ceil((q.m||[]).length/2); return (RBASE[CFG.id]||1600)+Math.min(300,60*Math.max(0,mv-1)); }
function rLoad(){ const v=parseFloat(store.get(rKey())); return isFinite(v)?v:1500; }
function rShow(){ const el=$('sRt'), d=$('sRtD'); if(!el) return; if(CFG.rep){ el.textContent='—'; d.textContent='дебют, без рейтинга'; d.className='rtd'; return; }
  const r=S&&S.rt?S.rt.r:rLoad(); el.textContent=Math.round(r); if(S&&S.rt){ const dd=Math.round(S.rt.r-S.rt.r0); d.textContent=dd?(dd>0?'▲ +':'▼ ')+dd:''; d.className='rtd '+(dd>0?'up':dd<0?'down':''); } else { d.textContent=''; } }
function rUpdate(score){ if(CFG.rep||!S||!S.rt) return; const q=ALL[cur.n-1]; if(!q) return; const pr=prat(q); const E=1/(1+Math.pow(10,(pr-S.rt.r)/400)); const K=S.rt.n<20&&S.rt.r0===1500?32:20; S.rt.r=Math.max(400,S.rt.r+K*(score-E)); S.rt.n++; store.set(rKey(),String(Math.round(S.rt.r*10)/10)); rShow(); }
function solved(){
  rUpdate(cur.tried?0.5:1);""")
rep("SND.bad(); S.mist++;","rUpdate(0); SND.bad(); S.mist++;")
rep("S={running:true,fails:[],queue","S={running:true,rt:(()=>{const r=rLoad(); return {r,r0:r,n:0};})(),fails:[],queue")
rep("updateStats(); nextPuzzle(); tick();","updateStats(); rShow(); nextPuzzle(); tick();")
rep('ошибок ${S.mist} · серия ${S.bestCombo}','ошибок ${S.mist} · серия ${S.bestCombo}${(!CFG.rep&&S.rt)?` · рейтинг ${Math.round(S.rt.r0)} → ${Math.round(S.rt.r)}`:""}')
rep("Лучшая серия: ${S.bestCombo}","Лучшая серия: ${S.bestCombo}${(!CFG.rep&&S.rt)?`\\nРейтинг: ${Math.round(S.rt.r0)} → ${Math.round(S.rt.r)} (${Math.round(S.rt.r-S.rt.r0)>=0?'+':''}${Math.round(S.rt.r-S.rt.r0)})`:''}")
open(f,'w',encoding='utf-8').write(s); print('ok',f)
