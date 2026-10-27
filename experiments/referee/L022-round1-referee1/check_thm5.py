# Referee check of L022 Theorem 5 (computational table): re-verify every stored explicit
# realization with independent code; recount Delta<=3 classes; obstruction degrees;
# independently re-decide a sample of classes reported NOT realizable.
import json, glob, random, sys, time
from rlib import is_45_fast, is_45_bruteforce, degree, tau, verts
from realize import decide, ap_edges_of_points

INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
OUT = '/home/user/Erdos-757/experiments/prover/L022/out/'


def load_cell(cell):
    out = []
    for line in open(INP + 'cell_%s.txt' % cell):
        a = list(map(int, line.split()))
        if not a:
            continue
        n, m, t = a[:3]
        e = [tuple(sorted(a[3 + 3 * i:6 + 3 * i])) for i in range(m)]
        out.append((n, m, t, e))
    return out


cells = ['3_1_1', '10_7_4', '14_12_6', '17_13_7', '8_5_3', '12_10_5', '15_11_6', '19_16_8', '22_17_9', '26_22_11']
summary = {}
nonreal = {}
for cell in cells:
    L = load_cell(cell)
    recs = [json.loads(l) for l in open(OUT + 'realize_%s.jsonl' % cell)]
    d3 = [i for i, (n, m, t, e) in enumerate(L) if max(degree(e, x) for x in range(n)) <= 3]
    tested = [r for r in recs if 'skipped' not in r]
    real = [r for r in tested if r.get('realizable')]
    nreal = [r for r in tested if r.get('realizable') is False]
    bad = 0
    for r in real:
        n, m, t, e = L[r['cls']]
        x = r['explicit']
        okd = len(set(x)) == n
        ok45 = is_45_fast(x) and (n > 26 or is_45_bruteforce(x))
        aps = ap_edges_of_points(x)
        okE = aps == set(e)
        if not (okd and ok45 and okE):
            bad += 1
            print('BAD realization', cell, r['cls'])
    # consistency: skipped == Delta>3 exactly
    skipped = set(r['cls'] for r in recs if 'skipped' in r)
    d3set = set(d3)
    tested_set = set(r['cls'] for r in tested)
    cons = all((i in d3set) == (i in tested_set) for i in set(r['cls'] for r in recs))
    summary[cell] = {'classes': len(L), 'Delta<=3': len(d3), 'records': len(recs), 'tested': len(tested),
                     'realizable': len(real), 'not_realizable': len(nreal), 'bad_realizations': bad,
                     'skip_consistent': cons, 'timeouts': sum(1 for r in tested if r.get('timeout'))}
    nonreal[cell] = [r['cls'] for r in nreal]
    print(cell, summary[cell], flush=True)
print('not realizable (cls):', nonreal)
# obstruction degrees
obs = json.load(open('/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9/obstructions.json'))
mx = []
for o in obs:
    E = [tuple(e) for e in o['subedges']]
    V = verts(E)
    mx.append(max(degree(E, x) for x in V))
print('obstruction max degrees:', mx)
# independent re-decision of a sample of NOT-realizable slack-1 classes
rng = random.Random(3)
sample = int(sys.argv[1]) if len(sys.argv) > 1 else 3
L = load_cell('12_10_5')
for c in nonreal['12_10_5'][:sample]:
    n, m, t, e = L[c]
    t0 = time.time()
    ok, info = decide(e, n, rng)
    print('12_10_5 class', c, 'realizable(any extra APs):', ok, info.get('stats'), '%.0fs' % (time.time() - t0), flush=True)
# and one realizable control per cell with my own decider (exact)
for cell in ('10_7_4', '17_13_7'):
    L = load_cell(cell)
    recs = [json.loads(l) for l in open(OUT + 'realize_%s.jsonl' % cell)]
    r = [r for r in recs if r.get('realizable')][0]
    n, m, t, e = L[r['cls']]
