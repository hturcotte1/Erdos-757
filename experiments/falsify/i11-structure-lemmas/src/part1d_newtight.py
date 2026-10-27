import sys, json
sys.path.insert(0,'src')
from hg import *
out={}
for fn,key in [('new_tight_17_13_7_deg4.json','n17_deg4'),('counterexample_conjecture_T_n21.json','n21_deg4')]:
    gs=json.load(open(fn))['graphs']; res=[]
    for g in gs:
        n=g['n']; es=[tuple(e) for e in g['edges']]; t=tau(n,es)
        u=[x for x in range(n) if tau(n,es,((1<<n)-1)&~(1<<x))==t]
        res.append({'n':n,'tau':t,'universal_vertices':u})
    out[key]=res; print(key,res)
json.dump(out,open('part1d_newtight.json','w'))
