import sys,re,json
f,bj,hid=sys.argv[1],sys.argv[2],sys.argv[3]; s=open(f,encoding='utf-8').read()
B=json.load(open(bj,encoding='utf-8'))
m=re.search(r'const BOOKS=(\[.*?\]);\s*let CFG',s,re.S); BOOKS=json.loads(m.group(1))
BOOKS=[b for b in BOOKS if b['id']!=B['id']]+[B]
s=s[:m.start(1)]+json.dumps(BOOKS,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
rm=re.search(r"/\^#\(([a-z0-9|]+)\)\(\\d\{1,4\}\)\$/",s)
ids=rm.group(1).split('|')
if hid not in ids: s=s[:rm.start(1)]+'|'.join(ids+[hid])+s[rm.end(1):]
s=s.replace("репертуар «Гамбит Яниша» — студия Serta_chess.","репертуары «Гамбит Яниша» и «Волжский гамбит» — студии Serta_chess.")
open(f,'w',encoding='utf-8').write(s); print('ok',f,len(s),'|'.join(ids))
