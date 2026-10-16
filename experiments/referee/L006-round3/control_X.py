"""Positive control for route_X.run_class (called unmodified): A = A_base - {p,u,v} (11 points) with h(A) = 7, so that
B = A_base - {p} (13 points, (4,5), h = 8 <= h(A)+1) is a deficient (4,5) 2-extension of A. Route X must flag (4u,4v) when u or v
is in P_x(A) (its case (i)); otherwise case (ii) requires a vertex in all maximum Sidon sets of A, reported as 'core'."""
import itertools, json, sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L006-round3')
import route_X as X
Ab = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
def h(S):
    for k in range(len(S), 0, -1):
        if any(X.is_sidon(T) for T in itertools.combinations(S, k)): return k
def third(P):
    out = set()
    for a, b in itertools.combinations(P, 2):
        if (a + b) % 2 == 0: out.add((a + b) // 2)
        out.add(2 * a - b); out.add(2 * b - a)
    return out - set(P)
done = 0; tested = []
for p in Ab:
    B = [a for a in Ab if a != p]
    assert h(B) == 8
    for u, v in itertools.combinations(B, 2):
        A = [a for a in B if a not in (u, v)]
        if h(A) != 7: continue
        r = X.run_class(0, A)   # integer tag 0: spot mode (slow Y_x recomputation, per-pair Sidon re-verification)
        pts = [tuple(f[1:]) for f in r['flags'] if f[0] == 'deficient (4,5) pair']
        hit = (str(4 * u), str(4 * v)) in pts or (str(4 * v), str(4 * u)) in pts
        inPx = (u in third(A)) or (v in third(A))
        tested.append((p, u, v, inPx, hit, len(pts), r['core']))
        if len(tested) >= 12: break
    if len(tested) >= 12: break
for t in tested:
    print('A_base-{%d,%d,%d}: u or v in P_x(A): %s; flagged: %s; deficient (4,5) pairs flagged: %d; core: %s' % t)
print('controls', len(tested), 'all (case (i)) detected:', all(t[4] for t in tested if t[3]), '; case (ii) controls:', sum(1 for t in tested if not t[3]))
