"""L020 calibration: non-co-transversal pair structures ("roles") in stored connected class-C graphs.
Exact integer arithmetic only.  Usage: python3 roles.py <cellfile> [<cellfile> ...]
Cell files: either engine format (lines 'FOUND: (a,b,c) ...') or transversal-richness input format
('n m tau a b c a b c ...' one graph per line).
For each graph F (connected, Delta<=3 lists) and the set A of vertices of F-degree <= 2 we compute all minimum
transversals and the graph NC on A of non-co-transversal pairs ({x,y} contained in no minimum transversal), then:
  maxdeg_NC   : the largest number of NC-partners of a vertex (the 'matching property' M* says <= 1);
  role_b      : triples of A pairwise in NC whose three vertices do not form an edge of F;
  role_e      : (e; a,b) with {a,e},{b,e} in NC, a,b not in a common edge of F;
  role_f1     : ({a,b},{c,e}) disjoint, {a,b} not in a common edge, all four cross pairs in NC;
  role_f1_inC : those role_f1 configurations with F + w({a,b},{c,e}) in C (linear, F7-free, (P3)).
"""
import sys, os, re, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017')
import hyp

def read_any(path):
    out = []
    for l in open(path):
        l = l.strip()
        if not l: continue
        if l.startswith('FOUND:'):
            es = hyp.parse_edges(l); n = 1 + max(max(e) for e in es); out.append((n, es)); continue
        if l[0].isdigit():
            a = list(map(int, l.split()))
            n, m = a[0], a[1]; flat = a[3:]
            es = [tuple(flat[3*i:3*i+3]) for i in range(m)]
            out.append((n, es))
    return out

def p3_ok_fast(n, edges):
    """(P3) e(S) <= |S|-2 for all S, |S|>=2  <=>  for every pair {x,y} the edges have an SDR avoiding x,y (Hall)."""
    m = len(edges)
    if m == 0: return True
    for x in range(n):
        for y in range(x+1, n):
            match = {}  # vertex -> edge index
            def aug(i, seen):
                for u in edges[i]:
                    if u == x or u == y or u in seen: continue
                    seen.add(u)
                    if u not in match or aug(match[u], seen):
                        match[u] = i; return True
                return False
            for i in range(m):
                if not aug(i, set()): return False
    return True

def in_C(n, edges):
    return hyp.is_linear(edges) and not hyp.contains_F7(n, edges) and p3_ok_fast(n, edges)

def analyse(n, es):
    em = hyp.masks(es)
    Ts, t = hyp.all_min_transversals(em)
    deg = hyp.degrees(n, es)
    A = [x for x in range(n) if deg[x] <= 2]
    cov = [0] * n
    for T in Ts:
        mm = T
        while mm:
            b = mm & -mm; mm ^= b
            cov[b.bit_length() - 1] |= T
    share = set()
    for e in es:
        for x, y in itertools.combinations(e, 2): share.add((min(x,y), max(x,y)))
    eset = set(frozenset(e) for e in es)
    NC = {x: set() for x in A}
    for x, y in itertools.combinations(A, 2):
        if not (cov[x] >> y) & 1:
            NC[x].add(y); NC[y].add(x)
    novert = sum(1 for x in range(n) if deg[x] > 0 and cov[x] == 0)
    maxdeg = max([len(NC[x]) for x in A] + [0])
    rb = 0
    for x, y, z in itertools.combinations(A, 3):
        if y in NC[x] and z in NC[x] and z in NC[y] and frozenset((x,y,z)) not in eset: rb += 1
    re_ = 0
    for e in A:
        for a, b in itertools.combinations(sorted(NC[e]), 2):
            if (min(a,b), max(a,b)) not in share: re_ += 1
    rf = 0; rf_in = 0; rf_ex = []
    for a, b in itertools.combinations(A, 2):
        if (a, b) in share: continue
        common = NC[a] & NC[b]
        for c, e in itertools.combinations(sorted(common), 2):
            if c in (a, b) or e in (a, b): continue
            rf += 1
            w = n
            es2 = list(es) + [(w, a, b), (w, c, e)]
            if in_C(n + 1, es2):
                rf_in += 1
                if len(rf_ex) < 3: rf_ex.append((a, b, c, e))
    ncpairs = sum(len(NC[x]) for x in A) // 2
    return dict(n=n, m=len(es), tau=t, slack=3*n+2*len(es)-11*t, nT=len(Ts), novert=novert, ncpairs=ncpairs,
                maxdegNC=maxdeg, role_b=rb, role_e=re_, role_f1=rf, role_f1_inC=rf_in, rf_ex=rf_ex,
                Delta=max(deg))

if __name__ == '__main__':
    import json
    for path in sys.argv[1:]:
        gs = read_any(path)
        agg = dict(classes=0, with_nc=0, maxdeg_ge2=0, role_b=0, role_e=0, role_f1=0, role_f1_inC=0, novert=0)
        maxmd = 0; ex = []
        skipped = 0
        for (n, es) in gs:
            if max(hyp.degrees(n, es)) > 3:
                skipped += 1; continue
            r = analyse(n, es)
            agg['classes'] += 1
            agg['with_nc'] += r['ncpairs'] > 0
            agg['maxdeg_ge2'] += r['maxdegNC'] >= 2
            for k in ('role_b', 'role_e', 'role_f1', 'role_f1_inC'): agg[k] += (r[k] > 0)
            agg['novert'] += r['novert']
            maxmd = max(maxmd, r['maxdegNC'])
            if r['role_f1_inC'] and len(ex) < 2: ex.append((n, es, r['rf_ex']))
        cell = (gs[0][0], len(gs[0][1])) if gs else None
        sl = (3*gs[0][0] + 2*len(gs[0][1]) - 11*hyp.tau(gs[0][0], gs[0][1])) if gs else None
        print(os.path.basename(path), 'cell', cell, 'slack', sl, 'Delta>3 skipped', skipped, json.dumps(agg), 'max NC-degree', maxmd, flush=True)
        for x in ex: print('   role_f1_inC example:', x, flush=True)
