#!/usr/bin/env python3
"""Round-2 referee verification of results/claims/C004-lemmaE-SK5-E1.json (no e757, no judge imports).

Checks: file sanity (id, type, integers, distinct), literal (4,5) test over all 4-subsets, weak Sidon,
conflict-set structure from the Sidon definition, witness, exact h by SAT (k=33 SAT with verified model,
k=34 UNSAT with three solver/encoding combinations), own branching solver, CP-SAT (gap 0 if OPTIMAL),
exact Fraction comparison with 4/7, and the structural claim: the set is I_5 + {min - t, min + t},
I_5 = 269^5 * S_5 rebuilt from O and phi, t = 3*span + 1000003, translated to min 0.
"""
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reflib as R  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
CLAIM = REPO / "results/claims/C004-lemmaE-SK5-E1.json"
OUT = Path(__file__).resolve().parent / "verify_c004_results.json"


def say(*a):
    print(*a)
    sys.stdout.flush()


def main():
    res = {}
    claim = json.loads(CLAIM.read_text())
    say("file:", CLAIM, " id:", claim.get("id"), " type:", claim.get("type"))
    assert claim["id"] == CLAIM.stem and claim["type"] == "construction"
    raw = claim["set"]
    assert all(isinstance(x, int) and not isinstance(x, bool) for x in raw), "non-integer JSON entries"
    Af = R.parse_set(raw)            # Fractions, distinct, sorted
    A = R.as_ints(Af)                # all integers
    n = len(A)
    assert A == sorted(set(raw)) and len(set(raw)) == len(raw) == n
    res.update(n=n, min=A[0], max=A[-1], all_integers=True, distinct=True)
    say("n =", n, " min =", A[0], " max =", A[-1], " all distinct integers")

    # ---- (4,5) literal
    t0 = time.time()
    ok45, n4, mn, worst = R.check_45_literal(A)
    say("(4,5) literal check: ok=%s  subsets=%d  min distinct diffs=%d  (%.1fs)" % (ok45, n4, mn, time.time() - t0))
    res.update(is_45=ok45, n_4subsets=n4, min_distinct_diffs=mn)
    assert ok45

    # ---- weak Sidon + conflict structure (from the Sidon definition)
    ws = R.is_weak_sidon_def(A)
    confl, ncoinc, hist = R.conflict_sets(A)
    say("weak Sidon:", ws, " sum coincidences:", ncoinc, " conflict sets by size:", hist)
    res.update(weak_sidon=ws, n_sum_coincidences=ncoinc, conflict_hist=hist)
    aps = sorted(tuple(A[i] for i in sorted(F)) for F in confl if len(F) == 3)
    for a, b, c in aps:
        assert a + c == 2 * b
    res["n_conflict_sets"] = len(confl)

    # ---- witness
    W = R.as_ints(R.parse_set(claim["witness_sidon_subset"]))
    w_ok = set(W) <= set(A) and R.is_sidon_def(W)
    say("witness: size=%d subset=%s Sidon(def)=%s" % (len(W), set(W) <= set(A), R.is_sidon_def(W)))
    res.update(witness_size=len(W), witness_ok=w_ok)
    assert w_ok and len(W) == claim["claimed_h"] == 33

    # ---- exact h: SAT
    k = 33
    s, ch, ts = R.sat_atleast(n, confl, k, "cadical153", "seqcounter")
    say("SAT k=%d cadical153/seqcounter: %s (%.1fs)" % (k, s, ts))
    assert s
    Sm = [A[i] for i in ch]
    assert len(Sm) >= k and R.is_sidon_def(Sm), "SAT model is not Sidon by the definition!"
    say("  model of size %d re-verified Sidon from the definition" % len(Sm))
    res["sat_33"] = dict(sat=True, model_size=len(Sm), model_sidon=True, seconds=round(ts, 2))
    res["sat_34"] = {}
    for solver, enc in (("cadical153", "seqcounter"), ("glucose4", "totalizer"), ("kissat404", "kmtotalizer"),
                        ("maplechrono", "cardnetwrk")):
        try:
            u, _, tu = R.sat_atleast(n, confl, 34, solver, enc)
            say("SAT k=34 %s/%s: %s (%.1fs)%s" % (solver, enc, u, tu, "" if not u else "   <-- LARGER SIDON SET EXISTS"))
            res["sat_34"]["%s/%s" % (solver, enc)] = dict(sat=u, seconds=round(tu, 2))
        except Exception as e:  # solver not available in this pysat build
            say("SAT k=34 %s/%s: not run (%s)" % (solver, enc, e))
            res["sat_34"]["%s/%s" % (solver, enc)] = dict(error=str(e))

    # ---- exact h: own branching solver
    try:
        ha, stats, ta = R.alpha_setsystem(n, confl, time_cap=900)
        say("own branching solver: h = %d  (%d calls, %d memo hits, %.1fs)" % (ha, stats["calls"], stats["memo_hits"], ta))
        res["own_solver"] = dict(h=ha, calls=stats["calls"], seconds=round(ta, 1))
    except R.Budget:
        say("own branching solver: time cap reached")
        res["own_solver"] = dict(h=None, note="time cap")

    # ---- exact h: CP-SAT (integer program)
    st, obj, bnd, chc, tc = R.cpsat_max(n, confl, tlim=420, workers=1)
    say("CP-SAT (IP, 1 worker, 420s cap): status=%s obj=%s bound=%s (%.1fs)" % (st, obj, bnd, tc))
    if chc is not None:
        assert R.is_sidon_def([A[i] for i in chc])
    res["cpsat"] = dict(status=st, obj=obj, bound=bnd, seconds=round(tc, 1))

    # ---- ratio
    r = Fraction(33, n)
    say("ratio 33/%d = %s < 4/7 ? %s   (7*33=%d, 4*%d=%d)" % (n, r, r < Fraction(4, 7), 7 * 33, n, 4 * n))
    res["ratio_lt_4_7"] = bool(r < Fraction(4, 7))

    # ---- structure: Lemma-E extension of I_5 at its minimum
    I5 = R.reader_family_int(5)
    span = max(I5) - min(I5)
    t = 3 * span + 1000003
    E1 = sorted([min(I5) - t, min(I5) + t] + I5)
    E1 = [v - min(E1) for v in E1]
    same = (E1 == A)
    say("structure: |I_5| = %d, span = %d (= 269^6: %s), t = %d, I_5 + {min-t, min+t} translated == claim set: %s"
        % (len(I5), span, span == 269 ** 6, t, same))
    res.update(structure_matches=same, t=t, span=span)
    if same:
        # the extreme point a = min I_5 sits at t in the claim set; the two new points are 0 and 2t
        a_idx = A.index(t)
        new_idx = [A.index(0), A.index(2 * t)]
        say("  a = min I_5 -> index %d (value %d); new points at indices %s" % (a_idx, t, new_idx))
        # the single new AP must be {0, t, 2t}
        new_aps = [e for e in aps if 0 in e or 2 * t in e]
        say("  conflict sets involving a new point:", new_aps, " (expected exactly [(0, t, 2t)])")
        res["new_aps"] = new_aps
        # h of the base I_5 and of I_5 minus its min (universality), by SAT
        confl5, _, hist5 = R.conflict_sets(I5)
        s32, _, _ = R.sat_atleast(len(I5), confl5, 32, "cadical153", "seqcounter")
        u33, _, t33 = R.sat_atleast(len(I5), confl5, 33, "cadical153", "seqcounter")
        say("  base I_5: n=%d conflicts=%s  h>=32: %s  h>=33: %s (%.1fs)  => h(I_5) = 32: %s" % (len(I5), hist5, s32, u33, t33, s32 and not u33))
        I5m = I5[1:]
        conflm, _, _ = R.conflict_sets(I5m)
        s31, _, _ = R.sat_atleast(len(I5m), conflm, 31, "cadical153", "seqcounter")
        u32, _, _ = R.sat_atleast(len(I5m), conflm, 32, "cadical153", "seqcounter")
        say("  I_5 minus min: h>=31: %s  h>=32: %s  => min is universal (alpha(H-a) = h-1 = 31): %s" % (s31, u32, s31 and not u32))
        res.update(h_I5_is_32=bool(s32 and not u33), min_universal=bool(s31 and not u32))

    OUT.write_text(json.dumps(res, indent=1, default=str))
    say("results written to", OUT)
    sat34_all_unsat = all(v.get("sat") is False for v in res["sat_34"].values() if "sat" in v)
    verdict_ok = ok45 and w_ok and sat34_all_unsat and res["ratio_lt_4_7"]
    say("SUMMARY: (4,5)=%s  h=33 (SAT at 33, all k=34 runs UNSAT=%s, own=%s, cpsat=%s)  ratio<4/7=%s  => %s"
        % (ok45, sat34_all_unsat, res.get("own_solver", {}).get("h"), res["cpsat"].get("obj"), res["ratio_lt_4_7"],
           "CLAIM VERIFIED" if verdict_ok else "PROBLEM"))
    return 0 if verdict_ok else 1


if __name__ == "__main__":
    sys.exit(main())
