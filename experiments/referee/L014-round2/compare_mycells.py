"""Referee L014 round 2: compare every list of my bottom-up engine (out/mycells) with the prover's list of the same key
(tracked cells.tar.gz extracted to out/tracked/cells) as sets of isomorphism classes (labelg, own nauty build)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canon_cmp import canon, read_hg
H = os.path.dirname(os.path.abspath(__file__)); MY = os.path.join(H, 'out', 'mycells'); TR = os.path.join(H, 'out', 'tracked', 'cells')
eq = df = miss = 0
for fn in sorted(os.listdir(MY)):
    k = tuple(map(int, re.findall(r'\d+', fn)))
    n, m, t, D = k
    mine = [l for l in open(os.path.join(MY, fn)) if not l.startswith('#')]
    route = [l for l in open(os.path.join(MY, fn)) if l.startswith('#DONE')][0]
    route = 'genbg' if '"genbg"' in route else 'recursion'
    pf = os.path.join(TR, fn)
    if not os.path.exists(pf): print('KEY', k, 'mine', len(mine), 'prover: no file'); miss += 1; continue
    A = read_hg(os.path.join(MY, fn), n, m); B = read_hg(pf, n, m)
    sa = set(canon(n, m, A)) if A else set(); sb = set(canon(n, m, B)) if B else set()
    same = (sa == sb and len(sa) == len(A) and len(sb) == len(B))
    eq += same; df += (not same)
    print('KEY', k, 'route', route, 'mine', len(A), 'classes', len(sa), 'prover', len(B), 'classes', len(sb), 'IDENTICAL' if same else 'DIFFERENT')
print('SUMMARY compared', eq + df, 'identical', eq, 'different', df, 'no prover file', miss)
