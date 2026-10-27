# targeted tight gluing with EXACT hub enumeration: parents = disjoint unions of 2-3 connected tight pieces (all connected slack<=1 graphs found so far,
# up to 3 classes per (n,m,slack)), total slack <= 3, n <= 39; vext enumerates every vertex of degree <= 4 joining them with tau(G+v) = tau(G)+1.
import gzip, json, itertools, collections, subprocess, os, sys, random, time
from common import *
random.seed(int(sys.argv[1])); LIM = float(sys.argv[2])
low = [json.loads(l) for l in gzip.open('low_graphs.jsonl.gz', 'rt')]
pcs = {}
byc = collections.defaultdict(list)
for d in low:
    if d['connected'] and d['n'] >= 15: byc[(d['n'], d['m'], d['slack'])].append(d)
P = [(3, [(0, 1, 2)], 0)]
sm = json.load(open('pieces.json'))
seen = set()
for d in sm:
    k = (d['n'], d['m'], d['slack'])
    if len([1 for p in P if (p[0], len(p[1]), p[2]) == k]) < 3: P.append((d['n'], [tuple(e) for e in d['edges']], d['slack']))
for k, L in byc.items():
    random.shuffle(L)
    for d in L[:3]: P.append((d['n'], [tuple(e) for e in d['edges']], d['slack']))
print('pieces', len(P), collections.Counter((p[0], len(p[1]), p[2]) for p in P), flush=True)
def disj(a, b): return (a[0] + b[0], a[1] + [tuple(v + a[0] for v in e) for e in b[1]])
parents = []
for k in (2, 3):
    for combo in itertools.combinations_with_replacement(range(len(P)), k):
        n = sum(P[i][0] for i in combo); s = sum(P[i][2] for i in combo)
        if n <= 39 and s <= 3:
            cur = (0, [])
            for i in combo: cur = disj(cur, (P[i][0], P[i][1]))
            parents.append((n, cur[1], s, combo))
random.shuffle(parents)
print('parents', len(parents), flush=True)
env = dict(os.environ, I11_DM='5', I11_MAXD='4', I11_SEED='3')
t0 = time.time(); kids = collections.Counter(); minconn = {}; nlow = 0
lowf = open('out/beam_hubunion_low.txt', 'w'); seenfp = set()
for ci in range(0, len(parents), 20):
    if time.time() - t0 > LIM: break
    chunk = parents[ci:ci + 20]
    inp = "\n".join(line(n, e) for n, e, s, c in chunk) + "\n"
    try:
        r = subprocess.run([os.path.join(HERE, 'vext'), '400', '2'], input=inp, capture_output=True, text=True, env=env, timeout=40); out = r.stdout
    except subprocess.TimeoutExpired as ex:
        out = ex.stdout.decode() if isinstance(ex.stdout, bytes) else (ex.stdout or '')
    for l in out.split("\n"):
        t = l.split(' ', 5)
        try:
            s, n, m, tau = int(t[0]), int(t[1]), int(t[2]), int(t[3]); gl = t[5]; gt = gl.split(' '); assert int(gt[1]) == len(gt) - 2
        except Exception: continue
        # connectivity
        es = [tuple(int(x) for x in w.split(',')) for w in gt[2:]]; par = list(range(n))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for e in es:
            for v in e[1:]: par[f(v)] = f(e[0])
        conn = len(set(f(v) for v in range(n))) == 1 and len(set(v for e in es for v in e)) == n
        kids[(n, conn)] += 1
        if conn:
            if n not in minconn or s < minconn[n]: minconn[n] = s
            if s < 0: print('!!! NEGATIVE SLACK', l, flush=True); lowf.write('NEG ' + l + '\n')
            if s <= 1 and t[4] not in seenfp: seenfp.add(t[4]); lowf.write(l + '\n'); lowf.flush(); nlow += 1
print(json.dumps(dict(parents_done=min(len(parents), ci + 20), seconds=time.time() - t0, children_connected={n: c for (n, cn), c in sorted(kids.items()) if cn}, min_connected_slack=dict(sorted(minconn.items())), n_slack_le1_connected=nlow)), flush=True)
json.dump(dict(min_connected_slack=minconn, children={str(k): v for k, v in kids.items()}), open('out/hubunion.json', 'w'))
