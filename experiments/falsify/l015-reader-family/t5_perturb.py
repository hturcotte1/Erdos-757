"""Power tests: perturb O or phi; compare the proof's hypotheses (own re-derivation) with actual behaviour."""
import json, time, sys, random
from fractions import Fraction
from lib import *

def analyze(O, c, a, K, literal45=False):
    O = sorted(O); M = max(O)
    copies, ic, den = build(O, c, a, K)
    pts = points(ic); n = len(pts); idx = {p: i for i, p in enumerate(pts)}
    sets = [set(cp) for cp in ic]
    r = {"n": n, "n_matches_11+9K": n == 11 + 9*K}
    # copy-intersection claim: consecutive share exactly 2 points (phi^j(c0), phi^j(cM)), non-consecutive disjoint
    ok = True
    for j in range(K+1):
        for jj in range(j+1, K+1):
            I = sets[j] & sets[jj]
            if jj == j+1:
                if len(I) != 2: ok = False
            elif I: ok = False
    r["copy_intersections_claim"] = ok
    groups, _ = relation_groups(pts)
    rps = relation_pointsets(groups)
    cidx = [set(idx[p] for p in s) for s in sets]
    r["n_relations"] = len(rps)
    r["n_4pt_relations"] = sum(1 for x in rps if len(x) == 4)
    r["n_cross_copy_relations"] = sum(1 for x in rps if not any(x <= cs for cs in cidx))
    r["all_relations_in_one_copy"] = r["n_cross_copy_relations"] == 0
    r["_ps"] = [sorted(x) for x in rps]; r["_pts"] = pts
    if literal45:
        r["min_distinct_diffs"] = min_distinct_diffs(pts)
    return r

def proof_hypotheses(O, c=101, a=18, dmax=8):
    """re-derive (own code) the finite facts the proof's Steps 1-2 use, for a general O (min 0, max M)"""
    O = sorted(O); M = max(O); Oi = [x for x in O if 0 < x < M]; h = {}
    h["M_prime"] = M > 1 and all(M % q for q in range(2, int(M**0.5)+1))
    h["M_not_div_a"] = (a % M != 0)
    # Lemma 1.2 analogue
    hits = set()
    for x in O:
        y = Fraction(x)
        for d in range(1, dmax+1):
            y = Fraction(c) + Fraction(a, M) * y
            if y.denominator == 1 and int(y) in O: hits.add((d, x, int(y)))
    h["lemma12_hits"] = sorted(hits)
    h["lemma12"] = (hits == {(1, 0, c), (1, M, c + a)})
    h["shared_in_O"] = (c in O and c + a in O)
    # F4 analogue: relations inside O all 3-point, linear, no edge with both endpoints
    ptsO = O
    groups, _ = relation_groups(ptsO)
    rps = relation_pointsets(groups)
    h["O_has_4pt_relation"] = any(len(x) == 4 for x in rps)
    E = [tuple(sorted(ptsO[i] for i in x)) for x in rps if len(x) == 3]
    h["O_linear"] = all(len(set(e) & set(f)) <= 1 for e, f in combinations(E, 2))
    h["O_no_edge_with_both_ends"] = not any(0 in e and M in e for e in E)
    h["O_midpoints_one_each"] = sorted(sorted(e)[1] for e in E) == sorted(Oi)
    # F5 analogue
    f5 = {}
    f5["i"] = all(x % M != 0 for x in Oi)
    f5["ii"] = all((x + y) % M != 0 for x in Oi for y in Oi)
    f5["iii"] = all(not ((x - y) % M == 0 and x != y) for x in Oi for y in Oi)
    sol = [(x, y, z) for x in Oi for y in Oi for z in Oi if (x + y - z) % M == 0]
    f5["iv_solutions"] = sol
    f5["iv"] = all(x == y and (x + y - z) in (0, M) for (x, y, z) in sol)
    h["F5"] = f5
    h["PRED"] = bool(h["M_prime"] and h["M_not_div_a"] and h["lemma12"] and h["shared_in_O"] and not h["O_has_4pt_relation"]
                     and h["O_linear"] and h["O_no_edge_with_both_ends"] and f5["i"] and f5["ii"] and f5["iii"] and f5["iv"])
    return h

