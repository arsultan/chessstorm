import json,re,glob,io,sys,chess,chess.pgn
def k(fen,mv): return ' '.join(fen.split()[:4])+'|'+mv
FULL={}
def add_files(files):
    for fn in files:
        f=open(fn,encoding='utf-8')
        while (g:=chess.pgn.read_game(f)):
            u=[m.uci() for m in g.mainline_moves()]
            if u: FULL.setdefault(k(g.board().fen(),u[0]),u)
add_files(sorted(glob.glob('/home/claude/wp2/*.pgn'))+sorted(glob.glob('/home/claude/gul/*.pgn'))+sorted(glob.glob('/home/claude/cs4/out/*.pgn')))
# MCS + Kaselas: use their processed game lists
sys.argv=['x']
ns={}
src=open('/home/claude/mcs/build.py').read().split("f=open('all.pgn')")[0]
import os
os.chdir('/home/claude/mcs'); exec(src,ns)
f=open('/home/claude/mcs/all.pgn')
while (g:=chess.pgn.read_game(f)):
    if not g.headers.get('FEN'): continue
    ns['fixnull'](g); ns['dedup'](g)
    u=[m.uci() for m in g.mainline_moves()]
    if u: FULL.setdefault(k(g.headers['FEN'],u[0]),u)
os.chdir('/home/claude/kas'); ns2={}
exec(open('/home/claude/kas/build.py').read().split("groups=[")[0],ns2)
for i,s,g in ns2['games']:
    u=[m.uci() for m in g.mainline_moves()]
    if u and g.headers.get('FEN'): FULL.setdefault(k(g.headers['FEN'],u[0]),u)
print('lines',len(FULL),file=sys.stderr)
for f in sys.argv_files if False else []: pass
def apply(path):
    s=open(path,encoding='utf-8').read()
    m=re.search(r'const BOOKS=(\[.*?\]);\s*let CFG',s,re.S); BOOKS=json.loads(m.group(1))
    for b in BOOKS:
        if b['id'] not in ('wp','pr','cs','mcs','kas'): continue
        hit=miss=0
        for p in b['data']:
            u=FULL.get(k(p['fen'],p['m'][0]))
            if u and u[:len(p['m'])]==p['m']:
                p['m']=u; p.pop('x',None); hit+=1
            else:
                p['m']=p['m']+p.get('x',[]); p.pop('x',None); miss+=1
        b['full']=1; b['mate']=1
        print(path.split('/')[-1],b['id'],'hit',hit,'miss',miss,file=sys.stderr)
    s=s[:m.start(1)]+json.dumps(BOOKS,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
    open(path,'w',encoding='utf-8').write(s)
for p in ['/home/claude/storm/hub/chess-storm.html','/home/claude/storm/woodpecker-storm.html','/home/claude/storm/woodpecker_storm.html','/home/claude/storm/terekhin-storm.html']: apply(p)
