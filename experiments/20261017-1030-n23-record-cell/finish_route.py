"""Collect hits of a final stage, iso-dedupe, orderability SAT, exact saturated realization, (4,5) and h check."""
import sys,re,json,time
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
from engine import iso_dedupe, parse_hits
from post import orderings
from realize_fast import realize_fast
from e757.core import is_45_set, alpha
files=sys.argv[2:]; tag=sys.argv[1]; n=23
hits=[]
for f in files: hits+=list(parse_hits(open(f).read()))
print('raw hits',len(hits),flush=True)
reps=iso_dedupe(hits); print('iso classes',len(reps),flush=True)
res=dict(raw_hits=len(hits),iso_classes=len(reps),orderable=0,realized_graphs=0,candidates=[])
t0=time.time(); orderable=[]
for es in reps:
    if orderings(es,n): orderable.append(es)
res['orderable']=len(orderable); print('orderable classes',len(orderable),time.time()-t0,flush=True)
stats_tot=dict(assignments=0,solvable=0,distinct=0,noextra=0,exact_ok=0)
for k,es in enumerate(orderable):
    f,s=realize_fast(es,n)
    for key in stats_tot: stats_tot[key]+=s[key]
    if f:
        res['realized_graphs']+=1
        for S in f[:50]:
            ok45=is_45_set(S); h=alpha(S) if ok45 else None
            res['candidates'].append(dict(edges=es,set=S,is45=ok45,h=h))
            print('REALIZED',S,ok45,h,flush=True)
    if k%50==0: print('progress',k,len(orderable),stats_tot,round(time.time()-t0),flush=True)
res['realize_stats']=stats_tot
json.dump(res,open('results_%s_final.json'%tag,'w'))
print(res['raw_hits'],res['iso_classes'],res['orderable'],res['realized_graphs'],stats_tot)
