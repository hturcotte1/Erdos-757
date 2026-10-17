import gzip, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model14 import *
rows = [json.loads(l) for l in gzip.open(os.path.join(REPO, "data/census_n14_m12_classes.jsonl.gz"), "rt")]
bad = []
for i, r in enumerate(rows):
    ok, det = check14(14, [tuple(e) for e in r["edges"]], 8)
    if not ok: bad.append((i, det))
print(len(rows), "classes;", len(bad), "violations")
json.dump({"n_classes": len(rows), "violations": len(bad), "first": bad[:3]}, open(os.path.join(HERE, "soundness_full_census.json"), "w"))
