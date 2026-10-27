import sys, json, time
sys.path.insert(0,'src')
from part3m import *
lib=load_library()
by={c.name:c for c in lib}
t0=time.time()
covs,nodes=minimal_covers([by['t14#0'],by['t10#0']],4,max_nodes=3_000_000)
print(len(covs),nodes,round(time.time()-t0,1), by['t14#0'].nmis, by['t10#0'].nmis)
