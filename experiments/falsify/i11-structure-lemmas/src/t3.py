import sys,time; sys.path.insert(0,'src')
from part3a import *
lib=load_library()
import collections
for N in (13,16):
  for idxs in multisets(lib,N):
    t0=time.time()
    res,info=search_union(lib,idxs,max_nodes=3_000_000)
    print([lib[i].name for i in idxs], len(res), collections.Counter(info[4]), info[3], round(time.time()-t0,1), flush=True)
