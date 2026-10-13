"""Quick random search: linear F7-free 3-uniform hypergraphs minimizing the Henning-Yeo slack
delta = 5n+3m-17 tau (exact arithmetic). Heuristic exploration only; HY theorem says delta>=0."""
import itertools, random, sys
from itertools import combinations
def tau(n, edges):
    masks=[sum(1<<v for v in e) for e in edges]
    best=[n]
    def rec(cov_masks, chosen):
        if chosen>=best[0]: return
        un=[m for m in cov_masks]
        if not un: best[0]=chosen; return
        # branch on edge with fewest... pick first
        e=un[0]
        for v in range(n):
            if e>>v&1:
                rec([m for m in un if not (m>>v&1)], chosen+1)
    rec(masks,0); return best[0]
def has_F7(n,E):
    Es=[frozenset(e) for e in E]
    inc={v:[e for e in Es if v in e] for v in range(n)}
    for v in range(n):
        for tri in combinations(inc[v],3):
            pairs=[e-{v} for e in tri]
            pts6=set().union(*pairs)
            if len(pts6)<6: continue
            cands=[e for e in Es if v not in e and e<=pts6 and all(len(e&p)==1 for p in pairs)]
            for a,b in combinations(cands,2):
                if not a&b: return True
    return False
def rand_hg(n,rng):
    E=[]; trip=list(combinations(range(n),3)); rng.shuffle(trip)
    for t in trip:
        s=set(t)
        if any(len(s&set(e))>=2 for e in E): continue
        E2=E+[t]
        if has_F7(n,E2): continue
        E=E2
    return E
if __name__=="__main__":
    rng=random.Random(int(sys.argv[2]) if len(sys.argv)>2 else 1)
    n=int(sys.argv[1]); best=None
    import time; t0=time.time()
    while time.time()-t0<float(sys.argv[3]) if len(sys.argv)>3 else 60:
        E=rand_hg(n,rng)
        # random deletion to vary
        for _ in range(rng.randint(0,3)):
            if E: E.pop(rng.randrange(len(E)))
        m=len(E); t=tau(n,E); d=5*n+3*m-17*t
        if best is None or d<best[0]:
            best=(d,m,t,E); print(n,'delta',d,'m',m,'tau',t,E,flush=True)
