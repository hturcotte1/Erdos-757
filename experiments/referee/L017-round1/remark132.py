# Referee L017 round 1: Remark 13.2 / C2 on the Delta<=4 lists (independent co-transversality via Fact 0.4).
import os, re, subprocess, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = os.path.join(HERE, 'cells')
LISTS = [((3,1,1),'L012/cells/cell_3_1_1_D4.txt'), ((10,7,4),'L012/cells/cell_10_7_4_D4.txt'),
 ((14,12,6),'L012/cells/cell_14_12_6_D4.txt'), ((17,13,7),'L012/cells/cell_17_13_7_D3.txt'),
 ((12,10,5),'L012/cells/cell_12_10_5_D4.txt'), ((19,16,8),'L012/cells/cell_19_16_8_D4.txt'),
 ((22,17,9),'L012/cells/cell_22_17_9_D4.txt'), ((26,22,11),'L016/cells_new/runF/cell_26_22_11_D3.txt')]
def parse(path):
    return [[tuple(int(x) for x in t.split(',')) for t in re.findall(r'\(([^)]*)\)', l)] for l in open(path) if l.startswith('FOUND:')]
tot = collections.Counter()
for cell, rel in LISTS:
    n, m, t0 = cell; s = 3*n + 2*m - 11*t0
    gs = parse(os.path.join(CELLS, rel))
    inp = ''.join('%d %d %s\n' % (n, len(E), ' '.join('%d %d %d' % e for e in E)) for E in gs)
    out = subprocess.run([os.path.join(HERE, 'src', 'cotrans')], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()
    c = collections.Counter(); types = collections.Counter()
    for E, line in zip(gs, out):
        tok = line.split(); t = int(tok[0].split('=')[1]); ncv = int(tok[1].split('=')[1])
        cv = set(map(int, tok[2:2+ncv])); rest = tok[2+ncv:]; k = int(rest[0].split('=')[1]); nums = list(map(int, rest[1:]))
        NP = {frozenset((nums[2*i], nums[2*i+1])) for i in range(k)}
        assert t == t0
        deg = collections.Counter(v for e in E for v in e)
        inedge = {frozenset(p) for e in E for p in itertools.combinations(e, 2)}
        D = max(deg.values())
        for v in range(n):
            if s < 3 + 2*deg[v]:
                c['vpred'] += 1
                if v in cv: c['vfail'] += 1
        for x, y in itertools.combinations(range(n), 2):
            pr = frozenset((x, y)); dxy = deg[x] + deg[y] - (1 if pr in inedge else 0)
            if s < 2*dxy - 5:
                c['ppred'] += 1
                if pr in NP: c['pfail'] += 1
            if pr in NP:
                types[(min(deg[x], deg[y]), max(deg[x], deg[y]), 1 if pr in inedge else 0)] += 1
                if 2*dxy > s + 5: c['pairlemma_fail'] += 1
                c['np_D%d' % D] += 1
        c['classes'] += 1
        if NP: c['classes_with_np_D%d' % D] += 1
    tot.update(c)
    print(cell, rel.split('/')[-1], dict(c), dict(types), flush=True)
print('TOTAL', dict(tot))
