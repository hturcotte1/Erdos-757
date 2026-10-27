"""L021: list the (n,m,tau) cells with negative shifted slack A = 27n + 35m - 132 tau
(epsilon = 1/6, t = 11/12; A = 12*(s + n/6 - (11/12)(n-m))) that are allowed by I11 (s >= 0)
and by the class-C counting bounds, and say which of them have a stored complete Delta<=3 list.
Exact integer arithmetic only."""
import os, re, json, sys
ROOTS = ['/home/user/Erdos-757/experiments/prover/L017/out']
pat = re.compile(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$')
stored = {}
for root in ROOTS:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            mm = pat.match(f)
            if mm:
                n, m, t, D = map(int, mm.groups())
                key = (n, m, t)
                stored.setdefault(key, []).append((D, os.path.join(dp, f)))
def count(path):
    k = 0
    for l in open(path):
        if l.startswith('FOUND'): k += 1
    return k
rows = []
for n in range(3, 28):
    for m in range(1, n - 1 if n > 3 else 2):
        if 2 * m + 1 < n: continue          # connected
        if m > n - 2 and not (n == 3 and m == 1): continue   # P3
        if 3 * m < n: continue
        for t in range(1, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if s < 0: continue               # I11 (proved for n <= 27, L016)
            A = 27 * n + 35 * m - 132 * t
            if A >= 0: continue
            if 17 * t > 5 * n + 3 * m: continue   # Henning-Yeo K8
            lists = sorted(stored.get((n, m, t), []))
            best = [x for x in lists if x[0] >= 3]
            info = None
            if best:
                D, p = best[0]
                info = (D, p, count(p))
            elif lists:
                info = ('only D2', lists[0][1], count(lists[0][1]))
            rows.append(dict(n=n, m=m, tau=t, s=s, A=A, nm=n - m, stored=info))
for r in rows:
    st = r['stored']
    print(f"({r['n']},{r['m']},{r['tau']}) s={r['s']} n-m={r['nm']} A={r['A']}  ->  " + (f"D{st[0]} list, {st[2]} graphs  {os.path.relpath(st[1], ROOTS[0])}" if st else "NOT STORED"))
json.dump(rows, open('/home/user/Erdos-757/experiments/referee/L021-round1-ref1/prover_rerun/special_cells.json', 'w'), indent=0, default=str)
