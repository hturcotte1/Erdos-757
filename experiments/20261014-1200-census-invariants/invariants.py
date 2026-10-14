"""Invariant tiers used for the constrained search (spec dicts understood by sat_indep / cpsat_extra)."""
TIERS = {
    # Tier 0: no extra invariants except the GL colour balance (a proved consequence, gl_constraints='LR' / sat only)
    "gl_only": {},
    # Tier 1: properties of ALL 54,243 realizable n=12 patterns and ALL 157 n=14 sets (and, for maxdeg, also vacuous at n=12)
    "t1": {"maxdeg": 4, "ends_sum_min": 3, "n_deg1_max": 1},
    # Tier 2 (sample based, heuristic): everything seen in the 157 n=14 sets; FALSE for many n=12 patterns
    "t2": {"maxdeg": 4, "n_deg1_max": 0, "deg_ends": (2, 4), "deg_near_ends": (2, 4)},
}
