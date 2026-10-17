"""(L014) Soundness audit (not load-bearing for an empty list): python3 audit_sample.py CELLDIR K SEED
For every complete cell file, all representatives if the cell has <= K classes, else K random ones (random.Random(SEED)), are
re-verified from the definitions by pyverify (written from scratch): labels 0..n-1, m distinct triples, linear, F7-free, (P3),
connected on n vertices, tau = t exactly, max degree <= D.  Prints problems and a summary."""
import sys, os, re, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyverify as pv
d, K, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); R = random.Random(seed)
tot = 0; prob = 0; cells = 0
for fn in sorted(os.listdir(d)):
    if not re.match(r'cell_\d+_\d+_\d+_D\d+\.txt$', fn): continue
    n, m, t, D = (int(x) for x in re.findall(r'\d+', fn)); reps = []; done = False
    for l in open(os.path.join(d, fn)):
        if l.startswith('FOUND:'): reps.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
        elif l.startswith('INFO '): done = True
    if not done: continue
    cells += 1; S = reps if len(reps) <= K else R.sample(reps, K)
    for E in S:
        tot += 1; why = None
        if len(E) != m or len(set(frozenset(e) for e in E)) != m: why = 'edge count'
        elif any(not (0 <= v < n) for e in E for v in e): why = 'labels'
        elif not pv.linear(E): why = 'nonlinear'
        elif pv.has_f7(E): why = 'F7'
        elif not pv.p3(E, range(n)): why = 'P3'
        elif not pv.connected(E, range(n)): why = 'disconnected'
        elif pv.maxdeg(E) > D: why = 'degree'
        elif pv.cover_le(E, t - 1) or not pv.cover_le(E, t): why = 'tau'
        if why: prob += 1; print('PROBLEM', fn, why, E)
    print('%s: %d classes, %d verified' % (fn, len(reps), len(S)), flush=True)
print('SUMMARY cells %d, representatives verified %d, problems %d' % (cells, tot, prob))
