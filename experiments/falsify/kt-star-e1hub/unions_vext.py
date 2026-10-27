#!/usr/bin/env python3
"""Second pass, structured generator: parents = disjoint unions of <=3 components from POOL (the 32 L* pieces and all stored connected
Delta<=3 classes with n<=14 and A<=30), total A <= AUNION (default 0); children = EVERY one-vertex extension (new vertex v with 1..3 edges, Delta<=3)
that raises tau by 1 (exact operator `vext` of experiments/falsify/i11-n28-40; children are in C).  A(child) = A(parent) + 35 d - 105.
Level 2 repeats from connected children with A<0 and n<=NMAX.  Every connected child with n>=NREP and A<0 is evaluated exactly: P = A + DEF (kt.deficiency).
usage: unions_vext.py tag NMAX AUNION NREP [maxparents]"""
import sys, os, json, glob, re, itertools, subprocess, time, random, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kt, hubs, pyverify
VEXT = '/home/user/Erdos-757/experiments/falsify/i11-n28-40/vext'
tag = sys.argv[1]; NMAX = int(sys.argv[2]); AUNION = int(sys.argv[3]); NREP = int(sys.argv[4]); MAXPAR = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
random.seed(5)
def A_of(n, m, t): return 27 * n + 35 * m - 132 * t
def line(n, E): return "%d %d %s" % (n, len(E), " ".join("%d,%d,%d" % tuple(e) for e in E))
comps = []   # (n, edges, tau, name)
for P in hubs.PIECES: comps.append((P.n, [tuple(e) for e in P.edges], P.tau, P.name))
seen = set()
for f in sorted(glob.glob('/home/user/Erdos-757/experiments/prover/L017/out/L01[2-6]/cells*/cell_*_D3.txt')):
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D3\.txt', os.path.basename(f)); n, m, t = map(int, mm.groups())
    if (n, m, t) in seen or n > 14 or A_of(n, m, t) > 30 or A_of(n, m, t) < 0: continue
    seen.add((n, m, t))
    for i, g in enumerate(kt.read_cell(f)):
        if max(hubs.degs(n, g)) <= 3: comps.append((n, [tuple(e) for e in g], t, '(%d,%d,%d)#%d' % (n, m, t, i)))
print('pool', len(comps), flush=True)
Ac = [A_of(c[0], len(c[1]), c[2]) for c in comps]
parents = []
idx = sorted(range(len(comps)), key=lambda i: Ac[i])
def union(ids):
    n = 0; E = []; t = 0
    for i in ids:
        c = comps[i]; E += [tuple(v + n for v in e) for e in c[1]]; n += c[0]; t += c[2]
    return n, E, t
for r in (1, 2, 3):
    for ids in itertools.combinations_with_replacement(range(len(comps)), r):
        if sum(Ac[i] for i in ids) > AUNION: continue
        n = sum(comps[i][0] for i in ids)
        if n + 1 > NMAX or n + 1 < NREP: continue
        parents.append(ids)
print('parents', len(parents), flush=True)
if len(parents) > MAXPAR: random.shuffle(parents); parents = parents[:MAXPAR]
env = dict(os.environ, I11_DM='3', I11_SEED='1', I11_MAXD='3')
def conn(n, E):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in E:
        for v in e[1:]: par[f(v)] = f(e[0])
    return len(set(f(v) for v in range(n))) == 1
def run_vext(plist):
    kids = {}
    for ci in range(0, len(plist), 40):
        inp = "\n".join(line(n, E) for (n, E, t) in plist[ci:ci + 40]) + "\n"
        try: txt = subprocess.run([VEXT, '2000', '5'], input=inp, capture_output=True, text=True, env=env, timeout=300).stdout
        except subprocess.TimeoutExpired as ex: txt = (ex.stdout.decode() if isinstance(ex.stdout, bytes) else (ex.stdout or ''))
        for l in txt.split("\n"):
            if not l: continue
            try:
                s, nn, m, tau, fp, gl = l.split(' ', 5); nn = int(nn); m = int(m); tau = int(tau)
                tk = gl.split(); assert int(tk[1]) == m
                E = [tuple(int(x) for x in w.split(',')) for w in tk[2:]]
            except Exception: continue
            kids[fp] = (nn, E, tau)
    return kids
reg = hubs.Registry(); out = open('uv_%s.jsonl' % tag, 'a')
stats = collections.Counter(); minP = None; t0 = time.time()
def evaluate(kids, level):
    global minP
    cur = []
    for fp, (nn, E, tau) in kids.items():
        A = A_of(nn, len(E), tau); stats['kids_L%d' % level] += 1
        if A >= 0: continue
        if not conn(nn, E): stats['disconnected'] += 1; continue
        stats['conn_A<0_L%d' % level] += 1
        cur.append((nn, E, tau))
        if nn < NREP: continue
        rec, new = reg.lookup(nn, E)
        if not new: continue
        stats['classes_n>=%d' % NREP] += 1
        r = hubs.analyse_H(nn, E, tau)
        if not r['inC']: stats['notinC'] += 1; continue
        stats['evaluated'] += 1
        if minP is None or r['P'] < minP: minP = r['P']
        out.write(json.dumps(dict(type='UV', level=level, **{k: r[k] for k in ('n', 'm', 'tau', 'A', 'DEF', 'DEFp', 'P', 'Pp', 'piece')}, H=E)) + '\n'); out.flush()
        if r['P'] < 0 or (r['piece'] is None and r['Pp'] < 0):
            stats['HITS'] += 1; print('HIT', r, E, flush=True)
    return cur
kids = run_vext([union(ids) for ids in parents])
print('level1 kids', len(kids), '[%.0fs]' % (time.time() - t0), flush=True)
cur = evaluate(kids, 1)
print(dict(stats), 'minP', minP, '[%.0fs]' % (time.time() - t0), flush=True)
cur = [c for c in cur if c[0] + 1 <= NMAX and c[0] + 1 >= NREP]
random.shuffle(cur); cur = cur[:int(os.environ.get('L2MAX', 3000))]
kids2 = run_vext(cur)
print('level2 kids', len(kids2), '[%.0fs]' % (time.time() - t0), flush=True)
cur2 = evaluate(kids2, 2)
print('FINAL', dict(stats), 'minP', minP, '[%.0fs]' % (time.time() - t0), flush=True)
json.dump(dict(stats=dict(stats), minP=minP, pool=len(comps), parents=len(parents)), open('uv_%s.stats.json' % tag, 'w'))
