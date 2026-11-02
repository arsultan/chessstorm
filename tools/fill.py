import json,sys,subprocess,chess,chess.pgn,os
d=sys.argv[1]
R=json.load(open(f'{d}/solved2.json'))
short=[r for r in R if r.get('ok') and len(r['m'])<=3]
print('short',len(short))
with open(f'{d}/short.pgn','w') as f:
    for r in short:
        g=chess.pgn.Game(); g.setup(chess.Board(r['fen'])); g.headers['Round']=str(r['n']); f.write(str(g)+'\n\n')
# prior file with n renumbered 1..len to reuse first moves
pri=[dict(r,n=k+1) for k,r in enumerate(short)]
json.dump(pri,open(f'{d}/short_prior.json','w'))
best={r['n']:r for r in R}
for t in range(2):
    out=f'{d}/short_out{t}.json'
    if os.path.exists(out): os.remove(out)
    subprocess.run(['python3','/home/claude/storm/solve2.py',f'{d}/short.pgn',out,f'{d}/short_prior.json'],stdout=subprocess.DEVNULL)
    for k,r in enumerate(json.load(open(out))):
        n=short[k]['n']
        if len(r['m'])>len(best[n]['m']):
            best[n]=dict(best[n],m=r['m'],a=r['a'])
R2=[best[r['n']] for r in R]
json.dump(R2,open(f'{d}/solved3.json','w'))
print('still short',sum(1 for r in R2 if r.get('ok') and len(r['m'])<=3))
