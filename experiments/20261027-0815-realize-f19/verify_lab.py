"""usage: verify_lab.py classfile outfile n out_json : for each RES..REAL + LAB in outfile, rebuild V exactly over Q from the labelling (rexact.Space), pick a random integer
point, verify distinctness, is_45_set, number of 3-APs, h=alpha (e757.core.alpha). Writes JSON list."""
import sys, re, json, random
from rexact import *
from e757.core import alpha
cf, of, n, oj = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
lim = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
classes = [l for l in open(cf) if l.startswith('FOUND:')]
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
res = []; cur = None
for l in open(of):
    if l.startswith('RES'): cur = int(l.split()[1])
    elif l.startswith('LAB'):
        if len(res) >= lim: break
        lab = parse(l); sp = Space(n)
        for a, mid, c in lab:
            row = [Fr(0)] * n; row[a] += 1; row[c] += 1; row[mid] -= 2; sp = sp.add(row)
        R, k = sp.coords(); kind, det, F = forced_events(R, n)
        iv = explicit_point((lab, k - 2, R, sp), n, random.Random(cur))
        r = dict(cls=cur, labelling=lab, dim=k - 2, forced_event=kind)
        if iv:
            from math import gcd
            lo = min(iv); iv = [x - lo for x in iv]; g = 0
            for x in iv: g = gcd(g, x)
            iv = [x // g for x in iv]
            E = ap_edges(iv); idx = {x: i for i, x in enumerate(sorted(iv))}
            got = {frozenset(idx[v] for v in e) for e in E}
            r.update(set=sorted(iv), is_45=is_45_set(iv), num_aps=len(E), h=alpha(iv, E))
        res.append(r)
        print(cur, {x: r.get(x) for x in ('dim','is_45','num_aps','h')}, flush=True)
json.dump(res, open(oj, 'w'))
