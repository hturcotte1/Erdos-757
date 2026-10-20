#!/usr/bin/env python3
"""Longer CP-SAT run (with the valid local cuts) for K = 8, to try to close the optimality proof that 900 s did not reach."""
import json, sys, time
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from fractions import Fraction as F
from check_family import cpsat_h, census, is_sidon_def
REPO = here.parents[1]
fam = {m["K"]: m for m in json.loads((REPO / "data" / "reader_5_9_family.json").read_text())["family"]}
K = int(sys.argv[1]); tl = float(sys.argv[2])
A = sorted(fam[K]["set"]); scale = fam[K]["scale"]
L = F(27169, 251)
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
copies = [{int((L + F(18, 269) ** j * (F(x) - L)) * scale) for x in O} for j in range(K + 1)]
c = census(A)
st, obj, bnd, wit, wt = cpsat_h(A, c["aps"], workers=2, tlim=tl, copies=copies)
res = dict(K=K, n=len(A), status=st, obj=obj, bound=bnd, wall=round(wt, 1), witness_is_sidon_by_definition=is_sidon_def(wit))
print(res, flush=True)
(here / f"cpsat_K{K}_long.json").write_text(json.dumps(res, indent=1))
