"""Triples (n,m,tau), n<=27, with A = 27n+35m-132tau <= AMAX that a connected member of C_3 can have
(I11 s>=0 by L016 for n<=27; K8 17tau<=5n+3m; connectivity 2m+1>=n; (P3) m<=n-2 (n>=4); 3m>=n), and the best stored D3 list.
Sources (priority): refereed L012-L016 extracted in experiments/prover/L017/out, then OUR out/cells (cells_ref symlinks + computed here).
usage: python3 scan2.py AMAX > scan2_AMAX.txt ; writes scan2_AMAX.json"""
import os, re, sys, json
AMAX = int(sys.argv[1])
H = '/home/user/Erdos-757/experiments'
ROOTS = [('refereed L017/out', H + '/prover/L017/out'), ('OWN out/cells', H + '/20261027-0730-kt-cells/out/cells'),
         ('seed cells_ref (computed-from-refereed, 0340 worker)', H + '/20261027-0340-induction-n28-n29-f25/out/cells_ref'),
         ('0340 out/cells (other workers, unrefereed)', H + '/20261027-0340-induction-n28-n29-f25/out/cells')]
pat = re.compile(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$')
stored = {}
for lab, root in ROOTS:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            mm = pat.match(f)
            if mm:
                n, m, t, D = map(int, mm.groups())
                pth = os.path.join(dp, f)
                if lab == 'OWN out/cells' and os.path.islink(pth): lab2 = 'seed (symlink into 0340 out/cells_ref: refereed or computed by the 0340 worker; see PROVENANCE.md)'
                elif lab == 'OWN out/cells': lab2 = 'OWN (computed in this folder)'
                else: lab2 = lab
                if D >= 3:
                    stored.setdefault((n, m, t), []).append((lab2, D, pth))
def count(p): return sum(1 for l in open(p) if l.startswith('FOUND'))
rows = []
for n in range(3, 28):
    for m in range(1, n - 1 if n > 3 else 2):
        if 2 * m + 1 < n or 3 * m < n: continue
        for t in range(1, m + 1):
            s = 3 * n + 2 * m - 11 * t
            if s < 0 or 17 * t > 5 * n + 3 * m: continue
            A = 27 * n + 35 * m - 132 * t
            if A > AMAX: continue
            c = stored.get((n, m, t), [])
            if c:
                c.sort(key=lambda x: (x[1], ))
                lab, D, p = c[0]
                rows.append(dict(n=n, m=m, tau=t, s=s, A=A, src=lab, D=D, path=p, classes=count(p)))
            else:
                rows.append(dict(n=n, m=m, tau=t, s=s, A=A, src=None))
for r in rows:
    print(f"({r['n']},{r['m']},{r['tau']}) s={r['s']} A={r['A']}  ->  " + (f"{r['src']} D{r['D']} {r['classes']} classes" if r['src'] else 'NOT STORED'))
json.dump(rows, open(f'scan2_{AMAX}.json', 'w'), indent=0)
