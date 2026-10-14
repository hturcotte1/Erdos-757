"""Compare my realized canonical sets with the census list results/realized_n12.json.gz (normalized independently)."""
import gzip, json
from math import gcd
from collections import Counter, defaultdict
N = 12
def norm(A):
    A = sorted(A); v = [x - A[0] for x in A]; g = 0
    for x in v: g = gcd(g, x)
    v = [x // g for x in v]; r = sorted(v[-1] - x for x in v)
    return tuple(min(v, r))
def refl(edges):
    return tuple(sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in edges))
mine = defaultdict(list)
labelled = set()
for line in gzip.open("my_realized.txt.gz", "rt"):
    a, s, h = line[1:].split("|")
    E = tuple(sorted(tuple(map(int, t.split(","))) for t in a.split()))
    S = tuple(map(int, s.split()))
    assert h.strip() == "h=7"
    assert norm(S) == S
    mine[S].append(E); labelled.add(E)
mult = Counter(len(v) for v in mine.values())
pairs_ok = all(len(v) == 2 and refl(v[0]) == v[1] or (len(v) == 2 and refl(v[1]) == v[0]) for v in mine.values())
self_sym = sum(1 for E in labelled if refl(E) == E)
print("my labelled realizable:", len(labelled), "distinct canonical sets:", len(mine), "multiplicities:", dict(mult),
      "each class = {P, refl(P)}:", pairs_ok, "self-symmetric:", self_sym)
theirs = json.load(gzip.open("/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz", "rt"))
tset = Counter(norm(r["set"]) for r in theirs)
tpat = set(tuple(sorted(tuple(e) for e in r["edges"])) for r in theirs)
print("theirs entries:", len(theirs), "distinct normalized sets:", len(tset), "max multiplicity:", max(tset.values()))
print("theirs - mine:", len(set(tset) - set(mine)), " mine - theirs:", len(set(mine) - set(tset)))
# their patterns must be one of the two labelled patterns of the class
bad = sum(1 for r in theirs if tuple(sorted(tuple(e) for e in r["edges"])) not in labelled)
print("their labelled patterns not in my realizable list:", bad)
print("their h all 7:", all(r["h"] == 7 for r in theirs), " their is_45 all:", all(r["is_45"] for r in theirs))
# known sets
for line in open("known_patterns.txt"):
    pat, rest = line.split("#"); name, S = rest.split(" ", 2)[1:]
    S = tuple(json.loads(S))
    E = tuple(sorted(tuple(map(int, t.split(","))) for t in pat.split()))
    print("known", name, "class in mine:", S in mine, " in theirs:", S in tset, " pattern realizable in mine:", E in labelled)
