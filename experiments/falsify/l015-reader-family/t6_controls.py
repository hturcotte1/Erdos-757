"""Controls: the checking code has power."""
import json, random
from lib import *
res = {}
# (1) 4-subset checker
res["min_diffs_{1,2,3,5}"] = min_distinct_diffs([1,2,3,5])        # expect 4 (not (4,5))
res["min_diffs_{0,1,3,7}"] = min_distinct_diffs([0,1,3,7])
# A_base known: h=8, (4,5)
Ab = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
res["A_base_min_diffs"] = min_distinct_diffs(Ab)
groups,_ = relation_groups(Ab); ps=[sorted(p) for p in relation_pointsets(groups)]
res["A_base_alpha_dp"] = alpha_frontier_dp(len(Ab), ps); res["A_base_alpha_cpsat"] = alpha_cpsat(len(Ab), ps)[1]
# (2) DP vs brute force vs CP-SAT on random hypergraphs
random.seed(1); bad = 0
for t in range(300):
    n = random.randint(5, 14)
    ps = [sorted(random.sample(range(n), random.choice([2,3,3,3,4]))) for _ in range(random.randint(1, 10))]
    bf = max(bin(m).count('1') for m in range(1 << n) if not any(all((m >> v) & 1 for v in P) for P in ps))
    if alpha_frontier_dp(n, ps) != bf or alpha_cpsat(n, ps)[1] != bf: bad += 1
res["dp_vs_bruteforce_vs_cpsat_random_hypergraphs_mismatches_of_300"] = bad
# (3) relation hashing finds a planted cross-copy relation
copies, ic, den = build(O0, 101, 18, 3); pts = points(ic)
a, b, c = ic[0][3], ic[2][4], ic[3][5]
p = a + b - c
pts2 = sorted(set(pts) | {p})
g, _ = relation_groups(pts2); rp = relation_pointsets(g)
res["planted_relation_detected_4pt"] = sum(1 for x in rp if len(x) == 4)
res["planted_min_diffs"] = min_distinct_diffs(pts2)
# (4) planted: the SAT/DP h must change or stay consistent with planted structure
ps2 = [sorted(x) for x in rp]
res["planted_alpha_dp"] = alpha_frontier_dp(len(pts2), ps2)
res["planted_alpha_sat_geq_22_and_23"] = (sat_atleast(len(pts2), ps2, 22), sat_atleast(len(pts2), ps2, 23))
# (5) sums_distinct_subset detects an AP
res["sidon_detects_AP"] = (sums_distinct_subset([1,2,3]), sums_distinct_subset([1,2,4]))
print(res); json.dump(res, open("t6_controls.json", "w"), indent=1)
