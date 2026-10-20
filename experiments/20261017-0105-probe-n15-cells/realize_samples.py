import sys, glob, json, collections, random
from e757.realizability import realize_exact
m = int(sys.argv[1]); cap = int(sys.argv[2])
pats = []
for f in sorted(glob.glob("experiments/20261017-0105-probe-n15-cells/samples/n15_m%d_prefix_*.sol" % m)):
    for l in open(f):
        pats.append([tuple(map(int, t.split(","))) for t in l.split()[1:]])
random.Random(1).shuffle(pats)
c = collections.Counter(); ok = []
for e in pats[:cap]:
    r = realize_exact(15, e)
    c[r[1] if not r[0] else "REALIZABLE"] += 1
    if r[0]: ok.append((e, r[1]))
print(m, "total saved", len(pats), "tested", min(cap, len(pats)), dict(c))
json.dump({"m": m, "tested": min(cap, len(pats)), "counts": dict(c), "realized": [{"edges": e, "set": s} for e, s in ok[:20]]},
          open("experiments/20261017-0105-probe-n15-cells/realiz_m%d.json" % m, "w"))
