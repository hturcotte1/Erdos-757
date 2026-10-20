#!/usr/bin/env python3
"""Exact checks of the reader's family S_K (K = 0..8) read from data/reader_5_9_family.json.

Per K (all arithmetic in Python ints):
  - n, distinctness, 4-subset (4,5) test written here (independent of e757 and of judge/) and
    e757.core.is_45_set;  literal |B-B| >= 11 test for K <= 5;
  - AP / relation census: every solution of a+b = c+d (a<=b, c<=d, pairs distinct), number of 3-APs,
    parallelograms (4 distinct points), pairs of APs sharing two points, APs containing both anchors;
  - h exactly:  CP-SAT on the 3-AP hypergraph (status OPTIMAL, objective = bound) + a witness re-verified
    from the Sidon definition; python-sat/CaDiCaL on a DIRECT sum-collision encoding with a cardinality
    constraint (>= h SAT with model re-verified, >= h+1 UNSAT);  e757.core.alpha for K <= 2;
  - the max-plus transfer matrix over copies (own DP over the 2^11 subsets of O), to depth 200.
Usage: python3 check_family.py [--ks 0,1,2] [--no-sat] [--sat-timeout S] > ...
"""
import argparse
import itertools
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from e757 import core  # noqa: E402

O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
RESULTS = Path(__file__).resolve().parent / "check_results.json"


def four_subset_test(A):
    """Return (ok, number of 4-subsets, min #distinct positive differences)."""
    A = sorted(A)
    cnt = 0
    mn = 6
    for a, b, c, d in itertools.combinations(A, 4):
        cnt += 1
        k = len({b - a, c - a, d - a, c - b, d - b, d - c})
        if k < mn:
            mn = k
            if k < 5:
                return False, cnt, mn
    return True, cnt, mn


def literal_BB(A):
    for q in itertools.combinations(sorted(A), 4):
        if len({x - y for x in q for y in q}) < 11:
            return False
    return True


def census(A, anchors=None):
    """All relations a+b=c+d.  Returns dict with counts."""
    A = sorted(A)
    S = set(A)
    by_sum = defaultdict(list)
    for i, a in enumerate(A):
        for b in A[i:]:
            by_sum[a + b].append((a, b))
    aps = []
    parallelograms = 0
    other_multi = 0
    for s, prs in by_sum.items():
        if len(prs) < 2:
            continue
        for p, q in itertools.combinations(prs, 2):
            pts = set(p) | set(q)
            if len(pts) == 4:
                parallelograms += 1
            elif len(pts) == 3:
                # exactly 3 distinct points: a+c = 2b (one of the two pairs is (b,b))
                aps.append(tuple(sorted(pts)))
            else:
                other_multi += 1
    aps = sorted(set(aps))
    # relation list for SAT encoding: each relation as a set of distinct points
    rel_sets = set()
    for s, prs in by_sum.items():
        for p, q in itertools.combinations(prs, 2):
            rel_sets.add(frozenset(p) | frozenset(q))
    share2 = 0
    for e, f in itertools.combinations(aps, 2):
        if len(set(e) & set(f)) >= 2:
            share2 += 1
    return {"aps": aps, "n_aps": len(aps), "parallelograms": parallelograms, "other_multi": other_multi,
            "ap_pairs_sharing_two_points": share2, "rel_sets": rel_sets}


def is_sidon_def(S):
    """Sidon straight from the definition: all sums x+y, x<=y, distinct."""
    S = sorted(S)
    sums = [x + y for i, x in enumerate(S) for y in S[i:]]
    return len(sums) == len(set(sums))


def cpsat_h(A, aps, workers=2, tlim=600, copies=None):
    """CP-SAT on the 3-AP hypergraph.  With `copies` (list of 11-point sets phi^j(O)) it adds valid local cuts
    obtained by brute force on O alone: per copy  sum <= 7,  sum <= 6 + [anchor 0],  sum <= 6 + [anchor 269],
    and (interior 9 points) <= 6.  These are implied by the AP constraints, so optimality proofs stay rigorous."""
    from ortools.sat.python import cp_model
    idx = {v: i for i, v in enumerate(A)}
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(len(A))]
    for e in aps:
        m.Add(sum(x[idx[v]] for v in e) <= 2)
    if copies is not None:
        for cp in copies:
            pts = sorted(cp)
            a0, a1 = x[idx[pts[0]]], x[idx[pts[-1]]]
            tot = sum(x[idx[v]] for v in pts)
            m.Add(tot <= 7)
            m.Add(tot <= 6 + a0)
            m.Add(tot <= 6 + a1)
            m.Add(sum(x[idx[v]] for v in pts[1:-1]) <= 6)
    m.Maximize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_workers = workers
    r = s.Solve(m)
    st = s.StatusName(r)
    wit = [A[i] for i in range(len(A)) if s.Value(x[i])] if st in ("OPTIMAL", "FEASIBLE") else []
    return st, int(round(s.ObjectiveValue())), int(round(s.BestObjectiveBound())), wit, s.WallTime()


