"""Sanity check on realizable data: 14-point (4,5)-sets with exactly 11 APs obtained as (class + one point x in a new AP)
minus one point, for the first K census classes of data/census_n14_m12_classes.jsonl.gz.  Theorem 2 predicts h >= 9 for all.
Exact integers (sets scaled by 4); h by e757.core.alpha (= h for weak Sidon sets, K4)."""
import sys, json, gzip, itertools, collections
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import ap_edges, alpha
K = int(sys.argv[1])
def nd(q): return len({abs(u - v) for u, v in itertools.combinations(q, 2)})
hist = collections.Counter(); nsets = 0; seen = set(); ncls = 0
for line in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt'):
    if ncls >= K: break
    ncls += 1
    A = sorted(4 * a for a in json.loads(line)['set']); S = set(A)
    cand = set()
    for a, b in itertools.combinations(A, 2): cand |= {(a + b) // 2, 2 * a - b, 2 * b - a}
    cand -= S
    tr = list(itertools.combinations(A, 3))
    for x in sorted(cand):
        if not all(nd((x,) + q) >= 5 for q in tr): continue
        B = sorted(A + [x])
        for u in B:
            C = [y for y in B if y != u]
            E = ap_edges(C)
            if len(E) != 11: continue
            g = min(C); key = (ncls, tuple(y - g for y in C))
            if key in seen: continue
            seen.add(key); nsets += 1; hist[alpha(C, E)] += 1
print('classes', ncls, '14-point (4,5)-sets with m = 11 (distinct per class):', nsets, 'histogram of h:', dict(sorted(hist.items())))
json.dump(dict(classes=ncls, sets=nsets, h_hist=dict(hist)), open('sanity_m11_sets_K%d.json' % K, 'w'))
