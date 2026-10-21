import json
r3 = json.load(open("step3_results.json")); r1 = json.load(open("step1_universality_dp.json"))
r2 = json.load(open("step2_all_universal.json")); r5 = json.load(open("step5_results.json"))
rows = ["| set | n | m (APs) | h (DP) | CP-SAT cuts | SAT (>=h, >=h+1) | h/n | 7h<4n | universal vertices after (indices) |", "|---|---|---|---|---|---|---|---|---|"]
for nm, r in r3.items():
    rows.append(f"| {nm} | {r['n']} | {r['m_aps']} | {r['h_dp']} (expected {r['expected_h']}) | {r['cpsat_cuts'][0]} {r['cpsat_cuts'][1]}/{r['cpsat_cuts'][2]} | {r['sat_ge_h']}, {r['sat_ge_h_plus_1']} | {r['ratio']} | {r['beats_4_7']} | {r['universal_vertices']} |")
open("table.md", "w").write("\n".join(rows) + "\n")
json.dump(dict(step1_min_max_universal=r1, step2_all_universal_vertices_of_SK=r2, step3_extensions=r3, step5_beam=r5), open("results.json", "w"), indent=1, default=str)
print("\n".join(rows))
