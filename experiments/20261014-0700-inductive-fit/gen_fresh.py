"""Fresh abstract hypergraphs via e757.cpsat_model.enumerate_solutions (one process, 300 s per call, seed 1)."""
import sys,json,time,glob
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import enumerate_solutions, load_cores
CORES=load_cores(*sorted(glob.glob('/home/user/Erdos-757/data/forbidden_ordered_n*.json')))
for cls in ('O','Op'):
    for (n,m,T) in ((10,8,6),(11,9,7),(13,11,8)):
        kw=dict(monotone=True,medial=True,cores=CORES) if cls=='Op' else dict(monotone=False,medial=False,cores=None)
        t=time.time()
        cnt,sols,status=enumerate_solutions(n,T,m,limit=200,time_limit=300,workers=1,seed=1,**kw)
        json.dump(dict(cls=cls,n=n,m=m,T=T,status=status,count=cnt,time=time.time()-t,sols=[s[0] for s in sols]),open(f'fresh_{cls}_{n}_{m}_{T}.json','w'))
        print(cls,n,m,T,status,cnt,round(time.time()-t),flush=True)
