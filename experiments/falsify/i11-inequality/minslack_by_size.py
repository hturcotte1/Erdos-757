from common import *
import sys
f,tag=sys.argv[1],sys.argv[2]
p=subprocess.run(['nice','-n','5',HERE+'/subsets'],stdin=open(f),capture_output=True,text=True)
j=json.loads("\n".join(l for l in p.stdout.splitlines() if not l.startswith('VIOLATION')))
by={}
for s,m,t,c,wl,wm,sl in j['hist']:
    d=by.setdefault(s,{})
    if sl not in d: d[sl]=[]
    d[sl].append((m,t,c))
res={s:{'min_slack':min(d),'cells_at_min':[dict(m=m,tau=t,count=c) for m,t,c in d[min(d)]]} for s,d in sorted(by.items())}
json.dump(res,open(HERE+'/results_minslack_by_size_%s.json'%tag,'w'),indent=1)
for s,r in res.items(): print(tag,'size',s,'min slack',r['min_slack'],r['cells_at_min'])
