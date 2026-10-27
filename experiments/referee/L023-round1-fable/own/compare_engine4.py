"""Compare my degree-4-side recomputation (engine4/cells, from refereed seeds only) with U1's out/cells and the prover's repro4/cells
(sets of FOUND lines and of edge sets); keys = the 8 unrefereed lists of the degree-4 subtree plus the two top-level component cells."""
import os, re, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U1 = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
REP4 = '/home/user/Erdos-757/experiments/prover/L023/repro4/cells'
def load(p):
    F = set(); info = None
    for l in open(p):
        if l.startswith('FOUND:'): F.add(l.rstrip('\n'))
        if l.startswith('INFO '): info = json.loads(l[5:])
    return F, info
def es(F): return set(frozenset(tuple(sorted(map(int, g))) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', l)) for l in F)
allok = True
for k in ['16_9_6_D4', '17_13_7_D4', '19_10_7_D4', '20_14_8_D4', '22_11_8_D4', '23_15_9_D4', '21_18_9_D4', '24_19_10_D4']:
    mine = os.path.join(R, 'engine4', 'cells', 'cell_%s.txt' % k)
    if not os.path.exists(mine): print('%-12s not yet computed' % k); allok = False; continue
    Fm, im = load(mine)
    if im is None: print('%-12s incomplete' % k); allok = False; continue
    res = []
    for name, d in (('U1', U1), ('repro4', REP4)):
        q = os.path.join(d, 'cell_%s.txt' % k)
        if os.path.exists(q):
            Fo, io = load(q); res.append('%s:%s/%s' % (name, 'EQUAL' if Fm == Fo else 'DIFF-lines', 'EQUAL' if es(Fm) == es(Fo) else 'DIFF-sets'))
            if Fm != Fo: allok = False
    br = im.get('branches', [])
    print('%-12s mine %6d classes (%s, inputs %s, bad_tau %s, %.1fs) | %s' % (k, len(Fm), im.get('route'), [b.get('inputs') for b in br], [b.get('ext', {}).get('bad_tau') for b in br], im.get('secs', 0), ' '.join(res)))
print('ALL EQUAL:', allok)
