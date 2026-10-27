"""Degree-1 histogram and pendant b-configuration count for cell files (engine format, FOUND lines).
usage: python3 analyze.py file...   Pendant b-configuration: 3 degree-1 vertices in three distinct edges, pairwise non-co-transversal
(a pair is co-transversal iff some minimum transversal contains both iff tau(G-u-v) = tau-2)."""
import sys, re, json, itertools, os
sys.setrecursionlimit(10000)
def parse(l):
    return [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
def tau(edges, ub=None):
    # min transversal by branching on an uncovered edge, with greedy upper bound and disjoint-edge lower bound
    edges = [frozenset(e) for e in edges]
    best = [len(edges)]
    def lb(es):
        used=set(); c=0
        for e in es:
            if not (e & used): used|=e; c+=1
        return c
    def rec(es, k):
        if not es:
            if k < best[0]: best[0] = k
            return
        if k + lb(es) >= best[0]: return
        e = es[0]
        for v in sorted(e, key=lambda v: -sum(1 for f in es if v in f)):
            rec([f for f in es if v not in f], k+1)
    rec(sorted(edges, key=lambda e: sorted(e)), 0)
    return best[0]
def analyze(edges):
    n = 1 + max(max(e) for e in edges); m = len(edges)
    deg = [0]*n
    for e in edges:
        for v in e: deg[v] += 1
    t = tau(edges)
    d1 = [v for v in range(n) if deg[v] == 1]
    def cotr(u, v):
        return tau([e for e in edges if u not in e and v not in e]) == t - 2
    nc = {}
    for u, v in itertools.combinations(d1, 2):
        nc[(u,v)] = not cotr(u, v)
    eof = {v: next(i for i,e in enumerate(edges) if v in e) for v in d1}
    nb = 0; trip = []
    for a, b, c in itertools.combinations(d1, 3):
        if len({eof[a], eof[b], eof[c]}) == 3 and nc[(a,b)] and nc[(a,c)] and nc[(b,c)]:
            nb += 1; trip.append((a,b,c))
    return dict(n=n, m=m, tau=t, slack=3*n+2*m-11*t, maxdeg=max(deg), deg_hist={k: deg.count(k) for k in sorted(set(deg))},
                n_deg1=len(d1), deg1=d1, pendant_b=nb, pendant_b_triples=trip[:5])
if __name__ == '__main__':
    out = {}
    for f in sys.argv[1:]:
        cls = [parse(l) for l in open(f) if l.startswith('FOUND')]
        res = [analyze(e) for e in cls]
        hist = {}
        for r in res: hist[r['n_deg1']] = hist.get(r['n_deg1'], 0) + 1
        out[os.path.basename(f)] = dict(classes=len(cls), n_deg1_hist=dict(sorted(hist.items())),
            pendant_b_total=sum(r['pendant_b'] for r in res), classes_with_pendant_b=sum(1 for r in res if r['pendant_b']),
            slacks=sorted({r['slack'] for r in res}), taus=sorted({r['tau'] for r in res}),
            ge3=[dict(edges=cls[i], **{k: res[i][k] for k in ('n_deg1','deg1','pendant_b')}) for i in range(len(res)) if res[i]['n_deg1'] >= 3])
        print(os.path.basename(f), json.dumps({k: v for k, v in out[os.path.basename(f)].items() if k != 'ge3'}), 'GE3:', len(out[os.path.basename(f)]['ge3']), flush=True)
    if os.environ.get('JSON'): json.dump(out, open(os.environ['JSON'], 'w'), indent=1)
