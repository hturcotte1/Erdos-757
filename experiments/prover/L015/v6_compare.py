#!/usr/bin/env python3
"""L015 / C6: compare this certificate's own numbers with the agent's (experiments/20261020-1730-reader-5-9/,
read as data only, no code imported).  Own numbers: v3_family_results.json (n, APs, census), v4_h_output.txt (h),
and the transfer table recomputed here by a third method (recursive extension of AP-free sets).
Run:  python3 -I v6_compare.py
"""
import json
import re

AG = "/home/user/Erdos-757/experiments/20261020-1730-reader-5-9/"
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
ST = [(0, 0), (1, 0), (0, 1), (1, 1)]
E = [set(e) for e in [(0, 49, 98), (49, 75, 101), (49, 83, 117), (49, 159, 269), (75, 98, 121), (75, 117, 159),
                      (83, 101, 119), (83, 121, 159), (117, 119, 121)]]

# third method for best[s][s']: depth-first extension in the order of O, pruning when a new point completes an AP
best = {}


def dfs(i, U):
    if i == len(O):
        s = (int(0 in U), int(269 in U))
        sp = (int(101 in U), int(119 in U))
        best[(s, sp)] = max(best.get((s, sp), -1), len(U))
        return
    dfs(i + 1, U)
    x = O[i]
    if not any(x in e and (e - {x}) <= U for e in E):
        dfs(i + 1, U | {x})


dfs(0, frozenset())
myM = [[best[(s, sp)] - sum(s) for sp in ST] for s in ST]
myR0 = [max(best[(s, sp)] for s in ST) for sp in ST]
cr = json.load(open(AG + "check_results.json"))
tm = cr["transfer_matrix"]
agbest = {k: v for k, v in tm["best_T_size"].items()}
mybest = {f"{s}|{sp}": best[(s, sp)] for s in ST for sp in ST}
print("transfer table: mine (third method) == agent's best_T_size:", mybest == agbest)
print("M: mine", myM, " agent", tm["M"], " equal:", myM == tm["M"])
print("R0: mine", myR0, " agent", tm["R_0"], " equal:", myR0 == tm["R_0"])
mine3 = {r["K"]: r for r in json.load(open("v3_family_results.json"))}
h4 = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r"\(b\) K=(\d+) n=\d+ APs=\d+: alpha = (\d+)", open("v4_h_output.txt").read())}
allok = mybest == agbest and myM == tm["M"] and myR0 == tm["R_0"]
print("K | n mine/agent | APs mine/agent | h mine(generic B&B)/agent(frontier DP, SAT>=h, SAT>=h+1, CP-SAT cuts)")
for K in range(9):
    a = cr[str(K)]
    m = mine3[K]
    cps = a.get("cpsat_cuts", {})
    row_ok = (m["n"] == a["n"] and m["APs"] == a["m_aps"] and h4.get(K) == a["frontier_dp_h"] == 7 + 5 * K
              and a["sat_ge_h"] is True and a["sat_ge_h1"] is False and a["parallelograms"] == 0 and a["ap_pairs_sharing_two_points"] == 0)
    allok &= row_ok
    print(f"{K} | {m['n']}/{a['n']} | {m['APs']}/{a['m_aps']} | {h4.get(K)}/{a['frontier_dp_h']}, {a['sat_ge_h']}, {a['sat_ge_h1']}, "
          f"{cps.get('status')} {cps.get('obj')}/{cps.get('bound')} | {'agree' if row_ok else 'DIFFER'}")
cd = {r["K"]: r for r in json.load(open(AG + "census_deep_results.json"))}
common = sorted(set(cd) & set(mine3))
for K in common:
    a, m = cd[K], mine3[K]
    ok = a["n"] == m["n"] and a["n_aps"] == m["APs"] and a["non_AP_coincidences_(parallelograms/other)"] == 0 == m["non_AP_relations"] \
        and a["point_pairs_in_two_APs"] == 0 == m["pairs_in_two_APs"] and a["max_span_of_APs_in_minimal_levels"] == m["max_level_span_of_an_AP"]
    allok &= ok
    print(f"census K={K}: n {m['n']}/{a['n']}, APs {m['APs']}/{a['n_aps']}, span {m['max_level_span_of_an_AP']}/{a['max_span_of_APs_in_minimal_levels']}: {'agree' if ok else 'DIFFER'}")
print("ALL COMPARISONS AGREE" if allok else "SOME COMPARISON DIFFERS")