def sat_card(A, rel_sets, k, timeout):
    """Is there a Sidon subset of size >= k?  Direct sum-collision encoding (clause per relation)."""
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Cadical153
    import threading
    idx = {v: i + 1 for i, v in enumerate(A)}
    n = len(A)
    clauses = [[-idx[v] for v in sorted(r)] for r in rel_sets]
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.totalizer)
    solver = Cadical153(bootstrap_with=clauses + card.clauses)
    t0 = time.time()
    # Cadical in pysat has no interrupt: run with a watchdog via solve_limited is unsupported -> plain solve
    res = solver.solve()
    dt = time.time() - t0
    model = solver.get_model() if res else None
    solver.delete()
    wit = [A[i - 1] for i in range(1, n + 1) if model[i - 1] > 0] if res else None
    return res, dt, wit


def frontier_dp_h(order, edges):
    """Exact max independent set of a 3-uniform hypergraph (no edge fully chosen) by a frontier DP
    over the given vertex order.  Generic: correct for any order, efficient when the frontier is small.
    Returns (h, max number of active vertices)."""
    pos = {v: i for i, v in enumerate(order)}
    last = {}
    by_vertex = defaultdict(list)
    for e in edges:
        for v in e:
            by_vertex[v].append(e)
        last[e] = max(pos[v] for v in e)
    drop_after = {v: max([last[e] for e in by_vertex[v]] or [pos[v]]) for v in order}
    dp = {frozenset(): 0}
    maxfront = 0
    for i, v in enumerate(order):
        new = {}
        for sel, val in dp.items():
            for take in (0, 1):
                if take:
                    s2 = sel | {v}
                    if any(last[e] == i and all(u in s2 for u in e) for e in by_vertex[v]):
                        continue
                else:
                    s2 = sel
                s3 = frozenset(u for u in s2 if drop_after[u] > i)
                nv = val + take
                if new.get(s3, -1) < nv:
                    new[s3] = nv
        dp = new
        maxfront = max(maxfront, max(len(k) for k in dp))
    return max(dp.values()), maxfront


