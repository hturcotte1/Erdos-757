import sys,json,time
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import enumerate_solutions, load_cores
import glob
cls,n,m,T,seed=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
kw={}
if cls=='Op':
    kw=dict(monotone=True,medial=True,cores=load_cores(*sorted(glob.glob('/home/user/Erdos-757/data/forbidden_ordered_n*.json'))))
else: kw=dict(monotone=False,medial=False,cores=None)
t=time.time()
cnt,sols,status=enumerate_solutions(n,T,m,limit=300,time_limit=300,workers=2,seed=seed,**kw)
json.dump(dict(cls=cls,n=n,m=m,T=T,status=status,count=cnt,time=time.time()-t,sols=[s[0] for s in sols]),open(f'gen_{cls}_{n}_{m}_{T}_s{seed}.json','w'))
print(cls,n,m,T,status,cnt,round(time.time()-t))
