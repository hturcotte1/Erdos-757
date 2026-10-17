"""Independent SAT decision (pysat/cadical) for a cell: does an ordered midpoint hypergraph (edges (i<j<k), each j midpoint of <=1 edge,
linear: two edges share <=1 vertex, F7 NOT imposed -> weaker class than O) with EXACTLY m edges and alpha <= T exist?
Extra sound constraints: every vertex covered is NOT imposed (all weaker).  Optional: --conn-free (no constraint).
Sound extra symmetry breaking: none (reflection only optional)."""
import sys, itertools, json, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def cell(n,m,tau0,reflect=True,k30=False,f7_free_check=True,timeout=None,cover=False):
    T=n-tau0
    trip=[(i,j,k) for i in range(n) for j in range(i+1,n) for k in range(j+1,n)]
    var={t:v+1 for v,t in enumerate(trip)}
    cl=[]
    # midpoint unique
    for j in range(n):
        es=[var[t] for t in trip if t[1]==j]
        for a,b in itertools.combinations(es,2): cl.append([-a,-b])
    # linear: pair in at most one edge
    for p in itertools.combinations(range(n),2):
        es=[var[t] for t in trip if p[0] in t and p[1] in t]
        for a,b in itertools.combinations(es,2): cl.append([-a,-b])
    # alpha<=T : every (T+1)-subset contains an edge
    for S in itertools.combinations(range(n),T+1):
        cl.append([var[t] for t in itertools.combinations(S,3)])
    if cover:  # WLOG connected component spanning all vertices (I11 is additive over components)
        for v in range(n): cl.append([var[t] for t in trip if v in t])
    top=len(trip)
    card=CardEnc.equals(lits=list(var.values()),bound=m,top_id=top,encoding=EncType.seqcounter)
    cl+=card.clauses
    if k30:
        # monotone midpoints K30: (i,j,k),(i',j',k'), i<=i', k<=k', (i,k)!=(i',k') => j<j'
        for t1 in trip:
            for t2 in trip:
                if t1!=t2 and t1[0]<=t2[0] and t1[2]<=t2[2] and not (t1[1]<t2[1]):
                    cl.append([-var[t1],-var[t2]])
    sys.path.insert(0,'/home/user/Erdos-757')
    from e757.cpsat_model import find_f7
    s=Cadical153(bootstrap_with=cl)
    t0=time.time(); edges=None; it=0
    while True:
        r=s.solve(); it+=1
        if not r: break
        mod=set(x for x in s.get_model() if x>0)
        edges=[t for t in trip if var[t] in mod]
        copies=find_f7(edges)
        if not copies: break
        for cp in copies:
            s.add_clause([-var[tuple(e)] for e in cp])
    if not r: edges=None
    return r,edges,time.time()-t0
if __name__=="__main__":
    n,m,tau0=map(int,sys.argv[1:4]); opts=sys.argv[4:]
    r,e,t=cell(n,m,tau0,k30='k30' in opts,cover='cover' in opts)
    print(json.dumps(dict(n=n,m=m,tau0=tau0,opts=opts,sat=r,edges=e,secs=round(t,1))))
