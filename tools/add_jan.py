import sys,re,json
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
B=json.load(open('/home/claude/jan/jan_book.json',encoding='utf-8'))
m=re.search(r'const BOOKS=(\[.*?\]);\s*let CFG',s,re.S); BOOKS=json.loads(m.group(1))
BOOKS=[b for b in BOOKS if b['id']!='jan']+[B]
s=s[:m.start(1)]+json.dumps(BOOKS,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:60],s.count(a)); s=s.replace(a,b,1)
if 'function repPath(' not in s:
    rep("/^#(b|wp|pr|cs|ter|mcs)(\\d{1,4})$/","/^#(b|wp|pr|cs|ter|mcs|jan)(\\d{1,4})$/")
    rep("function memoHTML(p,wrong){","""function repPath(p){ const ch=[]; let q=p, guard=0; while(q&&guard++<200){ ch.unshift(...(q.pm||[])); q=(q.pp!==undefined)?ALL[q.pp]:null; }
  const g=new Chess(); const out=[]; for(const u of ch){ const t=g.turn(), n=Math.ceil((g.history().length+1)/2); const r=g.move({from:u.slice(0,2),to:u.slice(2,4),promotion:u[4]}); if(!r) break; out.push(t==='w'?n+'.'+r.san:(out.length?r.san:n+'…'+r.san)); } return out; }
function memoHTML(p,wrong){
  if(p.pm&&!p.c){ p.c='Как пришли: '+repPath(p).join(' ')+'. Ход по репертуару за чёрных.'; }""")
    rep("$('pzLabel').textContent=CFG.item+' '+(cur.lab||cur.n);","""$('pzLabel').textContent=CFG.item+' '+(cur.lab||cur.n);
  { const q=ALL[cur.n-1]; if(q&&q.pm&&q.pm.length){ const u=q.pm[q.pm.length-1]; lastMove={from:u.slice(0,2),to:u.slice(2,4)}; const pth=repPath(q); $('pzLabel').textContent=CFG.item+' '+(cur.lab||cur.n)+' · '+(pth.length>4?'… ':'')+pth.slice(-4).join(' '); } }""")
    rep("J. Hellsten «Mastering Chess Strategy».","J. Hellsten «Mastering Chess Strategy»; репертуар «Гамбит Яниша» — студия Serta_chess.")
open(f,'w',encoding='utf-8').write(s); print('ok',f,len(s))
