import sys
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    a="cur={n:cur.n,fen:cur.fen,m:CFG.full?cur.m.slice():cur.m.slice(0,3)};"
    if 'a:cur.a' not in s:
        assert a in s; s=s.replace(a,"cur={n:cur.n,fen:cur.fen,m:CFG.full?cur.m.slice():cur.m.slice(0,3),a:cur.a};")
    b="  if(uci===exp || (exp&&exp.length===4&&uci.slice(0,4)===exp)){\n    const r1=game.move({from:mv.from,to:mv.to,promotion:promo});"
    if 'altOk' not in s:
        assert b in s
        s=s.replace(b,"""  const altOk=!!(exp&&cur.a&&cur.a[step]&&cur.a[step].includes(uci.slice(0,4))&&uci.slice(0,4)!==exp.slice(0,4));
  if(altOk){ const d=$('delta'); if(d){ d.textContent='Тоже верно! Основной вариант:'; d.className='delta plus'; clearTimeout(showDelta.t); showDelta.t=setTimeout(()=>{d.textContent='';},1800);} mv={from:exp.slice(0,2),to:exp.slice(2,4),promotion:exp[4]}; promo=exp[4]||undefined; }
  if(altOk || uci===exp || (exp&&exp.length===4&&uci.slice(0,4)===exp)){
    const r1=game.move({from:mv.from,to:mv.to,promotion:promo});""")
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
