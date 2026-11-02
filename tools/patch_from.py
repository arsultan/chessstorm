import sys
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'fromIn' in s: print('skip',f); continue
    a='    <div><div class="lbl">Разбор нерешённой позиции</div>'
    assert a in s
    s=s.replace(a,'''    <div><label class="lbl" for="fromIn">Начать с позиции (номер из книги)</label>
      <input id="fromIn" class="field" type="number" inputmode="numeric" min="1" placeholder="с начала раздела"></div>
'''+a,1)
    b="  const queue=(ERRQ||PUZ).slice(); ERRQ=null;"
    assert b in s
    s=s.replace(b,"""  let base=PUZ; const fr=parseInt(opt.from,10);
  if(!ERRQ && fr>0){ const num=q=>parseInt(q.lab||q.n,10)||0; let k=PUZ.findIndex(q=>num(q)>=fr);
    if(k<0){ const j=ALL.findIndex(q=>num(q)>=fr); base=j>=0?ALL.slice(j):PUZ; } else base=PUZ.slice(k); }
  const queue=(ERRQ||base).slice(); ERRQ=null;""",1)
    c="  $('startBtn').onclick=async()=>{ const v=nm.value.trim();"
    assert c in s
    s=s.replace(c,"""  const fi=$('fromIn'); if(fi){ fi.value=store.get('chstorm_from_'+CFG.id+'_'+opt.block)||''; opt.from=fi.value; fi.oninput=()=>{ opt.from=fi.value.trim(); store.set('chstorm_from_'+CFG.id+'_'+opt.block,opt.from); }; }
"""+c,1)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
