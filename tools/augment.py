import json,re,glob,chess,chess.pgn,sys
html=open(sys.argv[1],encoding='utf-8').read()
m=re.search(r'const BOOKS=(\[.*?\]);\s*let CFG',html,re.S)
BOOKS=json.loads(m.group(1))
def k(fen,mv): return ' '.join(fen.split()[:4])+'|'+mv
def clean(s):
    s=re.sub(r'Сначала найди план сам[^.]*\.','',s); s=re.sub(r'Дальше разыграй[^.]*\.','',s)
    s=re.sub(r'Оценка движка:[^.]*(\([^)]*\))?\.?','',s)
    return re.sub(r'\s+',' ',s).strip()
def load(files):
    idx={}
    for fn in files:
        f=open(fn,encoding='utf-8')
        while (g:=chess.pgn.read_game(f)):
            b=g.board(); mv=list(g.mainline_moves())
            if not mv: continue
            fen=b.fen(); ucis=[x.uci() for x in mv]
            com=[g.comment] if g.comment else []
            # collect mainline comments with ply index
            notes=[]
            for i,n in enumerate(g.mainline()):
                if n.comment and i<14: notes.append([i,clean(n.comment)])
            idx[k(fen,ucis[0])]={'x':ucis[:14],'c':clean(g.comment or ''),'nt':[n for n in notes if n[1]]}
    return idx
src={'wp':sorted(glob.glob('/home/claude/wp2/*.pgn')),'pr':sorted(glob.glob('/home/claude/gul/*.pgn')),
     'cs':sorted(glob.glob('/home/claude/cs4/out/*.pgn')),'ter':['/mnt/user-data/uploads/OneDrive/Рабочий стол/Книги/книги на рабочем/Terekhin_vse_pozicii (2).pgn']}
for B in BOOKS:
    idx=load(src[B['id']]); hit=0
    for p in B['data']:
        r=idx.get(k(p['fen'],p['m'][0]))
        if r:
            hit+=1
            if len(r['x'])>len(p['m']) and r['x'][:len(p['m'])]==p['m']: p['x']=r['x'][len(p['m']):]
            if r['c']: p['c']=r['c']
            if r['nt']: p['nt']=r['nt']
    print(B['id'],len(B['data']),'matched',hit, 'withtext',sum(1 for p in B['data'] if 'c' in p or 'nt' in p),file=sys.stderr)
new=json.dumps(BOOKS,ensure_ascii=False,separators=(',',':'))
html=html[:m.start(1)]+new+html[m.end(1):]
open(sys.argv[2],'w',encoding='utf-8').write(html)
