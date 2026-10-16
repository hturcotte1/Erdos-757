"""Recompute Step 3's numbers: K31 (medial triangle) count with my own definition on the 1,113,245 canonical
patterns of the census filter output, and extract the O' subset (census flags k30=k31=c4=1) for ./realize."""
import gzip, itertools, sys
N = 12
def medial(edges):
    for e1, e2, e3 in itertools.combinations(edges, 3):
        s12 = set(e1) & set(e2); s13 = set(e1) & set(e3); s23 = set(e2) & set(e3)
        if len(s12) != 1 or len(s13) != 1 or len(s23) != 1: continue
        if len(s12 | s13 | s23) != 3: continue
        ok = True
        for e, sh in ((e1, s12 | s13), (e2, s12 | s23), (e3, s13 | s23)):
            if e[1] in sh: ok = False   # shared vertex is the midpoint of e: not medial
        if ok: return True
    return False
canon = k31free = agree = 0
out = open("oprime_patterns.txt", "w")
for line in gzip.open("/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/n12_m10_filtered.txt.gz", "rt"):
    f = line.split(); fl = list(map(int, f[:4]))
    E = [tuple(map(int, t.split(","))) for t in f[4:]]
    canon += 1
    mine = not medial(E)
    k31free += mine
    agree += (mine == bool(fl[1]))
    if fl[0] and fl[1] and fl[2]:
        out.write(" ".join("%d,%d,%d" % e for e in E) + "\n")
out.close()
print("canonical", canon, "my K31-free", k31free, "agree with census flag", agree)
