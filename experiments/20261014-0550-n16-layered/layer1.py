"""Layer 1: enumerate ALL members H' of class O' on NP = N-1 vertices with exactly MP edges and alpha <= T.
O' = linear, midpoint-injective, F7-free, K30 monotone, K31 medial, forbidden cores with <= 4 edges
(data/forbidden_ordered_n7.json + _n8.json).  No symmetry breaking (reflection would turn 'delete max' into
'delete min').  Streams results/n{NP}_m{MP}_solutions.jsonl (one solution per line, flushed) and
results/n{NP}_m{MP}_progress.json.  Resumable at stream granularity: finished streams (status EXHAUSTED or
LIMIT in the progress JSON) are skipped; an unfinished stream is restarted from scratch.
Usage: python3 layer1.py NP T MP TIME_LIMIT_S [SOLUTION_LIMIT]"""
import sys as _s, os as _o; _s.path.insert(0, _o.path.abspath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "..")))
import json, os, sys
from e757.cpsat_model import enumerate_native, load_cores
NP, T, MP, TL = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
LIM = int(float(sys.argv[5])) if len(sys.argv) > 5 else 2_000_000
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.abspath(os.path.join(here, "..", ".."))
res = os.path.join(here, "results"); os.makedirs(res, exist_ok=True)
base = os.path.join(res, "n%d_m%d" % (NP, MP))
prog = base + "_progress.json"
if os.path.exists(prog) and json.load(open(prog))["status"] in ("EXHAUSTED", "LIMIT"):
    print("SKIP finished", prog); sys.exit(0)
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
cnt, st = enumerate_native(NP, T, MP, base + "_solutions.jsonl", limit=LIM, time_limit=TL, progress_path=prog,
                           cores=cores, core_max_edges=4)
print("DONE", NP, T, MP, st, cnt)
