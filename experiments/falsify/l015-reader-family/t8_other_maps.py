"""Side data: other (c,a) maps for which the claim-set (sharing + no cross-copy relation, K=3) holds with the same O.
Report per-copy growth of h (DP exact at K=12, 16) -> ratio limit. Informational only."""
import json
from lib import *
from t5_perturb import analyze
pairs = [(75,8),(75,23),(75,26),(75,42),(75,44),(75,46),(83,15),(83,18),(83,34),(83,36),(83,38),(98,3),(98,19),(98,21),(98,23),(101,16),(101,18),(101,20),(101,58),(117,2),(117,4),(117,42),(119,2),(119,40),(121,38)]
out = []
for c, a in pairs:
    r = {"c": c, "a": a}
    hs = {}
    for K in (4, 8, 12, 16):
        an = analyze(O0, c, a, K)
        n = len(an["_pts"]); hs[K] = (n, alpha_frontier_dp(n, an["_ps"]), an["n_4pt_relations"], an["all_relations_in_one_copy"], an["copy_intersections_claim"])
    r["K->(n,h,4ptrel,onecopy,sharing)"] = hs
    n8, h8 = hs[8][:2]; n16, h16 = hs[16][:2]
    r["growth_per_copy_K8to16"] = (h16 - h8) / 8; r["points_per_copy"] = (n16 - n8) / 8
    tr = transfer(O0, c, a); r["transfer_pred_K16"] = predict_h(O0, 16, c, a)
    out.append(r); print(r, flush=True)
json.dump(out, open("t8_other_maps.json", "w"), indent=1)
