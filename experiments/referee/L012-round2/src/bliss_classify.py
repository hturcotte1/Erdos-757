# Referee round 2: isomorphism classes via igraph/BLISS (independent of nauty and of VF2), with explicit verified relabellings.
# Usage: bliss_classify.py NV reps_file hits_file   (lines "TAG: (a,b,c) ...")
import sys, re, igraph as ig
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def canon(nv, E):
    g = ig.Graph(n=nv + len(E), edges=[(v, nv + j) for j, e in enumerate(E) for v in e])
    col = [0] * nv + [1] * len(E)
    p = g.canonical_permutation(color=col); h = g.permute_vertices(p)
    hE = set(frozenset(x) for x in h.get_edgelist())
    inv = [0] * len(p)
    for i, x in enumerate(p): inv[x] = i
    mp = None
    for cand in (p, inv):   # whichever relabelling actually maps g onto its canonical graph h (convention-independent)
        if set(frozenset((cand[a], cand[b])) for a, b in g.get_edgelist()) == hE and all((cand[i] < nv) == (i < nv) for i in range(len(cand))):
            mp = cand; break
    assert mp is not None
    key = tuple(sorted(tuple(sorted(mp[v] for v in e)) for e in E))
    return key, mp
def verify_map(nv, E1, p1, E2, p2):
    inv2 = {p2[v]: v for v in range(nv)}
    mp = [inv2.get(p1[v]) for v in range(nv)]
    if any(x is None for x in mp) or len(set(mp)) != nv: return False
    return set(frozenset(mp[v] for v in e) for e in E1) == set(frozenset(e) for e in E2)
nv = int(sys.argv[1])
reps = [parse(l) for l in open(sys.argv[2]) if '(' in l]
rk = {}
for i, E in enumerate(reps):
    k, p = canon(nv, E)
    if k in rk: print('REPS', i, 'and', rk[k][0], 'have equal BLISS forms (isomorphic)')
    else: rk[k] = (i, E, p)
print('representatives %d, distinct BLISS classes %d' % (len(reps), len(rk)))
if len(sys.argv) > 3:
    hit = set(); unmatched = 0; bad = 0; nh = 0
    for l in open(sys.argv[3]):
        if '(' not in l: continue
        E = parse(l); nh += 1
        k, p = canon(nv, E)
        if k not in rk: unmatched += 1; continue
        i, E2, p2 = rk[k]
        if not verify_map(nv, E, p, E2, p2): bad += 1
        hit.add(i)
    print('graphs %d, matched %d, unmatched %d, failed explicit verification %d, representatives hit %d of %d'
          % (nh, nh - unmatched, unmatched, bad, len(hit), len(rk)))
