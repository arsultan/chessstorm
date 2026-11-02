import sys
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    if b in s: return
    assert s.count(a)==1,(a[:50],s.count(a)); s=s.replace(a,b,1)
rep("cur={n:cur.n,fen:cur.fen,m:cur.m.slice(0,3)}","cur={n:cur.n,fen:cur.fen,m:CFG.full?cur.m.slice():cur.m.slice(0,3)}")
rep("""function tryMove(mv){
  const exp=cur.m[step];""","""function tryMove(mv){
  const exp=cur.m[step];
  if(CFG.mate){ const t=new Chess(game.fen()); const tr=t.move({from:mv.from,to:mv.to,promotion:mv.promotion?'q':undefined}); if(tr&&t.in_checkmate()){ selected=null; legal=[]; const r0=game.move({from:mv.from,to:mv.to,promotion:mv.promotion?'q':undefined}); (r0&&r0.captured?SND.capture:SND.move)(); lastMove={from:mv.from,to:mv.to}; step=cur.m.length; render(); solved(); return; } }""")
open(f,'w',encoding='utf-8').write(s); print('ok',f)
