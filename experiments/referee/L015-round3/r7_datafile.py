#!/usr/bin/env python3
"""Referee round 3, L015: data/reader_5_9_family.json (read as data only) vs my own I_K, K<=8."""
import json
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
def N(x, j):
    v = x
    for i in range(1, j + 1):
        v = 101 * 269 ** i + 18 * v
    return v
def I(K):
    return sorted({269 ** (K - j) * N(x, j) for j in range(K + 1) for x in O})
d = json.load(open("/home/user/Erdos-757/data/reader_5_9_family.json"))
fam = {m["K"]: m for m in d["family"]}
print("keys in file:", sorted(fam), "| top-level keys:", sorted(d))
ok = True
for K in sorted(fam):
    if K > 8: continue
    s = fam[K]["set"]
    same = sorted(s) == I(K) and all(isinstance(v, int) for v in s)
    ok &= same
    print("K=%d n=%d file==my I_K: %s; other fields: %s" % (K, len(s), same, {k: v for k, v in fam[K].items() if k != 'set'}))
print("DATAFILE OK" if ok else "DATAFILE MISMATCH")