def transfer_vector(depth_max=200):
    """Max-plus transfer over copies; own DP over all 2^11 subsets T of O (T must avoid the 9 APs of O).
    best[(s, s')] = max |T| with anchor state s = (0 in T, 269 in T) and inner state s' = (101 in T, 119 in T).
    Copy j+1's anchors are copy j's inner points 101, 119, so consecutive copies share exactly those points.
    M[s][s'] = best[(s,s')] - |s|  (the |s| anchor points were already counted in the previous copy).
    R_0(s') = max_s best[(s,s')]  (outermost copy; state = its inner points);  R_j = R_{j-1} (x) M  (max-plus).
    h(S_K) = max_s' R_K(s').  Also returns the inner-to-outer direction V_t for a cross-check."""
    idx = {v: i for i, v in enumerate(O)}
    S = set(O)
    aps = []
    for i, a in enumerate(O):
        for c in O[i + 1:]:
            if (a + c) % 2 == 0 and (a + c) // 2 in S:
                aps.append((idx[a], idx[(a + c) // 2], idx[c]))
    assert len(aps) == 9, len(aps)
    apmask = [sum(1 << v for v in e) for e in aps]
    NEG = -10**9
    best = {}
    for T in range(1 << 11):
        if any(T & m == m for m in apmask):
            continue
        s = ((T >> idx[0]) & 1, (T >> idx[269]) & 1)
        sp = ((T >> idx[101]) & 1, (T >> idx[119]) & 1)
        c = bin(T).count("1")
        if c > best.get((s, sp), NEG):
            best[(s, sp)] = c
    states = [(0, 0), (1, 0), (0, 1), (1, 1)]
    M = [[best.get((s, sp), NEG) - sum(s) for sp in states] for s in states]
    R = [max(best.get((s, sp), NEG) for s in states) for sp in states]
    Rs = [list(R)]
    for _ in range(depth_max):
        R = [max(R[i] + M[i][k] for i in range(4)) for k in range(4)]
        Rs.append(list(R))
    # inner-to-outer direction
    V = [max(best.get((s, sp), NEG) for sp in states) for s in states]
    Vs = [list(V)]
    for _ in range(depth_max):
        V = [max((best.get((s, sp), NEG) + V[states.index(sp)] - sum(sp)) for sp in states) for s in states]
        Vs.append(list(V))
    return states, best, M, Rs, Vs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ks", default="0,1,2,3,4,5,6,7,8")
    ap.add_argument("--no-sat", action="store_true")
    ap.add_argument("--no-cpsat", action="store_true")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--cpsat-tlim", type=float, default=900)
    ap.add_argument("--cpsat-tlim-plain", type=float, default=240)
    a = ap.parse_args()
    ks = [int(k) for k in a.ks.split(",")]
    fam = {m["K"]: m for m in json.loads((REPO / "data" / "reader_5_9_family.json").read_text())["family"]}
    out = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    for K in ks:
        t0 = time.time()
        A = sorted(fam[K]["set"])
        n = len(A)
        r = {"K": K, "n": n, "expected_n": 11 + 9 * K, "distinct": len(set(A)) == n, "expected_h": 7 + 5 * K}
        ok, cnt, mn = four_subset_test(A)
        r.update(own_4subset_ok=ok, n_4subsets=cnt, min_distinct_diffs=mn, e757_is_45=bool(core.is_45_set(A)))
        if K <= 5:
            r["literal_BB_ge_11"] = literal_BB(A)
        c = census(A)
        r.update(m_aps=c["n_aps"], expected_m=9 * (K + 1), parallelograms=c["parallelograms"],
                 other_multi=c["other_multi"], ap_pairs_sharing_two_points=c["ap_pairs_sharing_two_points"],
                 n_relation_sets=len(c["rel_sets"]), e757_n_aps=len(core.ap_edges(A)))
        # which copy contains each AP: all three points inside one phi^j(O) ?
        scale = fam[K]["scale"]
        from fractions import Fraction as F
        L = F(27169, 251)
        copies = []
        for j in range(K + 1):
            cp = {int((L + F(18, 269) ** j * (F(x) - L)) * scale) for x in O}
            copies.append(cp)
        r["aps_inside_one_copy"] = sum(1 for e in c["aps"] if any(set(e) <= cp for cp in copies))
        r["copies_cover_set"] = set().union(*copies) == set(A)
        r["consecutive_copies_share"] = [len(copies[j] & copies[j + 1]) for j in range(K)]
        r["nonconsecutive_copies_share"] = max([len(copies[i] & copies[j]) for i in range(K + 1) for j in range(i + 2, K + 1)] or [0])
        if K <= 2:
            r["e757_alpha"] = core.alpha(A)
        order = sorted(A, key=lambda v: (min(j for j in range(K + 1) if v in copies[j]), v))
        hdp, mf = frontier_dp_h(order, c["aps"])
        r.update(frontier_dp_h=hdp, frontier_dp_max_active=mf)
        if not a.no_cpsat:
            for tag, cps, tl in (("plain", None, a.cpsat_tlim_plain if K >= 4 else a.cpsat_tlim), ("cuts", copies, a.cpsat_tlim)):
                if tl <= 0:
                    continue
                st, obj, bnd, wit, wt = cpsat_h(A, c["aps"], workers=a.workers, tlim=tl, copies=cps)
                r[f"cpsat_{tag}"] = dict(status=st, obj=obj, bound=bnd, wall=round(wt, 1), witness_size=len(wit),
                                         witness_is_sidon_by_definition=is_sidon_def(wit), witness_is_subset=set(wit) <= set(A),
                                         witness=wit, proved_optimal=(st == "OPTIMAL" and obj == bnd))
        if not a.no_sat:
            h = 7 + 5 * K
            res1, dt1, w1 = sat_card(A, c["rel_sets"], h, None)
            r.update(sat_ge_h=res1, sat_ge_h_sec=round(dt1, 1), sat_ge_h_model_ok=(w1 is not None and len(w1) >= h and is_sidon_def(w1)))
            res2, dt2, _ = sat_card(A, c["rel_sets"], h + 1, None)
            r.update(sat_ge_h1=res2, sat_ge_h1_sec=round(dt2, 1))
        r["wall_sec"] = round(time.time() - t0, 1)
        out[str(K)] = r
        RESULTS.write_text(json.dumps(out, indent=1, default=str))
        print({k: v for k, v in r.items() if k != "witness"}, flush=True)
    states, best, M, Rs, Vs = transfer_vector(200)
    R0 = Rs[0]
    eig = [max(R0[i] + M[i][k] for i in range(4)) for k in range(4)]
    tm = {"states": states, "best_T_size": {f"{k[0]}|{k[1]}": v for k, v in best.items()}, "M": M, "R_0": R0,
          "R_0 (x) M": eig, "R_0 (x) M == R_0 + 5 (finite eigenvector check)": eig == [x + 5 for x in R0],
          "R_t == R_0 + 5t for t<=200": all(Rs[t] == [x + 5 * t for x in R0] for t in range(201)),
          "h(S_t)=max R_t == 7+5t for t<=200": all(max(Rs[t]) == 7 + 5 * t for t in range(201)),
          "inner-to-outer V_0": Vs[0], "V_t == V_0 + 5t for t<=200": all(Vs[t] == [x + 5 * t for x in Vs[0]] for t in range(201))}
    out["transfer_matrix"] = tm
    RESULTS.write_text(json.dumps(out, indent=1, default=str))
    print("transfer:", tm)


if __name__ == "__main__":
    main()
