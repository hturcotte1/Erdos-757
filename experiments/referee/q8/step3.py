import json, random, subprocess, itertools
from check import is45, apm, sweep
F='../../falsify/q8-omega-inequality/'
rs=json.load(open(F+'random_sets.json')); ad=json.load(open(F+'adv_sets.json'))
print({k:len(v) for k,v in rs.items()},{k:len(v) for k,v in ad.items()})
rng=random.Random(7); res=[]
for src,pool in (('random',rs),('adv',ad)):
    for nk in ('12','14','16'):
        for idx in rng.sample(range(len(pool[nk])),4 if nk!='16' else 2):
            A=pool[nk][idx]; ok=is45(A); m=len(apm(A))
            r=dict(src=src,n=len(A),idx=idx,is45=ok,aps=m,saturated=(m==len(A)-2),distinct=len(set(A))==len(A))
            if len(A)<=14 and ok:
                E,out=sweep(A); r['sweep']=[l for l in out.splitlines() if l.startswith('RESULT')][0]
            res.append(r); print(r,flush=True)
print(len(res),'sets;',sum(r['is45'] for r in res),'are (4,5)-sets;',sum(r['saturated'] for r in res),'saturated')
