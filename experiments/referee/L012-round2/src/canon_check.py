# Referee round 2: the prover's canon binary -- invariance under random relabelling and faithfulness (output isomorphic to input,
# by BLISS key equality), on the 699 and on cell(19,16,8,4) / cell(12,10,5,4).  Also the degree statistics of the 699.
import sys, os, random, subprocess, re
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x', '0']
exec(open(os.path.join(H, 'bliss_classify.py')).read().split("nv = int(sys.argv[1])")[0])
CANON = '/home/user/Erdos-757/experiments/prover/L012/bin/canon'
def run_canon(nv, graphs):
    inp = ''.join('%d ' % len(E) + ' '.join('%d %d %d' % e for e in E) + '\n' for E in graphs)
    out = subprocess.run(['nice', '-n', '5', CANON, str(nv)], input=inp, capture_output=True, text=True).stdout.splitlines()
    return out
random.seed(2026)
for nv, fn in ((23, 'out/r4_699.txt'), (19, 'out/cells_x/cells/cell_19_16_8_D4.txt'), (12, 'out/cells_x/cells/cell_12_10_5_D4.txt')):
    G = [parse(l) for l in open(fn) if l.startswith('FOUND')]
    base = run_canon(nv, G)
    rel = []
    for E in G:
        for r in range(3):
            pi = list(range(nv)); random.shuffle(pi); E2 = [tuple(pi[v] for v in e) for e in E]; random.shuffle(E2); rel.append(E2)
    out = run_canon(nv, rel)
    inv_bad = sum(1 for i, o in enumerate(out) if o != base[i // 3])
    faith_bad = 0
    for E, o in zip(G, base):
        Ec = [tuple(map(int, p.split('.'))) for p in o.split()[2:]]
        if canon(nv, Ec)[0] != canon(nv, E)[0]: faith_bad += 1
    print('%s: graphs %d, relabellings %d, canon-invariance failures %d, unfaithful outputs %d, distinct canon outputs %d'
          % (fn.split('/')[-1], len(G), len(rel), inv_bad, faith_bad, len(set(base))))
G = [parse(l) for l in open('out/r4_699.txt')]
d4 = Counter(); d1 = Counter(); pats = Counter()
for E in G:
    deg = Counter(v for e in E for v in e)
    assert len(deg) == 23 and len(E) == 21
    d4[sum(1 for v in deg if deg[v] == 4)] += 1; d1[sum(1 for v in deg if deg[v] == 1)] += 1
    pats[tuple(sorted(Counter(deg.values()).items()))] += 1
print('699: #deg-4 vertices', dict(d4), ' #deg-1 vertices', dict(d1), ' degree patterns', len(pats))
