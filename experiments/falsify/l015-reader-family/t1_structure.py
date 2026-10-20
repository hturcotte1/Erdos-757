import sys, json, time
from lib import *

def check_structure(O, c, a, K, verbose=False):
    copies, ic, den = build(O, c, a, K)
    pts = points(ic); n = len(pts); idx = {p: i for i, p in enumerate(pts)}
    res = {"K": K, "n": n}
    res["n_ok"] = (n == 11 + 9*K)
    # copy intersections
    sets = [set(cp) for cp in ic]
    inter_ok = True
    for j in range(K+1):
        for jj in range(j+1, K+1):
            I = sets[j] & sets[jj]
            if jj == j+1:
                exp = {ic[j][O.index(101)], ic[j][O.index(119)]}
                exp2 = {ic[jj][O.index(0)], ic[jj][O.index(269)]}
                if not (I == exp == exp2): inter_ok = False
            else:
                if I: inter_ok = False
    res["copy_intersections_ok"] = inter_ok
    cnt = {}
    for s in sets:
        for p in s: cnt[p] = cnt.get(p, 0) + 1
    res["no_point_in_3_copies"] = max(cnt.values()) <= 2
    # relations
    groups, false = relation_groups(pts)
    res["hash_false_groups"] = false
    res["max_group_size"] = max((len(g) for g in groups), default=0)
    rps = relation_pointsets(groups)
    res["n_relations_groups"] = len(groups)
    res["n_distinct_pointsets"] = len(rps)
    res["n_4point_relations"] = sum(1 for r in rps if len(r) == 4)
    aps = {r for r in rps if len(r) == 3}
    # AP must be genuine: middle*2 = sum of other two, and the group pairs are (u,u),(v,w)
    gen = all(any(2*pts[sorted(r)[1]] == pts[sorted(r)[0]] + pts[sorted(r)[2]] for _ in [0]) for r in aps)
    res["aps_are_3AP"] = gen
    # expected
    Eidx = [tuple(O.index(v) for v in e) for e in apsO(O)]
    exp = set()
    for J in range(K+1):
        for e in Eidx:
            exp.add(frozenset(idx[ic[J][i]] for i in e))
    res["n_expected_APs"] = len(exp)
    res["AP_set_equals_expected"] = (aps == exp)
    # each AP inside exactly one copy
    cidx = [set(idx[p] for p in s) for s in sets]
    res["each_AP_in_exactly_one_copy"] = all(sum(1 for cs in cidx if r <= cs) == 1 for r in aps)
    # linear
    lst = list(aps); lin = True
    from collections import defaultdict
    byp = defaultdict(list)
    for t, r in enumerate(lst):
        for p in r: byp[p].append(t)
    seenpair = set()
    for p, ts in byp.items():
        for x, y in combinations(ts, 2):
            if (x, y) in seenpair: lin = False
            seenpair.add((x, y))
    res["linear_pairs_share_le_1"] = all(len(lst[x] & lst[y]) <= 1 for (x, y) in seenpair)
    # midpoints: each non-extreme point is middle of exactly one AP
    mids = [sorted(r)[1] for r in aps]
    res["midpoints_distinct_and_cover_nonextreme"] = (len(set(mids)) == len(mids) == n - 2 and set(mids) == set(range(1, n-1)))
    res["max_deg"] = max(len(v) for v in byp.values())
    return res

if __name__ == "__main__":
    out = []
    Ks = list(range(0, 13)) + [30, 61, 100, 200]
    for K in Ks:
        t = time.time()
        r = check_structure(O0, 101, 18, K)
        r["sec"] = round(time.time() - t, 1)
        ok = all(v for k, v in r.items() if isinstance(v, bool))
        r["ALL_OK"] = ok and r["n_4point_relations"] == 0 and r["hash_false_groups"] >= 0
        print(r, flush=True)
        out.append(r)
    json.dump(out, open("t1_structure.json", "w"), indent=1)
    print("ALL_K_OK", all(r["ALL_OK"] for r in out))
