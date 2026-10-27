"""G1 shrink: library. Exact integer arithmetic only. Reuses experiments/prover/L021/kt.py (read-only)."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import Piece, masks, tau_masks, min_transversals

R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))

def load_pieces():
    return [Piece(p['edges'], p['name']) for p in R['pieces']]

def slack(n, m, tau):          # I11 slack s = 3n + 2m - 11 tau
    return 3 * n + 2 * m - 11 * tau

def popcount(x): return bin(x).count('1')

# ---------- membership in C: linear, F7-free, e(S) <= |S|-2 for all |S| >= 2 ----------
def is_linear(em):
    for a, b in itertools.combinations(em, 2):
        if popcount(a & b) > 1: return False
    return True

def has_F7(em):
    inc = {}
    for i, f in enumerate(em):
        x = f
        while x:
            b = x & -x; x ^= b; inc.setdefault(b, []).append(i)
    for c, es in inc.items():
        if len(es) < 3: continue
        for A, B, C in itertools.combinations(es, 3):
            ok = [f for j, f in enumerate(em) if j not in (A, B, C) and not f & c
                  and all(f & (em[X] & ~c) for X in (A, B, C))]
            for f, g in itertools.combinations(ok, 2):
                if not f & g: return True
    return False

def p3_ok(n, em):
    """e(S) <= |S|-2 for all S, |S|>=2.  Equivalent (Hall) to: for every pair {a,b} there is an injective map
    edges -> vertices \\ {a,b} with e -> a vertex of e."""
    m = len(em)
    if m > n - 2: return False
    for a in range(n):
        for b in range(a + 1, n):
            ex = ~((1 << a) | (1 << b))
            match = {}          # vertex -> edge
            def aug(e, seen):
                x = em[e] & ex
                while x:
                    bt = x & -x; x ^= bt
                    if bt in seen: continue
                    seen.add(bt)
                    if bt not in match or aug(match[bt], seen):
                        match[bt] = e; return True
                return False
            for e in range(m):
                if not aug(e, set()): return False
    return True

def in_C(n, edges):
    em = masks(edges)
    return is_linear(em) and not has_F7(em) and p3_ok(n, em)

def p3_bruteforce(n, edges):
    """independent check by spans of edge subsets (slow; for validation only)"""
    em = masks(edges); m = len(em); seen = set()
    def rec(i, U, k):
        if k >= 1 and U not in seen:
            seen.add(U)
            if sum(1 for f in em if f & U == f) > popcount(U) - 2: return False
        for j in range(i, m):
            if not rec(j + 1, U | em[j], k + 1): return False
        return True
    return rec(0, 0, 0)

def induced(n, edges, U):
    """induced subgraph on vertex set U (iterable), relabelled 0..|U|-1"""
    U = sorted(U); idx = {x: i for i, x in enumerate(U)}
    return len(U), [tuple(idx[x] for x in e) for e in edges if all(x in idx for x in e)]
