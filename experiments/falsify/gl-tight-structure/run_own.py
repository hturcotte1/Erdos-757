import sys, json, collections
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, '.')
from lemmas import *
from e757.cpsat_model import enumerate_solutions
res = {}; allf = []
for n, limit, seed in ((8, 1000, 1), (10, 1000, 2), (12, 400, 7)):
    st = collections.Counter(); sols = []
    cnt, sols, status = enumerate_solutions(n, n // 2 + 1 - 1 + 1 - 1 + 0 if False else n - (n // 2 - 1) , n - 2, limit=limit, time_limit=120, workers=1, seed=seed)
    for edges, a in sols:
        f = check_all(n, edges, st, None); allf += f
    res[n] = dict(count=cnt, status=status, stats=dict(st)); print(n, res[n], len(allf))
json.dump({'res': res, 'failures': allf[:20]}, open('own_results.json', 'w'), indent=1, default=str)
