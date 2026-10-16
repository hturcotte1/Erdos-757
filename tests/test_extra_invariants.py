"""The optional `extra` invariant hook of sat_indep and the CP-SAT wrapper cpsat_extra."""
from e757 import sat_indep, cpsat_extra

T1 = {"maxdeg": 4, "ends_sum_min": 3, "n_deg1_max": 1}


def test_sat_hook_keeps_small_instances_sat():
    st, edges = sat_indep.decide(8, 5, 6, extra=T1, gl_constraints="LR")
    assert st == "SAT"
    deg = [sum(v in e for e in edges) for v in range(8)]
    assert max(deg) <= 4 and deg[0] + deg[7] >= 3 and sum(1 for d in deg if d <= 1) <= 1


def test_sat_hook_can_prune():
    # no vertex may have degree >= 2 -> a saturated 6-vertex pattern with alpha<=4 cannot exist
    st, _ = sat_indep.decide(8, 5, 6, extra={"maxdeg": 1}, gl_constraints="LR")
    assert st == "UNSAT"
    st, _ = sat_indep.decide(8, 5, 6, extra={"n_deg1_max": 0, "deg_ends": (2, 4)}, gl_constraints="LR")
    assert st in ("SAT", "UNSAT")


def test_cpsat_wrapper_agrees_with_sat():
    for extra in (T1, {"maxdeg": 1}):
        a, _ = sat_indep.decide(8, 5, 6, extra=extra, gl_constraints="LR")
        b, _, _ = cpsat_extra.feasible(8, 5, 6, extra=extra, time_limit=60, workers=1)
        assert a == b
