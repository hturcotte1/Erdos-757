#!/usr/bin/env python3
"""A-driven beam search (second pass).  Children are produced by the exact vertex-extension operator `vext` of
experiments/falsify/i11-n28-40 (adds one vertex with <=3 edges so that tau rises by 1; children checked to be in C; Delta<=DM).
Ranking key: A = 27n+35m-132tau (lower is better); pool per n keeps the W lowest-A graphs (connected preferred).
All connected children with n>=25 and A<=AREP are written to OUT for a later exact DEF evaluation.
usage: beamA.py DM W NMAX seed tag"""
import sys, os, json, random, subprocess, time, collections
HERE = '/home/user/Erdos-757/experiments/falsify/i11-n28-40'
DM = int(sys.argv[1]); W = int(sys.argv[2]); NMAX = int(sys.argv[3]); seed = int(sys.argv[4]); tag = sys.argv[5]
AREP = int(os.environ.get('AREP', 10))
random.seed(seed)
env = dict(os.environ, I11_DM=str(DM), I11_SEED=str(seed), I11_MAXD=os.environ.get('MAXD', '3'))
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
pieces = [(p['n'], [tuple(e) for e in p['edges']]) for p in R['pieces']]
def line(n, E): return "%d %d %s" % (n, len(E), " ".join("%d,%d,%d" % tuple(e) for e in E))
def A_of(n, m, t): return 27 * n + 35 * m - 132 * t
def conn(gl):
    t = gl.split(' ', 2); n = int(t[0]); es = [tuple(int(x) for x in w.split(',')) for w in t[2].split()]
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)] = f(e[0])
    return len(set(v for e in es for v in e)) == n and len(set(f(v) for v in range(n))) == 1
pool = collections.defaultdict(dict)
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021'); import kt
PT = [p['tau'] for p in R['pieces']]
def add_seed(n, E, t):
    pool[n]['s%d' % len(pool[n])] = (A_of(n, len(E), t), len(E), t, line(n, E))
for (n, E), t in zip(pieces, PT): add_seed(n, E, t)
# unions of two pieces
for i in range(len(pieces)):
    for j in range(i, len(pieces)):
        n1, E1 = pieces[i]; n2, E2 = pieces[j]
        add_seed(n1 + n2, E1 + [tuple(v + n1 for v in e) for e in E2], PT[i] + PT[j])
out = open('out_beamA_%s.txt' % tag, 'w'); seen_rep = set()
t0 = time.time()
for n in range(3, NMAX):
    P = list(pool[n].values())
    if not P: continue
    cP = [p for p in P if conn(p[3])]; dP = [p for p in P if not conn(p[3])]
    cP.sort(key=lambda p: p[0] + 40 * random.random()); dP.sort(key=lambda p: p[0] + 40 * random.random())
    P = cP[:W] + dP[:W // 3]
    txt = ""
    for ci in range(0, len(P), 20):
        inp = "\n".join(p[3] for p in P[ci:ci + 20]) + "\n"
        try:
            r = subprocess.run([os.path.join(HERE, 'vext'), '600', '3'], input=inp, capture_output=True, text=True, env=env, timeout=120)
            txt += r.stdout
        except subprocess.TimeoutExpired as ex:
            txt += (ex.stdout.decode() if isinstance(ex.stdout, bytes) else (ex.stdout or ''))
    kids = 0; mnA = 10**9
    for l in txt.split("\n"):
        if not l: continue
        try:
            s, nn, m, tau, fp, gl = l.split(' ', 5); nn = int(nn); m = int(m); tau = int(tau); gl = gl.strip()
            assert int(gl.split(' ')[1]) == m
        except Exception: continue
        A = A_of(nn, m, tau); kids += 1
        if fp not in pool[nn]: pool[nn][fp] = (A, m, tau, gl)
        if nn >= 25 and A <= AREP and fp not in seen_rep and conn(gl):
            seen_rep.add(fp); out.write("%d %d %d %d %s\n" % (A, nn, m, tau, gl)); out.flush()
        mnA = min(mnA, A)
    if len(pool[n + 1]) > 30 * W:
        items = sorted(pool[n + 1].items(), key=lambda kv: kv[1][0] + 30 * random.random()); pool[n + 1] = dict(items[:30 * W])
    ca = sorted(v[0] for v in pool[n + 1].values() if conn(v[3]))
    print(n, 'parents', len(P), 'kids', kids, '-> n+1 pool', len(pool[n + 1]), 'minA(conn)', ca[:1], 'hist', dict(collections.Counter(ca).most_common(5)), 'reported', len(seen_rep), '[%.0fs]' % (time.time() - t0), flush=True)
