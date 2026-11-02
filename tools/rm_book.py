import sys,re,json
f,bid=sys.argv[1],sys.argv[2]; s=open(f,encoding='utf-8').read()
m=re.search(r'const BOOKS=(\[.*?\]);\s*let CFG',s,re.S); B=json.loads(m.group(1))
B=[b for b in B if b['id']!=bid]
s=s[:m.start(1)]+json.dumps(B,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
s=re.sub(r'\|'+bid+r'(?=[|)])','',s,count=1)
open(f,'w',encoding='utf-8').write(s); print('ok',f,[b['id'] for b in B])
