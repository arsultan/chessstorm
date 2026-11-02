import chess,chess.pgn,json,io,sys
tfile,src=sys.argv[1],sys.argv[2]
T=json.load(open(tfile)); cnt=0
for line in open(src,encoding='utf-8'):
    line=line.strip()
    if not line: continue
    n,fen,mv=line.split('|',2)
    if T.get(n,{}).get('exclude'): continue
    g=chess.pgn.read_game(io.StringIO(f'[SetUp "1"]\n[FEN "{fen}"]\n\n{mv} *\n'))
    if g.errors: print('ERR',n,g.errors); continue
    m=[]; a={}; node=g; turn=chess.Board(fen).turn
    while node.variations:
        nb=node.board()
        if len(node.variations)>1 and nb.turn==turn:
            a[str(len(m))]=[v.move.uci()[:4] for v in node.variations[1:]]
        node=node.variations[0]; m.append(node.move.uci())
    if m: T[n]={'fen':fen,'m':m,'a':a}; cnt+=1
json.dump(T,open(tfile,'w')); print('imported',cnt,'total',len(T))
