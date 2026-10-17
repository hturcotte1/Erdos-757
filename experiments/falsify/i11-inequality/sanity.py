# cross-check C tool vs python e757.core.alpha on random induced subsets of A_base and a 12-pt set
from common import *
import random
random.seed(1)
d=json.load(open(ROOT+'/data/small_records.json'))['sets']
bad=0;tot=0
for key in ['14','12b']:
    A=sorted(d[key]['set']); n=len(A); E=edges_idx(A)
    j=run_c([line(n,E)])
    hist={(h[0],h[1],h[2]):h[3] for h in j['hist']}
    # recompute histogram in python for ALL subsets of n=12 set (4096) and 14 (16384, use alpha from core)
    from collections import Counter
    C=Counter()
    for mask in range(1<<n):
        S=[A[i] for i in range(n) if mask>>i&1]
        es=ap_edges(S) if len(S)>=3 else []
        a=alpha(S,es) if S else 0
        C[(len(S),len(es),len(S)-a)]+=1
    C.pop((0,0,0),None); ok = (dict(C)==hist)
    print(key,'C hist == python hist:',ok, len(C))
    assert ok
