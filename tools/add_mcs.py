import sys,re,json
f=sys.argv[1]; s=open(f,encoding='utf-8').read()
B=json.load(open('/home/claude/mcs/mcs_book.json',encoding='utf-8'))
m=re.search(r'const BOOKS=(\[.*?\]);\s*let CFG',s,re.S); BOOKS=json.loads(m.group(1))
BOOKS=[b for b in BOOKS if b['id']!='mcs']+[B]
s=s[:m.start(1)]+json.dumps(BOOKS,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
def rep(a,b):
    global s
    if a in s: s=s.replace(a,b,1)
    else: print('MISS',a[:50])
rep("/^#(b|wp|pr|cs|ter)(\\d{1,4})$/","/^#(b|wp|pr|cs|ter|mcs)(\\d{1,4})$/")
rep("const EMB={n:['wn','#cfe3c7'],k:['wk','#f2d6a2'],r:['wr','#f2c94c']};","const EMB={n:['wn','#cfe3c7'],k:['wk','#f2d6a2'],r:['wr','#f2c94c'],q:['wq','#cbd9ee']};")
rep("А. Терехин «Ладейный эндшпиль».","А. Терехин «Ладейный эндшпиль», J. Hellsten «Mastering Chess Strategy».")
if 'hub/' in f:
    rep('content="Woodpecker Method 2, Терехин, Призант, Гулиев: решай позиции на время, 10 или 15 минут."','content="Woodpecker Method 2, Mastering Chess Strategy, Терехин, Призант, Гулиев: решай позиции на время, 10 или 15 минут."')
    rep('content="Woodpecker Method 2, Терехин, Призант, Гулиев: решай позиции на время, 10 или 15 минут."','content="Woodpecker Method 2, Mastering Chess Strategy, Терехин, Призант, Гулиев: решай позиции на время, 10 или 15 минут."')
    rep('Решай позиции из 4 шахматных книг на время','Решай позиции из 5 шахматных книг на время')
    rep('<b>2300 упражнений</b>','<b>2700 упражнений</b>')
open(f,'w',encoding='utf-8').write(s); print('ok',f,len(s))
