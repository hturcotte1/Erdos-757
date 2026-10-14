import gzip, json, sys, pickle, os
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, os.path.dirname(__file__))
from stats import stats
from e757.saturated import map_of_set
base = '/home/user/Erdos-757/experiments/'
out = {}
# n=12 realizable
real = json.load(gzip.open(base + '20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
rset = set(); R12 = []
for r in real:
    es = tuple(sorted(tuple(e) for e in r['edges']))
    rset.add(es)
    refl = tuple(sorted((11 - k, 11 - j, 11 - i) for (i, j, k) in es))
    rset.add(refl)
    R12.append(es)
print(len(R12), len(rset))
# unrealizable: filtered rows with c4 == 1, minus realized
U12 = []; Uall = 0
for line in gzip.open(base + '20261014-1005-census-dfs/results/n12_m10_filtered.txt.gz', 'rt'):
    p = line.split()
    if p[2] != '1' or p[1] != '1':  # k31 and c4
        continue
    Uall += 1
    es = tuple(tuple(int(x) for x in t.split(',')) for t in p[4:])
    es = tuple(sorted(es))
    if es in rset: continue
    U12.append(es)
print('c4 rows', Uall, 'unrealizable', len(U12))
# n=14
sets14 = json.load(open(base + '20261014-0610-extremal-census/results/n14_realizable_sets_partial.json'))
R14 = []
for A in sets14:
    lo, hi, mid = map_of_set(A)
    es = tuple(sorted((a, j, c) for j, (a, c) in mid.items()))
    assert len(es) == 12
    R14.append(es)
res = {}
for name, lst, n in (('R12', R12, 12), ('U12', U12, 12), ('R14', R14, 14)):
    res[name] = [stats(e, n) for e in lst]
    print(name, len(res[name]), flush=True)
pickle.dump(res, open(os.path.join(os.path.dirname(__file__), 'stats.pkl'), 'wb'))
