import glob
from common import *
from fastcores import has_core
rows=[]
out={}
for f in sorted(glob.glob('gen_*_s0.json')):
    g=json.load(open(f)); n=g['n']; sols=g['sols']
    mode,param=(0,0) if n<=12 else (1,3)
    res=run_cases([mk(i,n,e,mode,param) for i,e in enumerate(sols)],vcap=20)
    H=Counter(); H0=Counter(); nv=0; states=0; viol=[]
    for i,r in res.items():
        states+=r['states']
        for a,b in r['hist']['Q'].items(): H[a]+=b
        if r['violQ'] or r['violAct']:
            nv+=1
            kv=dict(x.split('=') for x in r['viol'][0].split())
            viol.append((i,sols[i],int(kv['S']),int(kv['D']),r['viol'][0]))
    # D-empty slack
    res0=run_cases([mk(i,n,e,1,0) for i,e in enumerate(sols)])
    for i,r in res0.items():
        for a,b in r['hist']['Q'].items(): H0[a]+=b
    fullO=[has_core(n,sols[i]) for i,_ in [(v[0],0) for v in viol]]
    key=f[:-5]
    out[key]=dict(cls=g['cls'],n=n,m=g['m'],T=g['T'],status=g['status'],nhyp=len(sols),states=states,hyp_with_viol=nv,
       viol_hyps_with_fullcore_violation=sum(fullO),minslack=min(H),slackD0=sorted(H0.items()),viol=viol[:5])
    print(key,g['status'],len(sols),'states',states,'hyps_with_viol',nv,'of which violate full cores',sum(fullO),'D0 slack',sorted(H0.items()),flush=True)
json.dump(out,open('step3_results.json','w'))
