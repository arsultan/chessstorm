import json,chess,chess.pgn,io,glob,collections
D='/home/claude/deb/'
p=json.load(open(D+'plan2.json'))
ids={int(l.split()[0]):l.split()[1] for l in open(D+'ids2.txt') if l.strip()}
NS=128
def key(b): return ' '.join(b.fen().split(' ')[:3])
def shard(k):
    h=0
    for c in k: h=(h*31+ord(c))&0xffffffff
    return h%NS
E=collections.defaultdict(dict)   # key -> {san: {rep: code}}  code=ci*1000+ply
CH=json.load(open(D+'chapters.json'))
ORD=collections.defaultdict(dict) # key-> san -> first order
def walk(node,b,ri,ci,ply,ml,mlp):
    k=key(b)
    for j,v in enumerate(node.variations):
        san=b.san(v.move); onml=ml and j==0; lp=ply+1 if onml else mlp
        d=E[k].setdefault(san,{}); code=ci*1000+lp
        if ri not in d or (d[ri]%1000!=ply+1 and onml): d[ri]=code
        b.push(v.move); walk(v,b,ri,ci,ply+1,onml,lp); b.pop()
for ri,x in enumerate(p):
    f=open(D+x['file'],encoding='utf-8')
    ci=0
    while (g:=chess.pgn.read_game(f)):
        walk(g,g.board(),ri,ci,0,True,0); ci+=1
# leaf positions: record reps that end there
LEAF=collections.defaultdict(set)
SH=[{} for _ in range(NS)]
for k,mv in E.items():
    SH[shard(k)][k]=sorted([[s,sorted(r),[r[i] for i in sorted(r)]] for s,r in mv.items()],key=lambda t:-len(t[1]))
for i,s in enumerate(SH):
    json.dump(s,open(D+f'tree/d/{i}.json','w'),ensure_ascii=False,separators=(',',':'))
# opening names
names={}
for x in 'abcde':
    for l in list(open(f'/tmp/claude-0/-home-claude/ecbdfa50-d81d-5734-9f96-d53922eea4e4/scratchpad/eco/{x}.tsv'))[1:]:
        eco,nm,pg=l.rstrip('\n').split('\t')
        g=chess.pgn.read_game(io.StringIO(pg)); b=g.end().board()
        names[key(b)]=eco+' '+nm
reps=[{'name':x['name'],'side':x['orient'][0],'study':ids.get(i+1),'chs':CH[i],'ch':x['cnt']} for i,x in enumerate(p)]
json.dump({'reps':reps,'names':names,'ns':NS},open(D+'tree/meta.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(E),sum(len(v) for v in E.values()))

# ---- v2 layout: core (min depth<=CD) + per-repertoire files for deeper positions
import os,shutil
CD=10
start=key(chess.Board()); depth={start:0}; q=[start]; FEN={start:chess.Board()}
for k in q:
    if depth[k]>=CD+1: continue
    b0=FEN[k]
    for san in E.get(k,{}):
        b=b0.copy()
        try: b.push_san(san)
        except Exception: continue
        k2=key(b)
        if k2 not in depth: depth[k2]=depth[k]+1; q.append(k2); FEN[k2]=b
def ent(k): return sorted([[s,sorted(r),[r[i] for i in sorted(r)]] for s,r in E[k].items()],key=lambda t:-len(t[1]))
core={k:ent(k) for k in E if depth.get(k,99)<=CD}
RF=collections.defaultdict(dict)
# child positions of r-edges with depth>CD go to file r
for k,mv in E.items():
    for san,rs in mv.items():
        pass
# need child keys: recompute by walking games again
def walk2(node,b,ri):
    for v in node.variations:
        b.push(v.move); k2=key(b)
        if depth.get(k2,99)>CD and k2 in E: RF[ri][k2]=1
        walk2(v,b,ri); b.pop()
for ri,x in enumerate(p):
    f=open(D+x['file'],encoding='utf-8')
    while (g:=chess.pgn.read_game(f)): walk2(g,g.board(),ri)
shutil.rmtree(D+'tree/r',ignore_errors=True); os.makedirs(D+'tree/r')
json.dump(core,open(D+'tree/core.json','w'),ensure_ascii=False,separators=(',',':'))
tot=0
for ri in range(len(p)):
    d={k:ent(k) for k in RF[ri]}
    s=json.dumps(d,ensure_ascii=False,separators=(',',':')); tot+=len(s)
    open(D+f'tree/r/{ri}.json','w').write(s)
print('core',len(core),'reps total',tot, 'unreached', sum(1 for k in E if k not in depth))
