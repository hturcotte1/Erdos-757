"""Find census class indices of the three known 12-point sets (affine canonical form incl. reflection)."""
import gzip, json
from math import gcd
from functools import reduce
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'
def canon(S):
    S = sorted(S)
    def norm(T):
        T = sorted(T); m = T[0]; T = [t - m for t in T]
        g = reduce(gcd, T); return tuple(t // g for t in T)
    return min(norm(S), norm([-s for s in S]))
known = {'12': [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575],
         '12b': [0, 178, 198, 218, 227, 235, 272, 276, 287, 317, 356, 436],
         '12c': [-336, -168, -44, -24, -4, 0, 39, 44, 49, 80, 102, 160]}
cen = json.load(gzip.open(CENSUS, 'rt'))
idx = {}
for i, r in enumerate(cen):
    idx.setdefault(canon(r['set']), []).append(i)
print('distinct canonical forms in census:', len(idx), 'of', len(cen))
for k, v in known.items():
    print(k, idx.get(canon(v)))
