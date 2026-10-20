# Referee round 2: brute-force validation of xr (all d-sets of disjoint admissible pairs; tau by exhaustive subset search).
import itertools, subprocess, sys, random, tarfile, re
def tau(nv, E):
    for k in range(0, nv + 1):
        for S in itertools.combinations(range(nv), k):
            s = set(S)
            if all(s & set(e) for e in E): return k
def bf(NG, E, d, EP, T):
    deg = [0] * NG
    for e in E:
        for v in e: deg[v] += 1
    pairs = [(a, b) for a in range(NG) for b in range(a + 1, NG) if deg[a] <= EP and deg[b] <= EP and not any(a in e and b in e for e in E)]
    res = set()
    for ps in itertools.combinations(pairs, d):
        vs = [v for p in ps for v in p]
        if len(set(vs)) != 2 * d: continue
        H = list(E) + [(a, b, NG) for (a, b) in ps]
        if tau(NG + 1, H) >= T: res.add(tuple(sorted(ps)))
    return res
def xr(NG, E, d, EP, T):
    line = '%d ' % len(E) + ' '.join('%d %d %d' % e for e in E) + '\n'
    out = subprocess.run(['./out/xr', str(NG), str(d), str(EP), str(T)], input=line, capture_output=True, text=True).stdout
    res = []
    for l in out.splitlines():
        if l.startswith('HIT:'):
            es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
            new = [e for e in es if e[2] == NG]; res.append(tuple(sorted((a, b) for a, b, _ in new)))
    return res
tf = tarfile.open('/home/user/Erdos-757/experiments/prover/L012/cells.tar.gz')
def cellreps(name):
    return [[tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
            for l in tf.extractfile('cells/' + name).read().decode().splitlines() if l.startswith('FOUND')]
random.seed(7)
cases = []
c853 = cellreps('cell_8_5_3_D3.txt'); c1074 = cellreps('cell_10_7_4_D3.txt'); c632 = cellreps('cell_6_3_2_D3.txt') if 'cells/cell_6_3_2_D3.txt' in tf.getnames() else []
AP = [(0, 1, 2)]
def shift(E, o): return [tuple(v + o for v in e) for e in E]
for E in c853: cases.append((8, E, 4, 3, 4)); cases.append((8, E, 3, 2, 4)); cases.append((8, E, 2, 2, 4)); cases.append((8, E, 3, 3, 3))
for E in c1074[:2]: cases.append((10, E, 3, 2, 5)); cases.append((10, E, 2, 1, 5)); cases.append((10, E, 2, 2, 4))
# with an isolated vertex and an AP component
for E in c853[:2]:
    cases.append((9, E, 3, 2, 4)); cases.append((9, E, 4, 3, 4))                     # vertex 8 isolated
    cases.append((11, E + shift(AP, 8), 3, 2, 5)); cases.append((11, E + shift(AP, 8), 4, 3, 5))
bad = 0; tot = 0
for (NG, E, d, EP, T) in cases:
    a = bf(NG, E, d, EP, T); b = xr(NG, E, d, EP, T)
    tot += len(a)
    ok = (len(b) == len(set(b))) and set(b) == a
    if not ok: bad += 1; print('MISMATCH', NG, d, EP, T, len(a), len(b), len(set(b)))
print('cases %d, brute-force hits %d, mismatches %d' % (len(cases), tot, bad))
