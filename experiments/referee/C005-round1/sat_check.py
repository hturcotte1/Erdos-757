"""Referee C005: SAT decision of 'Sidon subset of size >= k' on the DIRECT sum-collision encoding.
Own sequential-counter (Sinz 2005) cardinality encoding, pysat solvers only as black boxes.
Usage: python3 sat_check.py <claim.json> <k> [solver]"""
import sys, time
sys.path.insert(0, '.')
from common import *
from pysat.solvers import Solver

def seq_atmost(lits, K, top):
    """Clauses for sum(lits) <= K (Sinz LTseq). Returns (clauses, top)."""
    n = len(lits); cls = []
    if K >= n:
        return cls, top
    if K == 0:
        return [[-l] for l in lits], top
    s = [[0] * (K + 1) for _ in range(n)]
    for i in range(n - 1):
        for j in range(1, K + 1):
            top += 1; s[i][j] = top
    cls.append([-lits[0], s[0][1]])
    for j in range(2, K + 1):
        cls.append([-s[0][j]])
    for i in range(1, n - 1):
        cls.append([-lits[i], s[i][1]])
        cls.append([-s[i - 1][1], s[i][1]])
        for j in range(2, K + 1):
            cls.append([-lits[i], -s[i - 1][j - 1], s[i][j]])
            cls.append([-s[i - 1][j], s[i][j]])
        cls.append([-lits[i], -s[i - 1][K]])
    cls.append([-lits[n - 1], -s[n - 2][K]])
    return cls, top

def build(A, k):
    n = len(A)
    F, by_sum = forbidden_sets_from_sums(A)   # every relation x+y=z+w, {x,y}!={z,w}
    cls = [[-(u + 1) for u in sorted(f)] for f in F]
    # at least k chosen  <=>  at most n-k NOT chosen
    card, top = seq_atmost([-(i + 1) for i in range(n)], n - k, n)
    return cls + card, len(F), top

def decide(A, k, name='cadical195'):
    cls, nF, top = build(A, k)
    t = time.time()
    with Solver(name=name, bootstrap_with=cls) as s:
        res = s.solve()
        model = s.get_model() if res else None
        stats = s.accum_stats() if hasattr(s, 'accum_stats') else {}
    dt = time.time() - t
    W = None
    if res:
        W = [A[i] for i in range(len(A)) if model[i] > 0]
        assert len(W) >= k and is_sidon_def(W) and is_sidon_diff(W), 'model check failed'
    return res, W, dt, nF, len(cls), top, stats

if __name__ == '__main__':
    raw, pts = load_claim(sys.argv[1]); A = sorted(pts)
    k = int(sys.argv[2]); name = sys.argv[3] if len(sys.argv) > 3 else 'cadical195'
    res, W, dt, nF, ncl, top, st = decide(A, k, name)
    print(f'solver={name} n={len(A)} k={k} relations={nF} clauses={ncl} vars={top} -> {"SAT" if res else "UNSAT"} in {dt:.2f}s stats={st}')
    if res:
        print('  model re-verified Sidon (sums and diffs), size', len(W))
