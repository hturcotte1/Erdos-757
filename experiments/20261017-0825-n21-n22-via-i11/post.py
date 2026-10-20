"""Post-process HIT lines (n-vertex, m-edge unordered graphs with tau>=T):  step (3) of the plan.
 F7 test; e(S)<=|S|-2 on all subsets; ordered injective midpoint labelling (SAT);  survivors written to survivors.json."""
import re,sys,json,itertools
import numpy as np
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import find_f7
from pysat.solvers import Cadical153
def parse(path):
    for l in open(path):
        if l.startswith('HIT:'):
            yield [tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
def sub_ok(es,n):
    S=np.arange(1<<n,dtype=np.int64); c=np.zeros(1<<n,dtype=np.int32)
    for e in es:
        mk=sum(1<<v for v in e); c+= ((S&mk)==mk)
    pc=np.zeros(1<<n,dtype=np.int32)
    for b in range(n): pc+=((S>>b)&1).astype(np.int32)
    bad=(c>0)&(c>pc-2)
    return not bad.any()
def orderings(es,n,limit=1):
    """Is there an order of the vertices and a midpoint (middle vertex) per edge, midpoints pairwise distinct, each edge (a,mid,b) with mid strictly between? SAT."""
    var={}; cnt=[0]
    def V(k):
        if k not in var: cnt[0]+=1; var[k]=cnt[0]
        return var[k]
    cl=[]
    lt=lambda u,v: V(('lt',u,v)) if u<v else -V(('lt',v,u))
    for a,b,c in itertools.permutations(range(n),3):   # transitivity a<b<c => a<c
        cl.append([-lt(a,b),-lt(b,c),lt(a,c)])
    for ei,e in enumerate(es):
        sel=[]
        for mid in e:
            a,b=[x for x in e if x!=mid]; s=V(('s',ei,mid)); sel.append(s)
            cl.append([-s,-lt(a,mid),lt(mid,b)])
            cl.append([-s,lt(a,mid),-lt(mid,b)])
        cl.append(sel)
        for x,y in itertools.combinations(sel,2): cl.append([-x,-y])
    for v in range(n):
        ss=[V(('s',ei,v)) for ei,e in enumerate(es) if v in e]
        for x,y in itertools.combinations(ss,2): cl.append([-x,-y])
    s=Cadical153(bootstrap_with=cl); r=s.solve(); return r
if __name__=="__main__":
    path=sys.argv[1]; n=int(sys.argv[2]); out=sys.argv[3]
    tot=nf7=nsub=nord=0; surv=[]
    for es in parse(path):
        tot+=1
        if find_f7(es): nf7+=1; continue
        if not sub_ok(es,n): nsub+=1; continue
        if not orderings(es,n): nord+=1; continue
        surv.append(es)
    res=dict(hits=tot,with_F7=nf7,F7free_killed_by_eS=nsub,F7free_eS_ok_not_orderable=nord,survivors=len(surv))
    json.dump(dict(summary=res,survivors=surv),open(out,'w'))
    print(res)
