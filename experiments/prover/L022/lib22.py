"""L022 helper library: exact routines for AP hypergraphs of finite (4,5)-sets (class R).
All arithmetic exact (int / Fraction). Reuses the L017 transversal routines (hyp.py)."""
import sys, itertools, json
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757')
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017')
import hyp  # tau_masks, all_min_transversals, masks, components, contains_F7, is_linear, p3_ok
from e757.core import is_45_set

def ap_triples(A):
    """all 3-term APs of the sorted list A as rank triples (i,j,k), i<j<k, x_j midpoint."""
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}; out = []
    for i in range(len(A)):
        for k in range(i + 2, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and s // 2 in idx:
                out.append((i, idx[s // 2], k))
    return out

def is_45(A):
    return is_45_set(sorted(A))

def roles(n, E):
    """for each rank v: (#APs with v as left end, as midpoint, as right end)."""
    L = [0] * n; M = [0] * n; R = [0] * n
    for (i, j, k) in E:
        L[i] += 1; M[j] += 1; R[k] += 1
    return L, M, R

def deg(n, E):
    d = [0] * n
    for e in E:
        for x in e: d[x] += 1
    return d

def tau(E):
    return hyp.tau_masks(hyp.masks(E))

def slack(n, E):
    return 3 * n + 2 * len(E) - 11 * tau(E)

def induced(E, S):
    S = set(S); return [e for e in E if all(x in S for x in e)]

def relabel(S, E):
    S = sorted(S); idx = {v: i for i, v in enumerate(S)}
    return len(S), [tuple(sorted(idx[x] for x in e)) for e in E if all(x in idx for x in e)], idx

def min_transversals(E):
    em = hyp.masks(E)
    res, t = hyp.all_min_transversals(em)
    return res, t

def k30_ok(E):
    """K30: (i,j,k),(i2,j2,k2) with i<=i2, k<=k2, (i,k)!=(i2,k2) => j<j2."""
    for (i, j, k), (a, b, c) in itertools.permutations(E, 2):
        if i <= a and k <= c and (i, k) != (a, c) and not j < b:
            return False
    return True

def medial_triangle(E):
    """K31 configuration: APs with endpoint pairs {a,c},{a,e},{c,e} (a triangle of endpoint pairs)."""
    ends = {}
    for (i, j, k) in E: ends[(i, k)] = j
    S = set(ends)
    pts = sorted({x for p in S for x in p})
    for (a, c) in S:
        for e in pts:
            if e != a and e != c and (min(a, e), max(a, e)) in S and (min(c, e), max(c, e)) in S:
                return True
    return False
