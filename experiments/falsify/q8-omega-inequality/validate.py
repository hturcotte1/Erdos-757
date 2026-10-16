from q8lib import *
import itertools, collections
from sanity import ref
def indep(E,D): return not any(e<=D for e in E)
for name,A,k in [('12b',[0,178,198,218,227,235,272,276,287,317,356,436],3),('base',[0,136,200,243,246,249,272,286,298,323,400,528,596,1056],2)]:
    E=[set(e) for e in ap_edges(A)]; n=len(A)
    h=collections.Counter(); hd=collections.Counter()
    for s in range(k+1):
        for D in itertools.combinations(A,s):
            if indep(E,set(D)):
                tau,e1,e2,R,l4,r4,l,r=ref(A,D); h[r-l]+=1; hd[r4-l4]+=1
    res=run_cases([(1,n,masks_of(A),1,k,0)])[1]
    print(name, dict(h)==res['hist']['Q'], dict(hd)==res['hist']['D'], sum(h.values()), res['states'])
