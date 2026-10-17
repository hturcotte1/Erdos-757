"""Referee L008 round 3: definitional extension + filter pipeline, written from scratch (numpy).
Input: FOUND lines (3-graphs on vertices 0..NG-1; for mode A the graphs are (12,10) and the edge (12,13,14) is added).
For each G on 15 vertices: every unordered triple of pairwise disjoint pairs {a,b} of V(G) with no pair inside an edge of G and
G-degree <= 2 at every endpoint; H = G + {15,a_i,b_i}.  tau(H) >= 7 is tested DEFINITIONALLY: no 6-subset of the 16 vertices
meets all 14 edges (all C(16,6)=8008 subsets, vectorised).  Hits are filtered definitionally: F7 containment = some 5 edges on 7
vertices are the image of F7 under one of the 7! bijections (degree-multiset prefilter); P3 = e(S) <= |S|-2 for ALL vertex
subsets S with |S| >= 2 (all 2^16 subsets, vectorised).  Also checks tau(G) = 6 for every input and reports class-level counts.
Usage: r3_extend.py A|B file [maxgraphs]"""
import sys, re, itertools, numpy as np
mode, path = sys.argv[1], sys.argv[2]
NG = 15; NH = 16
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
PERMS = list(itertools.permutations(range(7)))
def parse(f):
    for l in open(f):
        if l.startswith('FOUND:'):
            yield [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
def mask(e): return sum(1 << v for v in e)
SUB6 = np.array([mask(c) for c in itertools.combinations(range(NH), 6)], dtype=np.int64)   # all 6-subsets of V(H)
ALLS = np.arange(1 << NH, dtype=np.int64)
POP = np.array([bin(s).count('1') for s in range(1 << NH)], dtype=np.int64)
def tau_ge7(edges):
    ok = np.ones(len(SUB6), dtype=bool)
    for e in edges: ok &= (SUB6 & mask(e)) != 0
    return not ok.any()
def tau_exact(edges, nv):
    for k in range(0, nv + 1):
        for S in itertools.combinations(range(nv), k):
            sm = mask(S)
            if all(mask(e) & sm for e in edges): return k
    return nv
def contains_f7(edges):
    ms = [mask(e) for e in edges]
    for five in itertools.combinations(range(len(edges)), 5):
        U = 0
        for i in five: U |= ms[i]
        if bin(U).count('1') != 7: continue
        verts = [v for v in range(NH) if U >> v & 1]
        degs = sorted(sum(1 for i in five if ms[i] >> v & 1) for v in verts)
        if degs != [2,2,2,2,2,2,3]: continue
        fiveset = set(ms[i] for i in five)
        for p in PERMS:
            if all(mask((verts[p[a]], verts[p[b]], verts[p[c]])) in fiveset for a, b, c in F7): return True
    return False
def p3_ok(edges):
    cnt = np.zeros(1 << NH, dtype=np.int64)
    for e in edges:
        m = mask(e); cnt += ((ALLS & m) == m)
    bad = (POP >= 2) & (cnt > POP - 2)
    return not bad.any()
def linear(edges):
    ms = [mask(e) for e in edges]
    return all(bin(ms[i] & ms[j]).count('1') <= 1 for i in range(len(ms)) for j in range(i+1, len(ms)))
graphs = list(parse(path))
if len(sys.argv) > 3: graphs = graphs[:int(sys.argv[3])]
tot_ext = tot_hits = f7hits = p3bad = surv = 0; badtau = 0
for G in graphs:
    if mode == 'A':
        assert len(G) == 10 and set().union(*G) == set(range(12)); G = G + [(12,13,14)]
    assert len(G) == 11 and linear(G) and (mode == 'C' or set().union(*G) == set(range(15)))
    if tau_exact(G, NG) != 6: badtau += 1
    deg = [0]*NG
    for e in G:
        for v in e: deg[v] += 1
    gm = [mask(e) for e in G]
    pairs = [(a, b) for a in range(NG) for b in range(a+1, NG) if deg[a] <= 2 and deg[b] <= 2 and not any((m >> a & 1) and (m >> b & 1) for m in gm)]
    for i in range(len(pairs)):
        p1 = pairs[i]
        for j in range(i+1, len(pairs)):
            p2 = pairs[j]
            if set(p1) & set(p2): continue
            for k in range(j+1, len(pairs)):
                p3 = pairs[k]
                if (set(p1) | set(p2)) & set(p3): continue
                tot_ext += 1
                H = G + [(p1[0], p1[1], NH-1), (p2[0], p2[1], NH-1), (p3[0], p3[1], NH-1)]
                if tau_ge7(H):
                    tot_hits += 1
                    print('HIT: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in H))
                    f7 = contains_f7(H); ok3 = p3_ok(H)
                    f7hits += f7; p3bad += (not ok3)
                    if not f7 and ok3:
                        surv += 1; print('SURVIVOR:', H)
print(f'mode={mode} graphs={len(graphs)} bad_tau={badtau} extensions={tot_ext} hits(tau>=7)={tot_hits} hits_with_F7={f7hits} hits_violating_P3={p3bad} survivors={surv}')