if __name__ == "__main__":
    Kcross = 5
    res = {"A_single_element_changes": [], "B_phi_changes": {}, "D_transfer": {}}
    # sanity: the original
    h0 = proof_hypotheses(O0); print("original hypotheses:", {k: v for k, v in h0.items() if k != 'F5'}, h0["F5"]["iv_solutions"], flush=True)
    assert h0["PRED"]
    a0 = analyze(O0, 101, 18, Kcross); assert a0["all_relations_in_one_copy"] and a0["n_4pt_relations"] == 0

    # ---- A. change one element of O (any of the 11 positions, including endpoints), phi=101+18x/M ----
    t0 = time.time(); stats = {"variants": 0, "PRED_true": 0, "PRED_true_and_cross": 0, "PRED_true_and_not45_literal": 0,
                               "cross_present": 0, "claimcopy_fail": 0, "n_fail": 0, "PRED_false_but_ok": 0}
    cross_by_failed_item = {}
    for pos in range(11):
        for v in range(0, 300):
            if v in O0: continue
            O = sorted(O0[:pos] + [v] + O0[pos+1:])
            if min(O) != 0: continue            # normalise: keep min = 0
            M = max(O)
            if M < 120: continue
            if len(set(O)) != 11: continue
            h = proof_hypotheses(O)
            a = analyze(O, 101, 18, Kcross)
            stats["variants"] += 1
            cross = a["n_cross_copy_relations"] > 0 or a["n_4pt_relations"] > 0 or not a["all_relations_in_one_copy"]
            stats["cross_present"] += cross
            stats["claimcopy_fail"] += (not a["copy_intersections_claim"])
            stats["n_fail"] += (not a["n_matches_11+9K"])
            if h["PRED"]:
                stats["PRED_true"] += 1
                if cross: stats["PRED_true_and_cross"] += 1; print("PROOF-LOGIC VIOLATION", O, flush=True)
                if not (a["copy_intersections_claim"] and a["n_matches_11+9K"]): print("PRED but sharing claim fails", O)
            else:
                failed = tuple(k for k in ["M_prime", "shared_in_O", "lemma12", "O_has_4pt_relation", "O_linear", "O_no_edge_with_both_ends"]
                               if (h[k] if k == "O_has_4pt_relation" else not h[k])) + tuple("F5" + k for k in ["i", "ii", "iii", "iv"] if not h["F5"][k])
                d = cross_by_failed_item.setdefault(failed, [0, 0]); d[0] += 1; d[1] += int(cross)
                if not cross and a["copy_intersections_claim"]: stats["PRED_false_but_ok"] += 1
    stats["sec"] = round(time.time() - t0, 1)
    res["A_single_element_changes"] = {"stats": stats, "cross_by_failed_hypothesis_set": {str(k): v for k, v in cross_by_failed_item.items()}}
    print("A", stats, flush=True)
    for k, v in sorted(cross_by_failed_item.items(), key=lambda kv: -kv[1][0])[:25]: print("   failed", k, "variants, with cross/4pt relation:", v, flush=True)

    # ---- A2. literal (4,5) check at K=2 on every single-element variant with PRED true ----
    lit = {"PRED_true_checked": 0, "PRED_true_45_ok": 0, "PRED_false_checked": 0, "PRED_false_45_fail": 0}
    for pos in range(11):
        for v in range(0, 300):
            if v in O0: continue
            O = sorted(O0[:pos] + [v] + O0[pos+1:])
            if min(O) != 0 or max(O) < 120: continue
            h = proof_hypotheses(O)
            a = analyze(O, 101, 18, 2, literal45=True)
            if h["PRED"]:
                lit["PRED_true_checked"] += 1; lit["PRED_true_45_ok"] += (a["min_distinct_diffs"] >= 5)
            else:
                lit["PRED_false_checked"] += 1; lit["PRED_false_45_fail"] += (a["min_distinct_diffs"] < 5)
    print("A2", lit, flush=True); res["A2_literal_45_K2"] = lit

    # ---- B. change phi (c, a) keeping O: which lemma claims survive ----
    B = {"variants": 0, "all_claims_hold": [], "sharing_claim_fails": 0, "cross_present": 0}
    for c in range(60, 171):
        for aa in range(1, 61):
            a = analyze(O0, c, aa, 3)
            B["variants"] += 1
            okall = a["copy_intersections_claim"] and a["n_matches_11+9K"] and a["all_relations_in_one_copy"] and a["n_4pt_relations"] == 0
            if okall: B["all_claims_hold"].append((c, aa))
            B["sharing_claim_fails"] += (not a["copy_intersections_claim"])
            B["cross_present"] += (not a["all_relations_in_one_copy"])
    print("B", {k: (v if k != 'all_claims_hold' else v) for k, v in B.items()}, flush=True)
    res["B_phi_changes"] = B

    # ---- D. transfer-matrix logic on perturbed O' (needs 101,119 in O', phi fixed) ----
    D = {"variants": 0, "struct_ok": 0, "struct_ok_pred_eq_dp_all_K1to4": 0, "struct_ok_identity_plus5": 0, "struct_ok_identity_other": {},
         "struct_bad_pred_neq_dp": 0, "struct_bad": 0, "mismatch_examples": []}
    for pos in range(11):
        for v in range(0, 300):
            if v in O0: continue
            O = sorted(O0[:pos] + [v] + O0[pos+1:])
            if min(O) != 0 or max(O) != 269 and pos != 10: pass
            if min(O) != 0 or max(O) < 120: continue
            M = max(O)
            tr = transfer(O)
            if tr is None: continue
            D["variants"] += 1
            best, Mx, R0 = tr
            ident = maxplus(R0, Mx)
            diffs = {ident[t] - R0[t] for t in range(4)}
            a4 = analyze(O, 101, 18, 4)
            struct = a4["copy_intersections_claim"] and a4["n_matches_11+9K"] and a4["all_relations_in_one_copy"] and a4["n_4pt_relations"] == 0
            allm = True
            for K in range(1, 5):
                aK = analyze(O, 101, 18, K)
                dp = alpha_frontier_dp(len(aK["_pts"]), aK["_ps"])
                pr = predict_h(O, K)
                if dp != pr: allm = False
            if struct:
                D["struct_ok"] += 1; D["struct_ok_pred_eq_dp_all_K1to4"] += allm
                if diffs == {5}: D["struct_ok_identity_plus5"] += 1
                else: D["struct_ok_identity_other"][str(sorted(diffs))] = D["struct_ok_identity_other"].get(str(sorted(diffs)), 0) + 1
                if not allm and len(D["mismatch_examples"]) < 5: D["mismatch_examples"].append(O)
            else:
                D["struct_bad"] += 1; D["struct_bad_pred_neq_dp"] += (not allm)
    print("D", D, flush=True); res["D_transfer"] = D
    json.dump(res, open("t5_perturb.json", "w"), indent=1, default=str)
