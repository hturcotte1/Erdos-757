"""One timed n=16 case: python3 single_case.py m vertex1 time_limit [solver] -> results/single_*.json"""
import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
import json, sys, time
sys.path.insert(0, "/home/user/Erdos-757")
from e757.sat_indep import enumerate_all
m, k, TL = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
solver = sys.argv[4] if len(sys.argv) > 4 else "glucose4"
t = time.time()
sols, st = enumerate_all(16, 9, m, vertex1=k, time_limit=TL, solver=solver, return_stats=True, max_solutions=1000)
st = {x: (v if not isinstance(v, dict) else v) for x, v in st.items()}
st["wall"] = round(time.time() - t, 1)
st["solutions"] = [list(map(list, s)) for s in sols]
print(json.dumps({x: st[x] for x in st if x != "accum_stats"}), flush=True)
json.dump(st, open(f"results/single_m{m}_k{k}_{solver}.json", "w"))
