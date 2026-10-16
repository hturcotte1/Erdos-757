"""Assemble README.md from generated pieces.  Usage: python3 build_readme.py"""
import json
from collections import defaultdict, OrderedDict
import re
src = open("gen_readme.py").read()
names = eval(src[src.index("NAMES = ") + 8: src.index("\n}\n", src.index("NAMES = ")) + 2])
stats = json.load(open("catalogue_tables.md.stats.json"))
cat = json.load(open("catalogue.json"))
hg = [tuple(map(tuple, h)) for h in cat["hypergraphs"]]
agg = defaultdict(lambda: defaultdict(int))
for r in stats:
    a = agg[r["hid"]]
    a["lab"] += 1; a["inj"] += r["injective"]; a["real_lab"] += r["R"] > 0
    a["forb_inj"] += (r["injective"] and r["R"] == 0)
    a["orders"] += r["orders"]; a["R"] += r["R"]; a["O"] += r["O"]; a["E"] += r["E"]; a["D"] += r["D"]
rows = ["| config | name | vertices | edges | labelings | midpoint-injective | labelings realizable in >=1 order | injective but forbidden in every order | ordered patterns | R | O | E | D |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for hid, h in enumerate(hg):
    a = agg[hid]
    nv = max(v for e in h for v in e) + 1
    rows.append(f"| H{hid} | {names[h]} | {nv} | {len(h)} | {a['lab']} | {a['inj']} | {a['real_lab']} | {a['forb_inj']} | {a['orders']} | {a['R']} | {a['O']} | {a['E']} | {a['D']} |")
summary = "\n".join(rows)
n8 = json.load(open("../../data/forbidden_ordered_n8.json"))
c8 = n8["counts_by_n"]["8"]
tally = open("tally_cores.out").read().strip()
fm = open("failure_modes.out").read().strip().splitlines()[-1]
tables = open("catalogue_tables.md").read()
tpl = open("README_template.md").read()
out = tpl.replace("@@SUMMARY@@", summary).replace("@@TALLY@@", tally).replace("@@FM@@", fm).replace("@@TABLES@@", tables)
for k in ("total", "realizable", "order-infeasible", "forced extra AP", "forced repeated difference"):
    out = out.replace("@@N8_" + k.replace(" ", "_") + "@@", str(c8[k]))
out = out.replace("@@N8_CORES@@", str(n8["n_cores"])).replace("@@N8_KINDS@@", json.dumps(n8["cores_by_n_kind"]))
open("README.md", "w").write(out)
