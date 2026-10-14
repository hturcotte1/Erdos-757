"""Time one UNSAT/SAT decision with/without Gyarfas-Lehel constraints.
Usage: python3 gl_timing.py n T m variant solver [time_limit] [vertex1]   (variant in none,L,R,LR)
Prints one JSON line."""
import json, os, sys, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/user/Erdos-757")
from e757.sat_indep import decide
n, T, m = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
var, solver = sys.argv[4], sys.argv[5]
TL = float(sys.argv[6]) if len(sys.argv) > 6 else None
v1 = int(sys.argv[7]) if len(sys.argv) > 7 else None
t = time.time()
st, r = decide(n, T, m, solver=solver, time_limit=TL, vertex1=v1, gl_constraints=("" if var == "none" else var))
print(json.dumps(dict(n=n, T=T, m=m, vertex1=v1, variant=var, solver=solver, status=st,
                      seconds=round(time.time() - t, 2), limit=TL)), flush=True)
