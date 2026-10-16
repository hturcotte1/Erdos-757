"""stdin version of dbgcheck: checks ALL 'A' lines with h != T and every k-th other verdict line."""
import sys
from itertools import combinations
n, T, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
def is45(X): return all(len({b - a, c - a, d - a, c - b, d - b, d - c}) >= 5 for a, b, c, d in combinations(X, 4))
def sidon(S):
    d = [b - a for a, b in combinations(S, 2)]; return len(d) == len(set(d))
def hmax(X):
    for kk in range(len(X), 0, -1):
        if any(sidon(S) for S in combinations(X, kk)): return kk
def napc(X):
    s = set(X); return sum(1 for a, c in combinations(X, 2) if (a + c) % 2 == 0 and (a + c) // 2 in s)
cnt = {}; chk = {}; bad = 0; i = 0
for line in sys.stdin:
    t = line.split(); tag = t[0]
    if len(tag) != 1 or tag not in 'EAN': continue
    i += 1
    hT = tag == 'A' and int(t[1 + n][2:]) != T
    key = tag + ('>' if hT else '')
    cnt[key] = cnt.get(key, 0) + 1
    if not hT and i % k: continue
    X = [int(v) for v in t[1:1 + n]]; ok = X == sorted(set(X))
    if tag == 'E': ok &= napc(X) != n - 2 and not is45(X)
    elif tag == 'N': ok &= napc(X) == n - 2 and not is45(X)
    else: ok &= napc(X) == n - 2 and is45(X) and hmax(X) == int(t[1 + n][2:])
    chk[key] = chk.get(key, 0) + 1
    if not ok: bad += 1; print("BAD", line.strip())
print("dbgcheck2 n=%d lines" % n, cnt, "checked", chk, "bad=%d" % bad)
