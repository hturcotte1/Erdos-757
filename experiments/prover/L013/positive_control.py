"""(L013, prover) Positive control for completeness of recursion cells: random members of C generated independently of the engine
(random greedy linear 3-graphs with n vertices, m edges and maximum degree <= D; kept iff connected, in C and tau == t, all tested by the
pure-Python verifier of check_cells.py) must each be isomorphic to a representative of the engine's cell list (nauty canonical form via
bin/canon, compared with the cell file, whose FOUND lines are canonical forms).
Usage: python3 positive_control.py CELLDIR n m t D WANTED MAXTRIES SEED   -> one JSON line (appended to positive_control.jsonl)"""
import sys, os, random, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from check_cells import verify, parse_edges
cd = sys.argv[1]; n, m, t, D = map(int, sys.argv[2:6]); want, maxtries, seed = map(int, sys.argv[6:9])
rng = random.Random(seed)
reps = set(tuple(parse_edges(l)) for l in open(os.path.join(cd, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))) if l.startswith('FOUND:'))
def rand_graph():
    """random connected growth: the first edge on 3 new vertices, every later edge has k in {0,1,2} new vertices (k chosen uniformly
    among the values that still allow exactly n vertices at the end) and 3-k old vertices of degree < D; pairs must be new (linear)."""
    deg = [0] * n; used = set(); E = []; nv = 0
    for i in range(m):
        r = m - i; q = n - nv
        ks = [k for k in (0, 1, 2, 3) if k <= q and q - k <= 2 * (r - 1) and (k == 3) == (i == 0) and 3 - k <= nv]
        if not ks: return None
        k = rng.choice(ks); ok = False
        for _ in range(200):
            olds = [v for v in range(nv) if deg[v] < D]
            if len(olds) < 3 - k: return None
            e = tuple(sorted(rng.sample(olds, 3 - k) + list(range(nv, nv + k))))
            ps = [frozenset((e[0], e[1])), frozenset((e[0], e[2])), frozenset((e[1], e[2]))]
            if any(p in used for p in ps): continue
            ok = True; break
        if not ok: return None
        E.append(e); used.update(ps); nv += k
        for v in e: deg[v] += 1
    perm = list(range(n)); rng.shuffle(perm)
    return [tuple(sorted(perm[v] for v in e)) for e in E] if nv == n else None
t0 = time.time(); found = []; tries = 0; reasons = {}
while len(found) < want and tries < maxtries:
    tries += 1; E = rand_graph()
    if E is None: reasons['incomplete'] = reasons.get('incomplete', 0) + 1; continue
    r = verify(E, n, m, t, D)
    if r: reasons[r] = reasons.get(r, 0) + 1; continue
    found.append(E)
lines = ['%d ' % m + ' '.join('%d %d %d' % e for e in E) for E in found]
out = subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines() if lines else []
canon = [tuple(tuple(map(int, p.split('.'))) for p in l.split()[2:]) for l in out]
hit = sum(1 for c in canon if c in reps)
rec = dict(cell=[n, m, t, D], cell_classes=len(reps), tries=tries, members_generated=len(found), distinct_classes_generated=len(set(canon)),
           found_in_cell=hit, missing=len(found) - hit, rejected=reasons, seed=seed, secs=round(time.time() - t0, 1))
print(json.dumps(rec)); open(os.path.join(HERE, 'positive_control.jsonl'), 'a').write(json.dumps(rec) + '\n')
