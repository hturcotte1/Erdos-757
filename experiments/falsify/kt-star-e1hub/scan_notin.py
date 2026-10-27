#!/usr/bin/env python3
"""Count low-degree (deg<=2) vertices lying in NO minimum transversal, over every stored connected Delta<=3 class with n<=NMAX
(all cells of the L012-L016 tarballs, any A).  Such vertices are needed for non-trivial disjoint-union b-configurations."""
import sys, glob, re, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hubs, kt
NMAX = int(sys.argv[1]); res = {}
seen = {}
for f in sorted(glob.glob('/home/user/Erdos-757/experiments/prover/L017/out/L01[2-6]/cells*/cell_*_D3.txt')):
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D3\.txt', os.path.basename(f)); n, m, t = map(int, mm.groups())
    if n > NMAX or os.path.getsize(f) > 3_000_000: continue
    key = (n, m, t)
    if key in seen: continue
    seen[key] = f
    cnt = 0; tot = 0; vert_any = 0
    for g in kt.read_cell(f):
        if max(hubs.degs(n, g)) > 3: continue
        tot += 1
        T = kt.min_transversals(kt.masks(g), t); inT = 0
        for tr in T: inT |= tr
        d = hubs.degs(n, g)
        nn = sum(1 for x in range(n) if d[x] <= 2 and not (inT >> x) & 1)
        nall = sum(1 for x in range(n) if not (inT >> x) & 1)
        cnt += nn; vert_any += nall
    res[str(key)] = dict(graphs=tot, low_notinT=cnt, any_notinT=vert_any)
    if tot: print(key, res[str(key)], flush=True)
json.dump(res, open('scan_notin.json', 'w'), indent=1)
