"""Referee L013 r1: independent decomposition generator + comparison with every recursion branch of the prover's cell files.
A decomposition of (N, M) with total slack S = multiset of component types summing to (N, M) with slack sum S, where
 - isolated vertex (1,0,0): slack 3;
 - connected type (p, q, r): p >= 3, ceil((p-1)/2) <= q <= p-2, 1 <= r <= q, slack 3p+2q-11r >= 0 (I11 below n), [optional K8: 17r <= 5p+3q].
Method: partition-first (integer partitions of N into parts 1 or >= 3, non-increasing), then for each part a type, types
non-increasing within equal part sizes, with pruning on remaining edges and slack."""
import sys, os, json, re, glob, math
def types_of(p, S, useK8):
    if p == 1: return [(1, 0, 0)] if S >= 3 else []
    out = []
    for q in range(-(-(p - 1) // 2), p - 1):
        for r in range(1, q + 1):
            s = 3 * p + 2 * q - 11 * r
            if 0 <= s <= S and (not useK8 or 17 * r <= 5 * p + 3 * q): out.append((p, q, r))
    return out
def slack(t): return 3 * t[0] + 2 * t[1] - 11 * t[2]
def partitions(n, maxp):
    if n == 0: yield []; return
    for p in range(min(n, maxp), 0, -1):
        if p == 2: continue
        for rest in partitions(n - p, p): yield [p] + rest
def decomps(N, M, S, useK8=True):
    sols = set()
    for part in partitions(N, N):
        tl = [types_of(p, S, useK8) for p in part]
        if any(not x for x in tl): continue
        def rec(i, m, s, chosen):
            if m > M or s > S: return
            if i == len(part):
                if m == M and s == S: sols.add(tuple(sorted(chosen)))
                return
            for t in tl[i]:
                # non-increasing order among equal part sizes to limit duplicates (set removes the rest)
                if i > 0 and part[i - 1] == part[i] and t > chosen[-1]: continue
                rec(i + 1, m + t[1], s + slack(t), chosen + [t])
        rec(0, 0, 0, [])
    return sorted(sols)
if __name__ == '__main__':
    celldir = sys.argv[1]
    nbr = 0; ndec = 0; bad = 0; k8diff = 0
    top = {(23,13,9,2),(23,14,9,3),(23,20,10,3),(24,12,9,2),(24,13,9,3),(24,18,10,3),(25,16,10,2),(25,17,10,3),(25,22,11,3),(26,14,10,2),(26,15,10,3),(26,21,11,3)}
    for fn in sorted(glob.glob(os.path.join(celldir, 'cell_*.txt'))):
        key = tuple(map(int, re.findall(r'\d+', os.path.basename(fn))))
        n, m, t, D = key
        info = None
        for l in open(fn):
            if l.startswith('INFO '): info = json.loads(l[5:])
        if info is None or info.get('route') != 'recurse': continue
        # expected branch set
        exp = set()
        for d in range(max(1, -(-3 * m // n)), D + 1):
            for tp in (t - 1, t):
                Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
                if Sp >= 0 and tp >= 0: exp.add((d, tp, Sp))
        got = set((b['d'], b['tp'], b['Sp']) for b in info['branches'])
        if exp != got: print('BRANCH SET MISMATCH', key, exp, got); bad += 1
        for b in info['branches']:
            d, tp, Sp = b['d'], b['tp'], b['Sp']; nbr += 1
            mine = decomps(n - 1, m - d, Sp, True)
            mine_noK8 = decomps(n - 1, m - d, Sp, False)
            if mine != mine_noK8: k8diff += 1; print('K8 MATTERS', key, d, tp, Sp, set(mine_noK8) - set(mine))
            theirs = sorted(tuple(sorted(tuple(c) for c in dec)) for dec, size in b['dec'])
            ndec += len(mine)
            # tau consistency
            for dec in mine:
                assert sum(c[2] for c in dec) == tp, (key, dec)
            if mine != theirs:
                bad += 1; print('DECOMP MISMATCH', key, d, tp, Sp, 'mine-theirs', set(mine) - set(theirs), 'theirs-mine', set(theirs) - set(mine))
            if key in top:
                print('TOP', key, 'd=%d tp=%d S\'=%d: %d decompositions (mine), %d (engine) %s' % (d, tp, Sp, len(mine), len(theirs), 'EQUAL' if mine == theirs else 'DIFF'))
    print('recursion branches %d, decompositions %d, mismatches %d, branches where K8 changes the list %d' % (nbr, ndec, bad, k8diff))
    # Remark 5 decompositions
    for (N, M, S) in [(26, 22, 1), (25, 19, 3), (22, 18, 3), (22, 17, 1)]:
        a = decomps(N, M, S, True); b = decomps(N, M, S, False)
        print('decomp (%d,%d) S=%d: %d (K8) %d (no K8) %s' % (N, M, S, len(a), len(b), a if len(a) <= 15 else ''))
