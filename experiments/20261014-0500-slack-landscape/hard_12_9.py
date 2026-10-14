import sys, json, time
sys.path.insert(0, "/home/user/Erdos-757")
from e757.cpsat_model import feasible_alpha_le, load_cores
cores = load_cores("/home/user/Erdos-757/data/forbidden_ordered_n7.json", "/home/user/Erdos-757/data/forbidden_ordered_n8.json")
st, edges, stats = feasible_alpha_le(12, 7, m_exact=9, time_limit=480, workers=4, monotone=True, medial=True, cores=cores, core_lit_budget=None)
print("op n=12 m=9 alpha<=7:", st, edges, stats.get("time"), flush=True)
