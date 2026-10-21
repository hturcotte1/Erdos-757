#!/usr/bin/env python3
"""Validate the referee tools on small sets against literal brute force (Sidon definition), n <= 22.

Sets: A_base (h=8), the sets of data/small_records.json (n = 8, 10, 11, 12, 14), the third 12-point record,
{1,...,9} (NOT weak Sidon; conflict sets of size 4 must be handled; h = 4), the Fibonacci prefix {2,3,5,...}
with 16 points, S_0 = O (h=7), S_1 (n=20, h=12), and the Lemma-E extension E1 of S_1 (n=22).
Also controls for the (4,5) checker: {1,2,3,5} (4 distinct differences, must FAIL), {0,1,3,7} (6, PASS).
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reflib as R  # noqa: E402

REPO = Path(__file__).resolve().parents[3]


def sets_to_test():
    out = []
    out.append(("A_base", [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056], 8))
    out.append(("12pt-third", [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575], 7))
    d = json.loads((REPO / "data/small_records.json").read_text())
    for key, rec in sorted(d["sets"].items()):
        out.append(("small_records[%s]" % key, rec["set"], rec.get("h")))
    out.append(("1..9 (not weak Sidon)", list(range(1, 10)), 4))
    fib = [2, 3]
    while len(fib) < 16:
        fib.append(fib[-1] + fib[-2])
    out.append(("Fibonacci16", fib, None))
    S0 = R.reader_family_int(0)
    S1 = R.reader_family_int(1)
    out.append(("S_0 = O", S0, 7))
    out.append(("S_1 (n=20)", S1, 12))
    span = max(S1) - min(S1)
    t = 3 * span + 1000003
    E1 = sorted([min(S1) - t, min(S1) + t] + S1)
    E1 = [v - min(E1) for v in E1]
    out.append(("E1(S_1) (n=22)", E1, None))
    return out


def main():
    # (4,5) checker controls
    ok1, _, mn1, _ = R.check_45_literal([1, 2, 3, 5])
    ok2, _, mn2, _ = R.check_45_literal([0, 1, 3, 7])
    print("control (4,5): {1,2,3,5} ->", ok1, mn1, "(expect False 4);  {0,1,3,7} ->", ok2, mn2, "(expect True 6)")
    assert ok1 is False and mn1 == 4 and ok2 is True and mn2 == 6
    all_ok = True
    for name, A, expected in sets_to_test():
        A = R.parse_set(A)
        A = R.as_ints(A)
        n = len(A)
        ok45, n4, mn, worst = R.check_45_literal(A)
        confl, ncoinc, hist = R.conflict_sets(A)
        t0 = time.time()
        hb, checked, S = R.brute_h(A)
        tb = time.time() - t0
        assert R.is_sidon_def(S) and len(S) == hb
        # SAT: k = hb must be SAT with a verified model; k = hb + 1 must be UNSAT (two solvers / encodings)
        s1, ch1, _ = R.sat_atleast(n, confl, hb, "cadical153", "seqcounter")
        assert s1 and R.is_sidon_def([A[i] for i in ch1]) and len(ch1) >= hb
        u1, _, _ = R.sat_atleast(n, confl, hb + 1, "cadical153", "seqcounter")
        u2, _, _ = R.sat_atleast(n, confl, hb + 1, "glucose4", "totalizer")
        # CP-SAT
        st, obj, bnd, chc, tc = R.cpsat_max(n, confl, tlim=120, workers=1)
        assert st == "OPTIMAL" and obj == hb and bnd == hb and R.is_sidon_def([A[i] for i in chc]) and len(chc) == hb
        # own branching solver
        ha, stats, ta = R.alpha_setsystem(n, confl)
        agree = (ha == hb) and (not u1) and (not u2) and (obj == hb)
        exp_ok = (expected is None) or (expected == hb)
        all_ok &= agree and exp_ok
        print("%-24s n=%2d (4,5)=%s minDiff=%d conflicts=%s brute=%d (%d subsets, %.1fs) SAT(k)=%s SAT(k+1)=%s/%s "
              "CPSAT=%s %s/%s own=%d (%d calls, %.2fs) expected=%s %s"
              % (name, n, ok45, mn, hist, hb, checked, tb, s1, u1, u2, st, obj, bnd, ha, stats["calls"], ta,
                 expected, "OK" if (agree and exp_ok) else "MISMATCH"))
        sys.stdout.flush()
    print("ALL TOOL VALIDATIONS OK" if all_ok else "TOOL VALIDATION FAILURE")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
