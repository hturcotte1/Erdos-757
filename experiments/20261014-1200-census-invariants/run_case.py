"""Usage: python3 run_case.py <engine: glucose4|cadical153|cpsat> <n> <T> <m> <tier> <time_limit_s> [gl]
Prints one JSON result line; SAT results are re-checked and realized exactly."""
import json, os, sys, time
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir('/home/user/Erdos-757')
from invariants import TIERS
engine, n, T, m, tier, tl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], float(sys.argv[6])
gl = (sys.argv[7] if len(sys.argv) > 7 else 'LR') if m == n - 2 else False
extra = TIERS[tier] or None
t0 = time.time()
if engine == 'cpsat':
    from e757 import cpsat_extra
    status, edges, stats = cpsat_extra.feasible(n, T, m, extra=extra, time_limit=tl, workers=int(os.environ.get('WORKERS', 2)),
                                                log=lambda s: print(s, file=sys.stderr, flush=True))
else:
    from e757 import sat_indep
    status, res = sat_indep.decide(n, T, m, extra=extra, time_limit=tl, solver=engine, gl_constraints=gl)
    edges, stats = (res, {}) if status == 'SAT' else (None, res)
out = dict(engine=engine, n=n, T=T, m=m, tier=tier, extra={k: v for k, v in (extra or {}).items()}, gl=gl,
           status=status, seconds=round(time.time() - t0, 1), stats={k: v for k, v in stats.items() if isinstance(v, (int, float, str))})
if status == 'SAT':
    edges = [tuple(e) for e in edges]
    out['edges'] = edges
    from e757.saturated import alpha_of_edges
    out['alpha'] = alpha_of_edges(n, edges)
    from e757.realizability import realize_exact
    try:
        r = realize_exact(n, edges)
        out['realize'] = str(r)[:600]
        if r[0]:
            out['realized_set'] = list(r[1])
    except Exception as ex:
        out['realize_error'] = repr(ex)
print(json.dumps(out, default=str))
