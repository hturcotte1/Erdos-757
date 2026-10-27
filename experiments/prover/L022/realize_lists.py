"""Exact realizability (rexact.decide of experiments/20261027-0400-realize-21-18-9) of the stored Delta<=3 tight and
slack-1 class lists (inputs of experiments/20261027-0300-transversal-richness, format 'n m tau a b c ...').
For each class: decide(find_all=False); if realizable, build an explicit integer point and check EXACTLY that it is a
(4,5)-set whose AP hypergraph equals the given edge set (exact realization).  Output: JSONL, one line per class.
usage: python3 realize_lists.py cellname [cellname ...]  (e.g. 17_13_7)"""
import sys, json, random, time, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9')
sys.path.insert(0, '/home/user/Erdos-757')
from rexact import decide, explicit_point
from e757.core import is_45_set
INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_%s.txt'
OUT = '/home/user/Erdos-757/experiments/prover/L022/out/realize_%s.jsonl'

def aps_of(vals):
    S = {x: i for i, x in enumerate(vals)}; out = set()
    for a, c in itertools.combinations(range(len(vals)), 2):
        s = vals[a] + vals[c]
        if s % 2 == 0 and s // 2 in S:
            out.add(frozenset((a, c, S[s // 2])))
    return out

for cell in sys.argv[1:]:
    lines = [l.split() for l in open(INP % cell) if l.strip()]
    with open(OUT % cell, 'w') as fo:
        for ci, t in enumerate(lines):
            n, m, tau = map(int, t[:3]); xs = list(map(int, t[3:]))
            E = [tuple(xs[3 * i:3 * i + 3]) for i in range(m)]
            d = [0] * n
            for e in E:
                for x in e: d[x] += 1
            D = max(d)
            rec = dict(cell=cell, cls=ci, n=n, m=m, tau=tau, maxdeg=D)
            if D > 3:
                rec['skipped'] = 'Delta>3'
            else:
                t0 = time.time()
                sols, st = decide(E, n, find_all=False, tlimit=1800)
                rec.update(realizable=bool(sols), timeout=st['timeout'], nodes=st['nodes'], secs=round(time.time() - t0, 1))
                if sols:
                    iv = explicit_point(sols[0], n, random.Random(ci))
                    if iv is None:
                        rec['explicit'] = None
                    else:
                        exact = aps_of(iv) == {frozenset(e) for e in E}
                        rec.update(explicit=iv, is45=is_45_set(sorted(iv)), exact_AP_hypergraph=exact,
                                   labelling=sols[0][0])
            fo.write(json.dumps(rec) + '\n'); fo.flush()
            print(cell, ci, {k: v for k, v in rec.items() if k not in ('explicit', 'labelling')}, flush=True)
