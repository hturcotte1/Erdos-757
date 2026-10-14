import sys,json,time
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import feasible_alpha_le
out={}
for n,T in [(14,7),(16,9)]:
    t=time.time(); r,e,st=feasible_alpha_le(n,T,forbid_f7=True,time_limit=300,workers=2)
    out[f'{n},{T}']=dict(result=r,edges=e,time=round(time.time()-t)); print(n,T,r,round(time.time()-t),flush=True)
json.dump(out,open('unsat_results.json','w'))
