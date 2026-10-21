"""Universal vertices of S_K (all vertices), K=0..6, exact DP."""
import json
from lib import *
out = {}
for K in range(0, 7):
    A, copies = family(K); g = groups_for(A, copies)
    h, _ = alpha_dp(A, g)
    uni = [v for v in A if alpha_dp(A, g, [v])[0] == h - 1]
    out[K] = dict(n=len(A), h=h, universal=uni, n_universal=len(uni), universal_are_min_max=(set(uni) == {min(A), max(A)}))
    print(K, len(A), h, len(uni), [A.index(v) for v in uni], flush=True)
json.dump(out, open("step2_all_universal.json", "w"), indent=1)
