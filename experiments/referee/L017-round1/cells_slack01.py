# Referee L017 round 1: enumerate connected cells (n,m,tau) of slack 0 and 1 (n<=30) and look up stored Delta<=3 counts.
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, 'cell_inventory.json')))
def cells(slack, nmax=30, use_hy=True):
    res = []
    for n in range(3, nmax+1):
        for m in range(max(1, math.ceil((n-1)/2)), n-1):   # m <= n-2 by (P3); connected: n <= 2m+1
            num = 3*n + 2*m - slack
            if num % 11: continue
            t = num // 11
            if t > m or t < 1: continue
            if use_hy and 17*t > 5*n + 3*m: continue
            res.append((n, m, t))
    return res
def stored(n, m, t):
    key = '%d_%d_%d' % (n, m, t)
    if key not in inv: return None
    best = None
    for (D, cnt, cnt3, path, ninfo) in inv[key]:
        if D >= 3:
            # number of classes with max degree <= 3 (classes are distinct across Delta-levels; a D4 list contains D3 classes)
            cand = (cnt3, D, path)
            if best is None or D == 3: best = cand
    return best if best else ('only D<=2 stored', [x[0] for x in inv[key]])
for s in (0, 1):
    print('=== slack', s, '(K8 applied) ===')
    for (n, m, t) in cells(s):
        print((n, m, t), 'stored Delta<=3:', stored(n, m, t))
    extra = sorted(set(cells(s, use_hy=False)) - set(cells(s)))
    print('cells excluded only by K8:', extra)
