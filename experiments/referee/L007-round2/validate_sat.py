"""Validate sat_ref.solve_cell against the brute-force tallies bf/bf_n.txt (own brute force) for 3<=n<=NMAX:
for every m in 1..mmax+1, t in 1..taumax+1, D in {1,2,3,None}, f7free in {False,True}:
SAT status must equal 'some labelled connected spanning linear 3-graph with these parameters exists'.
Also every SAT witness is re-checked from scratch (linear, connected, spanning, m, tau, D, F7 via det_A)."""
import sys, json, itertools, time
from sat_ref import solve_cell, components
from f7_ref import det_A, is_linear
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
CONN = sys.argv[2] if len(sys.argv) > 2 else "lazy"
def tau(n, es):
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            if all(set(S) & set(e) for e in es): return k
bad = 0; tot = 0; nonempty = 0; t0 = time.time()
for n in range(3, NMAX + 1):
    bf = {}
    for l in open('bf/bf_%d.txt' % n):
        m, t, d, f, c = map(int, l.split()); bf[(m, t, d, f)] = c
    mmax = max([k[0] for k in bf] + [0]); tmaxall = max([k[1] for k in bf] + [1])
    for m in range(1, mmax + 2):
        for t in range(1, tmaxall + 2):
            for D in (1, 2, 3, None):
                for f7free in (False, True):
                    want = any(c for (mm, tt, dd, ff), c in bf.items() if mm == m and tt >= t and (D is None or dd <= D) and (not f7free or ff == 0))
                    r, edges, info = solve_cell(n, m, t, D, f7free, conn=CONN)
                    got = (r == 'SAT')
                    ok = (got == want)
                    if got:
                        ok &= (len(edges) == m and is_linear(edges) and len(components(n, edges)) == 1 and set().union(*edges) == set(range(n))
                               and tau(n, edges) >= t and (D is None or max(sum(v in e for e in edges) for v in range(n)) <= D)
                               and (not f7free or not det_A(edges)))
                    tot += 1; nonempty += want; bad += (not ok)
                    if not ok: print('MISMATCH', n, m, t, D, f7free, r, edges, want, flush=True)
    print('n=%d done, instances so far %d, mismatches %d, %.1fs' % (n, tot, bad, time.time() - t0), flush=True)
print(json.dumps(dict(instances=tot, nonempty=nonempty, mismatches=bad)))
