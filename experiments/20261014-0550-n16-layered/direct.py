"""Direct (non-layered) native enumeration on N vertices: python3 direct.py N T M TIME_S  -> results/direct_n{N}_m{M}_*"""
import sys as _s, os as _o; _s.path.insert(0, _o.path.abspath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "..")))
import os, sys
from e757.cpsat_model import enumerate_native, load_cores
N, T, M, TL = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.abspath(os.path.join(here, "..", ".."))
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
base = os.path.join(here, "results", "direct_n%d_m%d" % (N, M))
cnt, st = enumerate_native(N, T, M, base + "_solutions.jsonl", time_limit=TL, progress_path=base + "_progress.json",
                           cores=cores, core_max_edges=4)
print("DONE", N, T, M, st, cnt)
