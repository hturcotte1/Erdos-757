"""For midpoint-injective labelings: failure kinds of the failing orders, and for order-infeasible ones the size of a
minimal order-infeasible sub-pattern (2 = K30 monotone-midpoint violation).  Usage: python3 failure_modes.py catalogue.json"""
import json, sys
from collections import Counter
from e757.realizability import forbidden_core
cat = json.load(open(sys.argv[1]))
res = Counter()
for c in cat["classes"]:
    if not c["mids_injective"]:
        continue
    medial = False
    for o in c["orders"]:
        v = o["verdict"]
        if v == "realizable":
            continue
        if v == "order-infeasible":
            k = len(forbidden_core(c["n"], [tuple(e) for e in o["rank_form"]], ("order",)))
            v = f"O(core {k} edges)"
        res[(c["hid"], v)] += 1
for k, n in sorted(res.items()):
    print(k, n)
tot = Counter()
for (h, v), n in res.items():
    tot[v] += n
print("TOTAL", dict(tot))
