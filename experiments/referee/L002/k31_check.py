"""Referee L002: recompute the medial-triangle (K31) flag with my own definition on every canonical pattern of the
census filtered file, compare with the census flag; emit the census O' subset (k30=k31=c4=1) for re-realization."""
import gzip, sys, itertools
def medial(es):
    for e1, e2, e3 in itertools.combinations(es, 3):
        s12 = set(e1) & set(e2); s13 = set(e1) & set(e3); s23 = set(e2) & set(e3)
        if len(s12) != 1 or len(s13) != 1 or len(s23) != 1: continue
        (a,), (b,), (c,) = s12, s13, s23
        if len({a, b, c}) != 3: continue
        # each shared vertex must be an endpoint (not the midpoint) of both edges containing it
        if a in (e1[1], e2[1]) or b in (e1[1], e3[1]) or c in (e2[1], e3[1]): continue
        return True
    return False
tot = agree = k31free = c4sub = 0
out = open(sys.argv[2], "w")
for line in gzip.open(sys.argv[1], "rt"):
    f = line.split()
    fl = list(map(int, f[:4])); es = [tuple(map(int, t.split(","))) for t in f[4:]]
    tot += 1
    mine_free = not medial(es)
    agree += (mine_free == bool(fl[1]))
    k31free += mine_free
    if fl[0] and fl[1] and fl[2]:
        c4sub += 1
        out.write(" ".join("%d,%d,%d" % e for e in es) + "\n")
print(f"canonical patterns={tot} my_K31_free={k31free} agree_with_census_flag={agree} census_O'_subset={c4sub}")
