import sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
if 'function fmtPath(' not in s:
    old_s=s.index('function repPath(p){'); old_e=s.index('function memoHTML(p,wrong){')
    s=s[:old_s]+"""function repPath(p){ const ch=[]; let q=p, guard=0; while(q&&guard++<200){ ch.unshift(...(q.pm||[])); q=(q.pp!==undefined)?ALL[q.pp]:null; }
  const g=new Chess(); const out=[]; for(const u of ch){ const t=g.turn(), n=Math.ceil((g.history().length+1)/2); const r=g.move({from:u.slice(0,2),to:u.slice(2,4),promotion:u[4]}); if(!r) break; out.push({w:t==='w',n,s:r.san}); } return out; }
function fmtPath(a){ return a.map((x,i)=>x.w?x.n+'.'+x.s:(i===0?x.n+'…'+x.s:x.s)).join(' '); }
"""+s[old_e:]
    s=s.replace("p.c='Как пришли: '+repPath(p).join(' ')+","p.c='Как пришли: '+fmtPath(repPath(p))+",1)
    s=s.replace("(pth.length>4?'… ':'')+pth.slice(-4).join(' ')","fmtPath(pth.slice(-4))",1)
s=s.replace("(pth.length>4?'… ':'')+fmtPath(pth.slice(-4))","fmtPath(pth.slice(-4))",1)
s=s.replace("!/все|Вся/.test(b.name)","!/^(все|вся)/i.test(b.name)",1)
s=s.replace("${p.c?`<div class=\"msec\"><b>Из книги</b>","${p.c?`<div class=\"msec\"><b>${CFG.rep?'Линия':'Из книги'}</b>",1)
open(f,'w',encoding='utf-8').write(s); print('ok',f, s.count('fmtPath'), "CFG.rep?'Линия'" in s)
