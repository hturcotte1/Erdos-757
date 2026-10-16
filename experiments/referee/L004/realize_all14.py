"""Referee L004, check R: exact realization of ALL 205,529 canonical census patterns with the referee's own realizer
(realize14.py), i.e. without the K31 / forbidden-core pre-filters; comparison with the census realizable list.
usage: python3 realize_all14.py CENSUS_KEYS.gz POSTDIR OUT.gz
 - tallies singular / order / extraAP / not45 / ok over all canonical patterns, and over the census O' subset
   (flags k30 k31 c4 from POSTDIR/filtered.txt.gz, read as data), to compare with summary.json
 - realizable: h (largest Sidon subset, own DFS), alpha of the 3-AP hypergraph (subset scan), (4,5) holds,
   AP pattern == stored pattern (by construction of 'ok'), affine normal form
 - compares with POSTDIR/real_*.json.gz: same realizable patterns, same normal forms, census set == own set (normal form)
"""
import sys, gzip, json, glob, os, collections, time
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "realize14.py")).read().split("if __name__")[0]
exec(src)  # solve, three_aps, is45, sidon_max, alpha_ap, normal_form, realize

KEYS, POST, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
N = 14
t0 = time.time()
pats = []
for l in gzip.open(KEYS, "rt"):
    k = l.split()[0]
    pats.append(tuple(tuple(map(int, e.split(","))) for e in k.split(";")))
print("patterns", len(pats), flush=True)
# O' flags from the census filter output (data only)
oflag = {}
for l in gzip.open(os.path.join(POST, "filtered.txt.gz"), "rt"):
    f = l.split()
    es = tuple(sorted(tuple(map(int, t.split(","))) for t in f[4:]))
    oflag[es] = tuple(map(int, f[:4]))
print("filtered lines", len(oflag), flush=True)
st_all = collections.Counter(); st_o = collections.Counter(); st_o_call = collections.Counter()
mine = {}
dets = collections.Counter()
for q, es in enumerate(pats):
    st, vals, det = realize(N, list(es))
    st_all[st] += 1
    dets["det_nonzero" if det != 0 else "det_zero"] += 1
    fl = oflag.get(es)
    if fl is None:
        st_all["NOT_IN_FILTER_OUTPUT"] += 1
    elif fl[0] and fl[1] and fl[2]:
        st_o[st] += 1
        if not fl[3]:
            st_o_call[st] += 1
    if st == "ok":
        h = sidon_max(vals); al = alpha_ap(N, three_aps(vals))
        mine[es] = (normal_form(vals), h, al, is45(vals), fl)
    if q % 20000 == 0:
        print(q, "%.0fs" % (time.time() - t0), dict(st_all), flush=True)
print("ALL canonical patterns:", dict(st_all))
print("determinants:", dict(dets))
print("O' subset (k30&k31&c4):", dict(st_o), "sum", sum(st_o.values()))
print("  of which excluded by a long core (call=0):", dict(st_o_call))
hs = collections.Counter((v[1], v[2], v[3]) for v in mine.values())
print("realizable:", len(mine), "(h, alpha, is45) histogram:", dict(hs))
print("realizable outside O' (would contradict the pre-filters):", sum(1 for v in mine.values() if not (v[4] and v[4][1] and v[4][2])))
print("realizable failing some long core (call=0):", sum(1 for v in mine.values() if v[4] and not v[4][3]))
nfs = [v[0] for v in mine.values()]
print("distinct normal forms:", len(set(nfs)))
# census realizable list
cen = {}
for f in sorted(glob.glob(os.path.join(POST, "real_*.json.gz"))):
    d = json.load(gzip.open(f, "rt"))
    for r in d["real"]:
        es = tuple(sorted(tuple(e) for e in r["edges"]))
        cen[es] = normal_form(r["set"])
print("census realizable entries:", len(cen))
A, B = set(mine), set(cen)
print("patterns: mine-census", len(A - B), "census-mine", len(B - A))
bad = sum(1 for es in A & B if mine[es][0] != cen[es])
print("normal-form disagreements on common patterns:", bad)
print("normal forms: mine-census", len(set(nfs) - set(cen.values())), "census-mine", len(set(cen.values()) - set(nfs)))
AB = (0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056)
print("A_base normal form among mine:", normal_form(AB) in set(nfs))
with gzip.open(OUT, "wt") as g:
    for es, v in sorted(mine.items()):
        g.write("%s\t%s\t%d\t%d\n" % (";".join("%d,%d,%d" % e for e in es), ",".join(map(str, v[0])), v[1], v[2]))
print("time %.0fs" % (time.time() - t0))
