"""Referee L002: write temporary claim files (scratch only) for a random sample of census sets and the known sets."""
import gzip, json, os, random, sys
here = os.path.dirname(os.path.abspath(__file__))
outdir = os.path.join(here, "spot_claims")
os.makedirs(outdir, exist_ok=True)
census = json.load(gzip.open(os.path.join(here, "../../20261014-1005-census-dfs/results/realized_n12.json.gz"), "rt"))
random.seed(20261014)
sample = random.sample(census, int(sys.argv[1]) if len(sys.argv) > 1 else 40)
for i, r in enumerate(sample):
    cid = "L002ref%02d" % i
    with open(os.path.join(outdir, cid + ".json"), "w") as f:
        json.dump({"id": cid, "type": "construction", "set": r["set"], "claimed_h": 7, "notes": "referee L002 spot check"}, f)
known = [[0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575],
         [0, 178, 198, 218, 227, 235, 272, 276, 287, 317, 356, 436],
         [-336, -168, -44, -24, -4, 0, 39, 44, 49, 80, 102, 160]]
for i, A in enumerate(known):
    cid = "L002refK%d" % i
    with open(os.path.join(outdir, cid + ".json"), "w") as f:
        json.dump({"id": cid, "type": "construction", "set": A, "claimed_h": 7, "notes": "referee L002 known set"}, f)
print(len(os.listdir(outdir)))
