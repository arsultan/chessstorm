import json,sys,subprocess,chess,os
d,n=sys.argv[1],sys.argv[2]
R={str(r['n']):r for r in json.load(open(f'{d}/solved.json'))}
fen=R[n]['fen']; parts=fen.split(' '); parts[1]='b' if parts[1]=='w' else 'w'; parts[3]='-'
nf=' '.join(parts); b=chess.Board(nf); print('valid',b.is_valid(),nf)
open('/tmp/fx.pgn','w').write(f'[Event "?"]\n[SetUp "1"]\n[FEN "{nf}"]\n\n*\n')
subprocess.run(env=dict(os.environ,FORCE='1'),args=['python3','/home/claude/storm/solve2.py','/tmp/fx.pgn','/tmp/fx.json','/nonexistent.json'])
r=json.load(open('/tmp/fx.json'))[0]; import os; os.remove('/tmp/fx.json')
T=json.load(open(f'{d}/teacher.json'))
if r['ok']:
    T[n]={'fen':r['fen'],'m':r['m'],'a':r.get('a',{}),'side_fix':1}; json.dump(T,open(f'{d}/teacher.json','w')); print('saved',n)
else: print('NOT OK',r)
