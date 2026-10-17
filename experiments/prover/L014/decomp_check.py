"""(L014) Cross-check (a): for every recursion cell of a dry-run tree (tree.py output) and every branch (d, t', S'), the decomposition
list of engine.decompositions(n-1, m-d, S') is compared with an independent brute force written here from scratch:
  all partitions of N = n-1 into parts equal to 1 or >= 3 (a component of a 3-graph has 1 or >= 3 vertices); for each part p every
  type (p, mp, tp) allowed for a connected member of C with slack in [0, S] (p = 1: (1,0,0), slack 3; p >= 3: n <= 2m+1 i.e.
  mp >= ceil((p-1)/2), mp <= p-2 by (P3), 1 <= tp <= mp, 17 tp <= 5p + 3mp (K8), 0 <= 3p + 2mp - 11 tp <= S); the Cartesian product of
  the per-part type lists, kept iff sum mp = M and the slacks add to S exactly; compared as sets of sorted tuples.
Also prints the five decompositions of (22,18) with total slack 3.  Exact integer arithmetic only."""
import sys, os, re, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
def partitions(N, maxp=None):
    if maxp is None: maxp = N
    if N == 0: yield (); return
    for p in range(min(N, maxp), 0, -1):
        if p == 2: continue
        for rest in partitions(N - p, p): yield (p,) + rest
def types_of(p, S):
    if p == 1: return [(1, 0, 0)] if S >= 3 else []
    out = []
    for mp in range((p - 1 + 1) // 2, p - 1):          # ceil((p-1)/2) .. p-2
        if p > 2 * mp + 1: continue
        for tp in range(1, mp + 1):
            s = 3 * p + 2 * mp - 11 * tp
            if 0 <= s <= S and 17 * tp <= 5 * p + 3 * mp: out.append((p, mp, tp))
    return out
def slack(c): return 3 * c[0] + 2 * c[1] - 11 * c[2]
def bf(N, M, S):
    sols = set()
    for part in partitions(N):
        lists = [types_of(p, S) for p in part]
        if any(not l for l in lists): continue
        for combo in itertools.product(*lists):
            if sum(c[1] for c in combo) == M and sum(slack(c) for c in combo) == S: sols.add(tuple(sorted(combo)))
    return sols
if __name__ == '__main__':
    tree = sys.argv[1]; n_br = 0; n_dec = 0; bad = 0
    for l in open(tree):
        if not l.startswith('CELL') or ' recurse ' not in l: continue
        n, m, t, D = map(int, re.match(r'CELL \((\d+), (\d+), (\d+), (\d+)\)', l).groups())
        for d, tp, S in re.findall(r'\[d=(\d+) tp=(\d+) S=(\d+) decs=\d+\]', l):
            d, tp, S = int(d), int(tp), int(S)
            assert S == 3 * (n - 1) + 2 * (m - d) - 11 * tp
            e = set(tuple(sorted(x)) for x in engine.decompositions(n - 1, m - d, S)); b = bf(n - 1, m - d, S)
            assert len(e) == len(engine.decompositions(n - 1, m - d, S)), 'engine list has duplicates'
            ok = (e == b); n_br += 1; n_dec += len(e); bad += (not ok)
            print('cell (%d,%d,%d,%d) branch d=%d tp=%d S=%d: (%d,%d) engine %d brute force %d %s' % (n, m, t, D, d, tp, S, n - 1, m - d, len(e), len(b), 'EQUAL' if ok else 'DIFFERENT'))
            if not ok: print('   only engine:', sorted(e - b), ' only bf:', sorted(b - e))
    print('SUMMARY branches %d decompositions %d differences %d' % (n_br, n_dec, bad))
    print('The decompositions of (22,18) with total slack 3:')
    for x in sorted(bf(22, 18, 3)): print('   ', list(x))
