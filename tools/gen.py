import json,sys
p=json.load(open("plan2.json"));T=int(sys.argv[3]) if len(sys.argv)>3 else 522813638;REF=sys.argv[4] if len(sys.argv)>4 else "ref_91"
acts=[]
for i in range(int(sys.argv[1]),int(sys.argv[2])+1):
    x=p[i-1]; nm=x['name'].replace("'","\\'")
    acts+= [{"name":"navigate","input":{"url":"https://lichess.org/study/mine/newest","tabId":T}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":"document.querySelector('form[action$=\"/study\"]').submit(); 'ok'"}},
     {"name":"computer","input":{"action":"wait","duration":3,"tabId":T}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":f"window.__N='{nm}'; await eval(localStorage.hB)"}},
     {"name":"find","input":{"query":"PGN file input","tabId":T}},
     {"name":"file_upload","input":{"paths":["/home/claude/deb/"+x['file']],"ref":REF,"tabId":T}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":f"window.__O='{x['orient']}'; '#{i} exp {x['cnt']}: '+await eval(localStorage.hC)"}}]
print(json.dumps(acts,ensure_ascii=False))
