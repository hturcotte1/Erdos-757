"""Referee round 2, L017: independent re-derivation of the C4 table (Theorem 6(iii), Step 9.3): the d=3 branch decompositions of the
17 top-level violator cells of L013/L016 and their input counts from the stored Delta<=3 lists (counted here by grep of FOUND lines)."""
import math, glob, os
ROOT = '/home/user/Erdos-757/experiments/prover/L017/out'
def conn_ok(n, m, t): return n >= 3 and math.ceil((n-1)/2) <= m <= n-2 and 1 <= t <= m and 17*t <= 5*n+3*m
def slack(n, m, t): return 3*n+2*m-11*t
def stored(n, m, t):
    files = glob.glob('%s/*/cells/cell_%d_%d_%d_D3.txt' % (ROOT, n, m, t)) + glob.glob('%s/L016/cells_new/*/cell_%d_%d_%d_D3.txt' % (ROOT, n, m, t))
    if not files: return None
    counts = set(sum(1 for l in open(f) if l.startswith('FOUND')) for f in files)
    assert len(counts) == 1, (n, m, t, files, counts)
    return counts.pop()
def decomps(N, M, S, smax):
    pieces = [(n, m, t) for n in range(3, N+1) for m in range(1, n-1) for t in range(1, m+1) if 0 <= slack(n, m, t) <= smax and conn_ok(n, m, t)]
    if S >= 3: pieces.append((1, 0, 0))
    sols = set()
    def rec(i, n, m, s, chosen):
        if n == N and m == M and s == S: sols.add(tuple(sorted(chosen))); return
        if i == len(pieces) or n > N or m > M or s > S: return
        pn, pm, pt = pieces[i]; ps = slack(pn, pm, pt); k = 0
        while n + k*pn <= N and m + k*pm <= M and s + k*ps <= S:
            rec(i+1, n+k*pn, m+k*pm, s+k*ps, chosen + [(pn, pm, pt)]*k); k += 1
    rec(0, 0, 0, 0, [])
    return sorted(sols)
TOP = [(23,13,9,2),(23,14,9,3),(23,20,10,3),(24,12,9,2),(24,13,9,3),(24,18,10,3),(25,16,10,2),(25,17,10,3),(25,22,11,3),(26,14,10,2),(26,15,10,3),(26,21,11,3),(27,13,10,2),(27,18,11,2),(27,14,10,3),(27,19,11,3),(27,25,12,3)]
tot = dict(decs=0, r4=0, r4_used=0, r4_inputs=0, empty_T1M=0)
for (n, m, t, D) in TOP:
    s = slack(n, m, t)
    if D <= 2:
        print('(%d,%d,%d,%d) s=%d: Delta<=2 -> empty by Theorem 7 (and s<=-3: by Theorem 1(e))' % (n, m, t, D, s)); tot['empty_T1M'] += 1; continue
    S = s + 2; ds = decomps(n-1, m-3, S, S)
    inputs_le3 = 0; all_zero = True
    print('(%d,%d,%d,%d) s=%d: d=3 branch, (%d,%d) total slack %d: %d decompositions' % (n, m, t, D, s, n-1, m-3, S, len(ds)))
    for d in ds:
        cnts = [stored(*c) for c in d]; inp = 0 if None in cnts else math.prod(cnts); r = len(d)
        tot['decs'] += 1
        if r >= 4:
            tot['r4'] += 1
            if inp: tot['r4_used'] += 1; tot['r4_inputs'] += inp
        else:
            inputs_le3 += inp
            if inp: all_zero = False
        print('    r=%d %s counts=%s inputs=%s%s' % (r, list(d), cnts, inp, '  (void by Theorem 4(iii))' if r >= 4 else ''))
    print('    VERDICT:', 'empty given the stored lists (all r<=3 decompositions have 0 inputs)' if all_zero else 'needs the extension step: %d inputs from r<=3 decompositions' % inputs_le3)
print('TOTALS', tot)
