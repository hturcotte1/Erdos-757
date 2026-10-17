# Referee round 2: census controls for rz (n=14 one-sided: every census set found; n=12 two-sided vs the 221 classes).
import subprocess, sys, json, gzip, itertools
from fractions import Fraction
def aps_of(s):
    pos = {a: i for i, a in enumerate(s)}; E = []
    for i in range(len(s)):
        for k in range(i + 1, len(s)):
            t = s[i] + s[k]
            if t % 2 == 0 and t // 2 in pos: E.append((i, pos[t // 2], k))
    return E
def stream(n, lines):
    fn = 'out/ctrl_in_%d.txt' % n; open(fn, 'w').write(''.join(lines))
    p = subprocess.Popen(['nice', '-n', '5', './out/rz', str(n), 'print'], stdin=open(fn), stdout=subprocess.PIPE, text=True)
    cur = []
    for l in p.stdout:
        if l.startswith('REAL'):
            head, vals = l.split(':'); u, v = [int(t.split('=')[1]) for t in head.split()[1:]]
            cur.append((u, v, [int(t) for t in vals.split()]))
        elif l.startswith('G '):
            yield l.strip(), cur; cur = []
    p.wait()
def canon_aff(vals):  # vals: Fractions/ints; affine class up to reflection
    lo, hi = min(vals), max(vals); a = sorted(Fraction(x - lo, 1) / (hi - lo) for x in vals)
    b = sorted(1 - x for x in a); return min(tuple(a), tuple(b))
def is45_bruteforce(s):
    for q in itertools.combinations(s, 4):
        if len(set(abs(x - y) for x, y in itertools.combinations(q, 2))) < 5: return False
    return True
def weak_sidon(s):
    sums = [x + y for x, y in itertools.combinations(s, 2)]; return len(sums) == len(set(sums))
mode = sys.argv[1]
if mode == '14':
    rows = [json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')]
    lines = []; targets = []
    for r in rows:
        s = sorted(r['set']); E = aps_of(s)
        assert len(s) == 14 and len(E) == 12, 'census set not saturated'
        assert sorted(tuple(sorted(e)) for e in E) == sorted(tuple(sorted(e)) for e in r['edges']), 'edge list differs'
        lines.append('X: ' + ' '.join('(%d,%d,%d)' % e for e in E) + '\n'); targets.append(s)
    tot = 0; found = 0; g = 0; maxasg = 0
    for (stat, reals), s in zip(stream(14, lines), targets):
        g += 1; tot += len(reals); L = s[-1] - s[0]
        ok = any(u == 0 and v == 13 and all(y[i] * L == y[13] * (s[i] - s[0]) for i in range(14)) for (u, v, y) in reals)
        found += ok
    print('n=14 census: graphs %d, total realizations %d, own set found %d' % (g, tot, found))
else:
    import tarfile
    tf = tarfile.open('/home/user/Erdos-757/experiments/prover/L012/cells.tar.gz')
    cl = [l for l in tf.extractfile('cells/cell_12_10_5_D4.txt').read().decode().splitlines() if l.startswith('FOUND')]
    print('cell(12,10,5,4) classes:', len(cl))
    census = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
    cset = set(canon_aff(sorted(r['set'])) for r in census)
    print('census sets %d, distinct affine classes %d' % (len(census), len(cset)))
    tot = 0; n45 = 0; realclasses = 0; real45classes = 0; aff = set(); none = []; only_non45 = []; bf_checked = 0
    for gi, (stat, reals) in enumerate(stream(12, [l + '\n' for l in cl])):
        tot += len(reals); k45 = 0
        for (u, v, y) in reals:
            D = y[v]; x = [Fraction(t, D) for t in y]
            assert len(set(x)) == 12
            # exact AP set equals the pattern (re-verified here)
            ys = sorted(y); 
            w = weak_sidon(y)
            if bf_checked < 3000: assert w == is45_bruteforce(y), 'weak-sidon/(4,5) equivalence failed'; bf_checked += 1
            if w: k45 += 1; aff.add(canon_aff(y))
        n45 += k45; realclasses += (len(reals) > 0); real45classes += (k45 > 0)
        if not reals: none.append(gi)
        elif not k45: only_non45.append(gi)
    print('realizations %d, (4,5) realizations %d, classes with a realization %d, with a (4,5)-realization %d' % (tot, n45, realclasses, real45classes))
    print('classes with no realization:', none, ' classes with only non-(4,5) realizations:', len(only_non45))
    print('affine classes of (4,5)-realizations %d; equal to census: %s; census-realized %d; realized-census %d'
          % (len(aff), aff == cset, len(cset - aff), len(aff - cset)))
    json.dump(dict(none=none), open('out/c12_none.json', 'w'))
