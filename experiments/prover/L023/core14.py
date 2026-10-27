"""(L023) Minimal non-realizable tight pieces of classes 5 and 7 of cell(14,12,6,4): all vertex sets S with e(S) = |S| - 2 (tight),
each induced piece tested with realize_sdr.decide (saturated on S); report the smallest non-realizable tight S (if any besides V)."""
import sys, re, itertools, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from realize_sdr import decide
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
L = [parse(l) for l in open('topcell/cells/cell_14_12_6_D4.txt') if l.startswith('FOUND:')]
for ci in (5, 7):
    E = L[ci]; n = 14
    tight = []
    for r in range(3, 15):
        for S in itertools.combinations(range(n), r):
            s = set(S); ES = [e for e in E if set(e) <= s]
            if len(ES) == r - 2: tight.append((r, S, ES))
    res = []
    for r, S, ES in tight:
        idx = {v: i for i, v in enumerate(S)}
        st, ex = decide([tuple(idx[v] for v in e) for e in ES], r)
        res.append((r, S, bool(st['REAL'])))
    nonreal = [(r, S) for r, S, ok in res if not ok]
    minr = min(r for r, S in nonreal)
    print('class %d: tight sets %d (sizes %s); non-realizable tight sets %d; smallest size %d: %s' % (ci, len(tight), sorted(set(r for r, S, ES in tight)), len(nonreal), minr, [S for r, S in nonreal if r == minr][:5]), flush=True)
