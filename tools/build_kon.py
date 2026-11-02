import json,sys
src,out,bid,short,book,author,rb=sys.argv[1:8]
R=json.load(open(src))
import os
TF=sys.argv[8] if len(sys.argv)>8 else None
TE=json.load(open(TF)) if TF and os.path.exists(TF) else {}
for r in R:
    t=TE.get(str(r['n']))
    if t and not t.get('exclude'):
        old=r.get('m') or []; olda=r.get('a') or {}
        keep={k:[x for x in v if x!=t['m'][int(k)][:4]] for k,v in olda.items() if int(k)<len(t['m']) and old[:int(k)]==t['m'][:int(k)]}
        for k in range(0,min(len(old),len(t['m'])),2):
            if old[:k]==t['m'][:k] and old[k][:4]!=t['m'][k][:4] and k>0:
                keep.setdefault(str(k),[]); keep[str(k)]=sorted(set(keep[str(k)]+[old[k][:4]])); break
            if old[:k+1]!=t['m'][:k+1]: break
        keep={k:v for k,v in keep.items() if v}
        for k,v in (t.get('a') or {}).items(): keep[k]=sorted(set(keep.get(k,[]))|set(v))
        r.update(ok=True,fen=t['fen'],m=t['m'],a=keep,teacher=1)
R=[r for r in R if r.get('ok') and r.get('m') and not (TE.get(str(r['n'])) or {}).get('exclude')]
R.sort(key=lambda r:r['n'])
data=[{'lab':str(r['n']),'fen':r['fen'],'m':r['m'],'n':i+1,**({'a':r['a']} if r.get('a') else {})} for i,r in enumerate(R)]
blocks=[]
for lo in range(1,601,60):
    idx=[i for i,r in enumerate(R) if lo<=r['n']<lo+60]
    if idx: blocks.append({'name':f'{lo}–{lo+59}','s':idx[0],'e':idx[-1]+1})
blocks.append({'name':f'Все позиции ({len(data)})','s':0,'e':len(data)})
B={'id':bid,'short':short,'key':bid+'storm','title':'Konotop Storm','book':book,'author':author,'item':'Позиция','cover':False,'emb':'n','full':1,'mate':1,'blocks':blocks,'data':data}
json.dump(B,open(out,'w'),ensure_ascii=False)
print(len(data),'positions;',sum(len(d['m'])//2+1 for d in data)/len(data),'avg moves')
