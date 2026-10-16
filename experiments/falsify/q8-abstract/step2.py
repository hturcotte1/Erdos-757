from common import *
from verify import q8, indep, classify
from fastcores import has_core
d=json.load(open('../../20261014-0500-slack-landscape/witnesses.json'))
out={}
for fam in d:
    cases=[];meta={}
    for j,(k,v) in enumerate(d[fam].items()):
        n=v['n']; mode,param=(0,0) if n<=12 else (1,3)
        cases.append(mk(j,n,v['edges'],mode,param)); meta[j]=(k,v)
    res=run_cases(cases,vcap=50)
    H=Counter(); viol=[]; states=0
    for j,r in res.items():
        states+=r['states']
        for a,b in r['hist']['Q'].items(): H[a]+=b
        for line in r['viol']:
            kv=dict(x.split('=') for x in line.split()); viol.append((meta[j][0],int(kv['S']),int(kv['D']),line))
    print(fam,len(cases),'states',states,'viol',len(viol),'minslack',min(H)); 
    for x in viol[:5]: print(x)
    out[fam]=dict(n=len(cases),states=states,viol=viol,hist=sorted(H.items()))
json.dump(out,open('step2_results.json','w'))
