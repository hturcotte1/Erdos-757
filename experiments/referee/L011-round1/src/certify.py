"""Referee L011: re-check, from the definitions, the per-graph verdicts of bin/rfilt (verbose output 'R:' lines).
For every graph: F7 certificate (7 distinct points p0..p6 with {p0p1p2, p0p3p4, p0p5p6, p1p3p5, p2p4p6} all edges) or
P3 certificate (a point set S, |S|>=2, containing >= |S|-1 edges); linearity recomputed; connectivity recomputed by BFS on
all N points.  Claims checked: MODE 'notinC' (every graph has a valid F7 or P3 certificate, or is non-linear) or
MODE 'disc' (every graph either has a valid certificate of non-membership in C, or is disconnected on N points).
Also brute-force tau >= TH (all (TH-1)-subsets of points) on a seeded sample of K graphs.
Usage: certify.py RFILT_VERBOSE_FILE N MODE TH K"""
import sys, re, itertools, random
f, N, mode, TH, K = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
lines = [l for l in open(f) if l.startswith('R:')]
ok = bad = 0; kinds = {'F7': 0, 'P3': 0, 'disc': 0, 'nonlinear': 0}
def comps(E):
    adj = {v: set() for v in range(N)}
    for e in E:
        for a in e: adj[a] |= set(e)
    seen = set(); k = 0
    for s in range(N):
        if s in seen: continue
        k += 1; st = [s]; seen.add(s)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
    return k
graphs = []
for l in lines:
    E = [tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l.split('|')[-1])]
    Es = set(E); graphs.append(E)
    lin = all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2))
    cert = None
    m = re.search(r'F7img=([\d,]+)', l)
    if m:
        p = list(map(int, m.group(1).split(',')))
        want = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
        if len(set(p)) == 7 and all(tuple(sorted(p[i] for i in w)) in Es for w in want): cert = 'F7'
    m = re.search(r'P3S=([\d,]+)', l)
    if m and cert is None:
        S = set(map(int, m.group(1).split(',')))
        if len(S) >= 2 and sum(1 for e in E if set(e) <= S) >= len(S) - 1: cert = 'P3'
    if not lin and cert is None: cert = 'nonlinear'
    if cert is None and mode == 'disc' and comps(E) > 1: cert = 'disc'
    if cert is None: bad += 1
    else: ok += 1; kinds[cert] += 1
random.seed(2026); smp = random.sample(graphs, min(K, len(graphs))); tauok = 0
for E in smp:
    pts = sorted({v for e in E for v in e})
    if all(any(not (set(e) & set(T)) for e in E) for T in itertools.combinations(range(N), TH - 1)): tauok += 1
print('%s: graphs %d, certified %d (%s), UNCERTIFIED %d; brute-force tau>=%d on sample %d/%d' % (f.split('/')[-1], len(lines), ok, kinds, bad, TH, tauok, len(smp)))
