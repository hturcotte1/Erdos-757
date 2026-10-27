# Independent exact realizability test (referee 1, L022 round 1).
# A labelled configuration = list of (a, mid, c) on vertices 0..n-1.
# Decision for one labelling: compute the solution space V of the AP equations
# (exact nullspace basis over Q), and test which forms of Phi vanish identically on V:
#   X_i - X_j                    -> forced equal points          (dead)
#   X_i + X_j - X_k - X_l, {i,j} and {k,l} disjoint -> forced weak-Sidon violation (dead)
#   X_i + X_k - 2 X_j            -> forced AP; dead if the forced APs are not linear
# If not dead, the generic point of V is a (4,5)-set whose AP hypergraph is exactly
# the forced APs (a superset of the configuration).  Soundness of "dead": the vanishing
# relation holds at every point of V, hence at every realization with this labelling.
# Completeness: every realization (as a sub-hypergraph) has some labelling.
from fractions import Fraction
from itertools import combinations, product
import random
from rlib import nullspace, is_45_fast, is_45_bruteforce, ap_triples


def forced_data(n, labelled):
    rows = []
    for (a, b, c) in labelled:
        v = [0] * n
        v[a] += 1
        v[c] += 1
        v[b] -= 2
        rows.append(v)
    B = nullspace(rows, n)  # list of basis vectors (length n)
    # coordinates of vertex i in the basis: column i of B
    col = [tuple(B[k][i] for k in range(len(B))) for i in range(n)]
    return B, col


def labelling_status(n, labelled):
    """Return ('dead', reason) or ('ok', forced_aps, basis)."""
    B, col = forced_data(n, labelled)
    k = len(B)
    # equal points
    seen = {}
    for i in range(n):
        if col[i] in seen:
            return ('dead', 'equal %d %d' % (seen[col[i]], i))
        seen[col[i]] = i
    # pair sums
    sums = {}
    for i, j in combinations(range(n), 2):
        s = tuple(col[i][t] + col[j][t] for t in range(k))
        if s in sums:
            (p, q) = sums[s]
            # pairs are disjoint here (shared element would mean equal points)
            return ('dead', 'parallelogram %s %s' % ((p, q), (i, j)))
        sums[s] = (i, j)
    # forced APs: 2 col[j] = col[i] + col[k]
    forced = []
    for j in range(n):
        two = tuple(2 * x for x in col[j])
        if two in sums:
            i, kk = sums[two]
            if j not in (i, kk):
                forced.append((i, j, kk))
    # linearity of forced APs
    pairs = set()
    for e in forced:
        for p in combinations(sorted(e), 2):
            if p in pairs:
                return ('dead', 'nonlinear forced APs')
            pairs.add(p)
    return ('ok', forced, B)


def explicit_point(n, B, rng, tries=200, bound=10**6):
    for _ in range(tries):
        coef = [rng.randint(-bound, bound) for _ in B]
        x = [sum(coef[t] * B[t][i] for t in range(len(B))) for i in range(n)]
        # clear denominators
        from math import lcm
        L = 1
        for v in x:
            L = lcm(L, Fraction(v).denominator)
        xi = [int(v * L) for v in x]
        if len(set(xi)) == n and is_45_fast(xi):
            return xi
    return None


def ap_edges_of_points(xi):
    pts = {i: xi[i] for i in range(len(xi))}
    return set(tuple(sorted(t)) for t in ap_triples(pts))


def all_labellings(edges):
    return product(*[[(tuple(x for x in e if x != b)[0], b, tuple(x for x in e if x != b)[1]) for b in e] for e in edges])


def decide(edges, n, rng=None, want_exact=False, max_lab=None):
    """Exhaustive over all 3^m labellings. Returns (realizable?, info)."""
    rng = rng or random.Random(1)
    count = 0
    stats = {}
    for lab in all_labellings(edges):
        count += 1
        mids = [t[1] for t in lab]
        st = labelling_status(n, list(lab))
        if st[0] == 'dead':
            key = st[1].split()[0]
            stats[key] = stats.get(key, 0) + 1
            continue
        forced, B = st[1], st[2]
        fs = set(tuple(sorted(e)) for e in forced)
        es = set(tuple(sorted(e)) for e in edges)
        if want_exact and fs != es:
            stats['extra'] = stats.get('extra', 0) + 1
            continue
        xi = explicit_point(n, B, rng)
        if xi is None:
            stats['nopoint'] = stats.get('nopoint', 0) + 1
            continue
        got = ap_edges_of_points(xi)
        assert got == fs, (got, fs)
        assert es <= got
        return True, {'labelling': lab, 'point': xi, 'aps': sorted(got), 'labellings_tried': count, 'stats': stats}
    return False, {'labellings_tried': count, 'stats': stats}
