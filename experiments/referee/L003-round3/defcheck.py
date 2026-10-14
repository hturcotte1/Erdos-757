"""Re-check output sets of sat3 from the definitions only (pure Python, ints).
usage: python3 -I defcheck.py n T file [sample_size seed]
For each 'S' line: strictly increasing, min 0, gcd 1, lex <= reflection; every 4-subset has >= 5 distinct
distances; the 3-APs are exactly n-2, one per interior point; largest Sidon subset (all pairwise
differences distinct; exhaustive over subsets, largest first) has size exactly T."""
import sys, gzip, random, math
from itertools import combinations
n, T, fn = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
op = gzip.open if fn.endswith('.gz') else open
sets = [tuple(int(v) for v in l.split()[1:1 + n]) for l in op(fn, 'rt') if l.startswith('S ')]
if len(sys.argv) > 4:
    random.seed(int(sys.argv[5])); sets = random.sample(sets, min(int(sys.argv[4]), len(sets)))
def is_sidon(S):
    d = [b - a for a, b in combinations(S, 2)]
    return len(d) == len(set(d))
def hmax(X):
    for k in range(len(X), 0, -1):
        if any(is_sidon(S) for S in combinations(X, k)): return k
bad = 0
for X in sets:
    ok = list(X) == sorted(set(X)) and X[0] == 0 and math.gcd(*X) == 1
    refl = tuple(X[-1] - v for v in reversed(X)); ok &= X <= refl
    ok &= all(len({b - a, c - a, d - a, c - b, d - b, d - c}) >= 5 for a, b, c, d in combinations(X, 4))
    S = set(X); aps = [(a, (a + c) // 2, c) for a, c in combinations(X, 2) if (a + c) % 2 == 0 and (a + c) // 2 in S]
    ok &= len(aps) == n - 2 and sorted(m for _, m, _ in aps) == list(X[1:-1])
    # h: no Sidon subset of size T+1, at least one of size T
    ok &= not any(is_sidon(Q) for Q in combinations(X, T + 1)) and any(is_sidon(Q) for Q in combinations(X, T))
    if not ok: bad += 1; print("BAD", X)
print("defcheck n=%d T=%d checked=%d bad=%d" % (n, T, len(sets), bad))
