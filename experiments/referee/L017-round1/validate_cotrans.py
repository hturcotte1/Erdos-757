# Referee L017 round 1: validate src/cotrans against brute force (all subsets) on random linear 3-graphs.
import random, subprocess, itertools, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
def rand_linear(n, m, rng):
    edges = []; pairs = set()
    tries = 0
    while len(edges) < m and tries < 2000:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        ps = {(e[0], e[1]), (e[0], e[2]), (e[1], e[2])}
        if ps & pairs: continue
        pairs |= ps; edges.append(e)
    return edges
def tau_bf(n, edges, removed=()):
    rem = set(removed)
    E = [e for e in edges if not (set(e) & rem)]
    V = [v for v in range(n) if v not in rem]
    if not E: return 0
    for k in range(0, len(V) + 1):
        for T in itertools.combinations(V, k):
            S = set(T)
            if all(S & set(e) for e in E): return k
rng = random.Random(17)
graphs = []
for _ in range(400):
    n = rng.randint(3, 11); m = rng.randint(1, 2 * n)
    edges = rand_linear(n, m, rng)
    graphs.append((n, edges))
inp = ''.join('%d %d %s\n' % (n, len(e), ' '.join('%d %d %d' % t for t in e)) for n, e in graphs)
out = subprocess.run([os.path.join(HERE, 'src', 'cotrans')], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()
bad = 0
for (n, edges), line in zip(graphs, out):
    tok = line.split()
    t = int(tok[0].split('=')[1])
    ncv = int(tok[1].split('=')[1]); cv = set(map(int, tok[2:2 + ncv]))
    rest = tok[2 + ncv:]; npairs = int(rest[0].split('=')[1]); nums = list(map(int, rest[1:]))
    NP = {(nums[2*i], nums[2*i+1]) for i in range(npairs)}
    tb = tau_bf(n, edges)
    if tb != t: bad += 1; print('tau mismatch', n, edges, t, tb); continue
    for v in range(n):
        co = tau_bf(n, edges, (v,)) == t - 1
        if co == (v in cv): bad += 1; print('vertex mismatch', n, edges, v)
    for x in range(n):
        for y in range(x + 1, n):
            co = tau_bf(n, edges, (x, y)) == t - 2
            if co == ((x, y) in NP): bad += 1; print('pair mismatch', n, edges, x, y)
print('graphs', len(graphs), 'mismatches', bad)
