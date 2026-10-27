"""L026 C8: the I11 form on stored data (own code, ownlib.py only).
For every graph of the given lists (any maximum degree): tau, all minimum transversals, the
non-co-transversal pairs, and every b-configuration in the wide sense used in Theorem 11 (three vertices,
any degrees, pairwise non-co-transversal, not an edge).  Theorem 11 predicts: none in a tight graph.
For slack-1 graphs it reports the counts (none expected from the earlier role tables), and for every
pairwise-NC triple that IS an edge (only E_1-type) it reports it separately.
Usage: python3 i11_form_check.py <list files ...>"""
import sys, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L

def load(path):
    out = L.read_found(path)
    if not out: out = L.read_flat(path)
    return out

tot = {}
for f in sys.argv[1:]:
    t0 = time.time()
    c = dict(graphs=0, tight=0, slack1=0, bconf_tight=0, bconf_slack1=0, bconf_other=0, edge_triples=0)
    for E in load(f):
        n = L.nv(E); m = len(E); t = L.tau(E); s = 3 * n + 2 * m - 11 * t
        c['graphs'] += 1
        if s == 0: c['tight'] += 1
        if s == 1: c['slack1'] += 1
        T = L.all_min_transversals(E, t)
        co = set()
        for Tm in T:
            vs = [i for i in range(n) if Tm >> i & 1]
            for p in itertools.combinations(vs, 2): co.add(p)
        NCadj = [set() for _ in range(n)]
        for x, y in itertools.combinations(range(n), 2):
            if (x, y) not in co: NCadj[x].add(y); NCadj[y].add(x)
        Es = set(tuple(sorted(e)) for e in E)
        for x in range(n):
            for y in NCadj[x]:
                if y <= x: continue
                for z in NCadj[x] & NCadj[y]:
                    if z <= y: continue
                    if (x, y, z) in Es: c['edge_triples'] += 1; continue
                    if s == 0: c['bconf_tight'] += 1; print('TIGHT B-CONF (contradicts Thm 11)', f, E, (x, y, z))
                    elif s == 1: c['bconf_slack1'] += 1; print('slack-1 b-conf', f, E, (x, y, z))
                    else: c['bconf_other'] += 1
    print(f.split('/')[-1], c, '[%ds]' % (time.time() - t0), flush=True)
    for k, v in c.items(): tot[k] = tot.get(k, 0) + v
print('TOTAL', tot)
