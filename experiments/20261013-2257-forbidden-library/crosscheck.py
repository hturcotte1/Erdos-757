"""Cross-check realize_exact against the independent float-LP + sympy path of ordered_search
(_order_lp, _exact_realization) on every pattern with n <= 7, and certificates via verify_certificate."""
import random, sys, itertools
sys.argv = ["x", "3"]
from e757.realizability import order_feasible, realize_exact, verify_certificate
from e757.ordered_search import _order_lp, _exact_realization
import importlib.util
spec = importlib.util.spec_from_file_location("enum", "enumerate.py")
src = open("enumerate.py").read().split("def main():")[0]
ns = {}
exec(src, ns)
bad = 0; tot = 0
rng = random.Random(1)
for n in range(3, 8):
    for edges in ns["patterns"](n):
        tot += 1
        ok, cert = order_feasible(n, list(edges))
        assert verify_certificate(n, edges, ok, cert)
        lp_ok, _ = _order_lp(n, list(edges))
        if lp_ok != ok:
            bad += 1; print("ORDER MISMATCH", n, edges, ok, lp_ok)
        r = realize_exact(n, list(edges))
        other = None
        if lp_ok:
            for _ in range(6):
                try:
                    other = _exact_realization(n, list(edges), rng)
                    break
                except ValueError:
                    pass
        if (r[0] is True) != (other is not None):
            bad += 1; print("REALIZE MISMATCH", n, edges, r[:2], other is not None)
print("patterns", tot, "mismatches", bad)
