"""Referee L002: duplicates and reflection closure of the DFS output (codes written by realize12.c),
and comparison of the realizable list with the census's realized_n12.json.gz."""
import sys, gzip, json
import numpy as np
codes = np.fromfile(sys.argv[1], dtype=np.uint64)
print("codes", len(codes), "distinct", len(np.unique(codes)))
# decode: digit for midpoint j (j=1..10, most significant first) = l*(11-j) + (r-j-1), base j*(11-j)
bases = [j * (11 - j) for j in range(1, 11)]
digs = {}
c = codes.copy()
for j in range(10, 0, -1):
    b = np.uint64(bases[j - 1])
    digs[j] = (c % b).astype(np.int64); c = c // b
assert np.all(c == 0)
L = {j: digs[j] // (11 - j) for j in digs}; R = {j: digs[j] % (11 - j) + j + 1 for j in digs}
for j in L:
    assert np.all(L[j] < j) and np.all(R[j] > j) and np.all(R[j] <= 11)
# reflection: edge (l(j), j, r(j)) -> (11-r(j), 11-j, 11-l(j)); new midpoint j' = 11-j has l' = 11-r(j), r' = 11-l(j)
rc = np.zeros(len(codes), dtype=np.uint64)
for jp in range(1, 11):
    j = 11 - jp
    lp = 11 - R[j]; rp = 11 - L[j]
    dig = lp * (11 - jp) + (rp - jp - 1)
    rc = rc * np.uint64(bases[jp - 1]) + dig.astype(np.uint64)
s = set(codes.tolist())
missing = sum(1 for x in rc.tolist() if x not in s)
print("reflections missing from list:", missing, " self-symmetric:", int(np.sum(rc == codes)))
# realizable comparison
mine = {}
for line in gzip.open(sys.argv[2], "rt"):
    a, b, c2 = line[1:].split("|")
    st = tuple(int(x) for x in a.split())
    mine.setdefault(st, []).append(tuple(tuple(int(y) for y in e.split(",")) for e in b.split()))
print("my realizable labelled lines:", sum(len(v) for v in mine.values()), " distinct canonical sets:", len(mine),
      " multiplicity histogram:", {k: sum(1 for v in mine.values() if len(v) == k) for k in set(len(v) for v in mine.values())})
theirs = json.load(gzip.open(sys.argv[3], "rt"))
def canon_set(v):
    v = sorted(v); v = [x - v[0] for x in v]
    from math import gcd
    g = 0
    for x in v: g = gcd(g, x)
    v = [x // g for x in v]
    r = sorted(v[-1] - x for x in v)
    return tuple(min(v, r))
ts = [canon_set(r["set"]) for r in theirs]
print("theirs entries:", len(theirs), " distinct canonical:", len(set(ts)))
print("theirs - mine:", len(set(ts) - set(mine)), " mine - theirs:", len(set(mine) - set(ts)))
print("their flags: all h=7", all(r["h"] == 7 for r in theirs), " all is_45", all(r["is_45"] for r in theirs), " all rigid", all(r["rigid"] for r in theirs))
mx = max(max(k) for k in mine)
print("max coordinate among canonical normalized sets:", mx)
