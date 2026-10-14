"""Check every ordered leaf verdict printed by sat3 printall mode against the definitions (pure Python).
E: AP count != n-2;  N: AP set ok but not (4,5);  A: (4,5) with printed h (exhaustive check)."""
import sys, gzip
from itertools import combinations
n = int(sys.argv[1]); fn = sys.argv[2]
def is45(X): return all(len({b - a, c - a, d - a, c - b, d - b, d - c}) >= 5 for a, b, c, d in combinations(X, 4))
def sidon(S):
    d = [b - a for a, b in combinations(S, 2)]; return len(d) == len(set(d))
def hmax(X):
    for k in range(len(X), 0, -1):
        if any(sidon(S) for S in combinations(X, k)): return k
def napc(X):
    s = set(X); return sum(1 for a, c in combinations(X, 2) if (a + c) % 2 == 0 and (a + c) // 2 in s)
cnt = {}; bad = 0
for line in gzip.open(fn, 'rt'):
    t = line.split(); tag = t[0]
    if tag not in 'EAN' or len(tag) != 1: continue
    X = [int(v) for v in t[1:1 + n]]; assert X == sorted(set(X))
    if tag == 'E': ok = napc(X) != n - 2 and not is45(X)
    elif tag == 'N': ok = napc(X) == n - 2 and not is45(X)
    else: ok = napc(X) == n - 2 and is45(X) and hmax(X) == int(t[1 + n][2:])
    cnt[tag] = cnt.get(tag, 0) + 1
    if not ok: bad += 1; print("BAD", line.strip())
print("dbgcheck n=%d" % n, cnt, "bad=%d" % bad)
