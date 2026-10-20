#!/usr/bin/env python3
"""Assemble results.json and the markdown table from check_results.json, census_deep_results.json, literal_big_results.json,
lemma_constants.py (re-run), and the claim logs (claim_K6.log, claim_K7.log, standalone_verdict_K6.txt)."""
import json
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

here = Path(__file__).resolve().parent
chk = json.loads((here / "check_results.json").read_text())
deep = json.loads((here / "census_deep_results.json").read_text())
lit = json.loads((here / "literal_big_results.json").read_text())
rows = []
for K in range(9):
    r = chk[str(K)]
    h = 7 + 5 * K
    n = 11 + 9 * K
    ratio = F(h, n)
    cp = r.get("cpsat_cuts", {})
    rows.append(dict(K=K, n=n, m=r["m_aps"], h=h, ratio=str(ratio), ratio_float=round(float(ratio), 6),
                     below_4_7=ratio < F(4, 7), equal_4_7=ratio == F(4, 7),
                     h_equals_formula=(r["frontier_dp_h"] == h),
                     four_subset_test_ok=r["own_4subset_ok"], e757_is_45=r["e757_is_45"],
                     e757_alpha=r.get("e757_alpha"),
                     cpsat_plain=r.get("cpsat_plain", {}).get("status"), cpsat_plain_bound=r.get("cpsat_plain", {}).get("bound"),
                     cpsat_cuts=cp.get("status"), cpsat_cuts_obj=cp.get("obj"), cpsat_cuts_bound=cp.get("bound"), cpsat_cuts_sec=cp.get("wall"),
                     witness_sidon_by_definition=cp.get("witness_is_sidon_by_definition", r.get("cpsat_plain", {}).get("witness_is_sidon_by_definition")),
                     frontier_dp_h=r["frontier_dp_h"], sat_ge_h=r["sat_ge_h"], sat_ge_h_plus_1=r["sat_ge_h1"],
                     parallelograms=r["parallelograms"], ap_pairs_sharing_two_points=r["ap_pairs_sharing_two_points"]))
tm = chk["transfer_matrix"]
verdicts = {}
for name, fn in (("C003 (K=6) via new_claim.py", "claim_K6.log"), ("C004 (K=7) via new_claim.py", "claim_K7.log"), ("standalone judge.py on K=6 (timing run)", "standalone_verdict_K6.txt")):
    p = here / fn
    verdicts[name] = p.read_text() if p.exists() else None
res = dict(source="reader's 5/9 family [community]; all numbers below computed here [verified-here] unless marked",
           table=rows, transfer_matrix=tm, deep_census=deep, literal_4subset_K9_12=lit, judge_outputs=verdicts)
(here / "results.json").write_text(json.dumps(res, indent=1, default=str))
md = ["| K | n | m (APs) | h | h/n | < 4/7 ? | CP-SAT (plain) | CP-SAT (+local cuts) | frontier DP | SAT >=h / >=h+1 | judge |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    jd = ""
    md.append(f"| {r['K']} | {r['n']} | {r['m']} | {r['h']} | {r['ratio']} = {r['ratio_float']} | {'YES' if r['below_4_7'] else ('equal' if r['equal_4_7'] else 'no')} | {r['cpsat_plain']} (bound {r['cpsat_plain_bound']}) | {r['cpsat_cuts']} {r['cpsat_cuts_obj']}/{r['cpsat_cuts_bound']} ({r['cpsat_cuts_sec']}s) | {r['frontier_dp_h']} | {r['sat_ge_h']} / {r['sat_ge_h_plus_1']} | {jd} |")
(here / "table.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
