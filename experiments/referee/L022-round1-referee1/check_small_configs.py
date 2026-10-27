# Referee check of the clause of L022 Theorem 1(e): every connected linear 3-graph with <= 4 edges
# is EXACTLY realizable (AP hypergraph equal to it); hence every linear member of M_R has >= 5 edges.
# Also: every proper sub-hypergraph of F7 is realizable, F7 itself is not.
import random
from itertools import combinations
from rlib import is_linear, components, verts, is_45_bruteforce
from realize import decide, ap_edges_of_points


def extend(E):
    """All connected linear one-edge extensions (labelled; new vertices get the next labels)."""
    V = verts(E)
    n = len(V)
    out = []
    for k in (1, 2, 3):  # number of old vertices in the new edge
        for old in combinations(V, k):
            new = tuple(range(n, n + 3 - k))
            e = tuple(sorted(old + new))
            if e in E:
                continue
            E2 = sorted(E + [e])
            if is_linear(E2):
                out.append(E2)
    return out


def canon_key(E):
    """Cheap invariant to cut duplicates (not a full canonical form: we keep all, the
    invariant only groups for reporting)."""
    V = verts(E)
    deg = sorted(sum(1 for e in E if x in e) for x in V)
    return (len(V), len(E), tuple(deg))


level = [[(0, 1, 2)]]
allc = [[(0, 1, 2)]]
seen = {tuple(level[0])}
for m in (2, 3, 4):
    nxt = []
    for E in level:
        for E2 in extend(E):
            t = tuple(E2)
            if t not in seen:
                seen.add(t)
                nxt.append(E2)
    level = nxt
    allc += nxt
print('labelled connected linear configurations with <=4 edges:', len(allc))
bad = 0
keys = {}
rng = random.Random(5)
for E in allc:
    n = len(verts(E))
    ok, info = decide(E, n, rng, want_exact=True)
    if ok:
        pt = info['point']
        assert is_45_bruteforce(pt)
        assert ap_edges_of_points(pt) == set(E)
    else:
        bad += 1
        print('NOT exactly realizable:', E, info)
    keys[canon_key(E)] = keys.get(canon_key(E), 0) + 1
print('invariant classes (n, m, degree sequence):', len(keys))
print('not exactly realizable:', bad)
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
ok, info = decide(F7, 7, rng)
print('F7 realizable (any extra APs):', ok, info.get('stats'))
sub_ok = True
for i in range(5):
    E = F7[:i] + F7[i + 1:]
    ok2, inf2 = decide(E, 7, rng, want_exact=True)
    sub_ok = sub_ok and ok2
print('all 4-edge sub-hypergraphs of F7 exactly realizable:', sub_ok)
