# beam search over vertex extensions that raise tau: pool[n] = lowest-slack graphs on n vertices (any connectivity), degree cap DM.
import sys, json, random, subprocess, collections, itertools, time, os, gzip
from common import *
DM = int(sys.argv[1]); W = int(sys.argv[2]); NMAX = int(sys.argv[3]); seed = int(sys.argv[4]); tag = sys.argv[5]
random.seed(seed)
env = dict(os.environ, I11_DM=str(DM), I11_SEED=str(seed), I11_MAXD=os.environ.get('MAXD', '4'))
tight = json.load(open('pieces.json'))
pieces = [(d['n'], [tuple(e) for e in d['edges']], d['slack']) for d in tight]
if DM <= 3: pieces = [p for p in pieces if max(sum(v in e for e in p[1]) for v in range(p[0])) <= 3]
if os.environ.get('EXTRA'):
    seen_fp = set()
    for l in open(os.environ['EXTRA']):
        t = l.strip().split(' ')
        if len(t) < 7 or t[0] not in ('0', '1') or t[4] in seen_fp: continue
        seen_fp.add(t[4]); nn = int(t[5]); pieces.append((nn, [tuple(int(x) for x in w.split(',')) for w in t[7:]], int(t[0])))
    print('extra pieces', len(seen_fp), flush=True)
AP = (3, [(0, 1, 2)], 0)
def disj(a, b):
    return (a[0] + b[0], a[1] + [tuple(v + a[0] for v in e) for e in b[1]])
def is_conn(gl):
    t = gl.split(' ', 2); n = int(t[0]); es = [tuple(int(x) for x in w.split(',')) for w in t[2].split()]
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)] = f(e[0])
    used = set(v for e in es for v in e)
    return len(used) == n and len(set(f(v) for v in range(n))) == 1
pool = collections.defaultdict(dict)   # n -> fp -> (slack, m, tau, edges-line)
def parse_child(l):
    t = l.split(' ', 5); return int(t[0]), int(t[1]), int(t[2]), int(t[3]), t[4], t[5].strip()
# seeds: multiset unions of tight pieces (n<=NMAX-1, <=MAXC components, total slack<=SMAX)
MAXC = int(os.environ.get('MAXC', 5)); SMAX = int(os.environ.get('SMAX', 3))
useA = int(os.environ.get('USEA', 1))
plist = [(p[0], p[1], p[2]) for p in pieces if (useA or p[0] != 14)]
# dedupe pieces by (n,m,slack,sorted degree seq) to keep a few per type
seen_t = {}; pl2 = [(3, [(0, 1, 2)], 0)]
for p in plist:
    key = (p[0], len(p[1]), p[2], tuple(sorted(sum(v in e for e in p[1]) for v in range(p[0]))))
    if key not in seen_t: seen_t[key] = 1; pl2.append(p)
plist = pl2; print("pieces", [(p[0], len(p[1]), p[2]) for p in plist], flush=True)
seeds = []
def rec(idx, cn, ce, cs, cc):
    if cc > 0 and cn >= 6: seeds.append((cn, ce, cs))
    if cc >= MAXC: return
    for k in range(idx, len(plist)):
        p = plist[k]
        if cn + p[0] <= NMAX - 1 and cs + p[2] <= SMAX:
            n2, e2 = disj((cn, ce), (p[0], p[1])); rec(k, n2, e2, cs + p[2], cc + 1)
rec(0, 0, [], 0, 0)
print("seeds", len(seeds), flush=True)
lines = [line(n, e) for n, e, s in seeds]
res = run_eval(lines)
for (n, e, s), r in zip(seeds, res):
    if r and r[4] == 0: pool[n]["seed%d" % len(pool[n])] = (r[3], r[1], r[2], line(n, e))
# extra seeds: gluing results (connected, slack<=12), if available
for gf in ['out/glue_main.json', 'out/glue_test2.json']:
    if os.path.exists(gf):
        gd = json.load(open(gf))
        for nk, lst in gd['best'].items():
            for d in lst:
                if int(nk) <= NMAX and max(sum(v in e for e in d['edges']) for v in range(int(nk))) <= DM:
                    pool[int(nk)]['g%d' % len(pool[int(nk)])] = (d['slack'], d['m'], d['tau'], line(int(nk), [tuple(e) for e in d['edges']]))
        break
stats = {}
best_by_n = {}
t0 = time.time()
lowfile = open('out/beam_%s_low.txt' % tag, 'w')
for n in range(3, NMAX):
    P = list(pool[n].values())
    if not P: continue
    cP = [p for p in P if is_conn(p[3])]; dP = [p for p in P if not is_conn(p[3])]
    c7 = [p for p in cP if p[0] <= 7]; random.shuffle(c7); c7.sort(key=lambda p: p[0] + 3 * random.random())
    dP2 = [p for p in dP if p[0] <= 1]; random.shuffle(dP2)
    Wl = W if n < 23 else int(os.environ.get('W2', 250)); P = c7[:Wl] + dP2[:Wl // 4]
    inp = "\n".join(p[3] for p in P) + "\n"
    try:
        r = subprocess.run([os.path.join(HERE, 'vext'), '400', '2'], input=inp, capture_output=True, text=True, env=env, timeout=int(os.environ.get('VT', 150)))
        out_txt = r.stdout
    except subprocess.TimeoutExpired as ex:
        out_txt = ex.stdout.decode() if isinstance(ex.stdout, bytes) else (ex.stdout or '')
        print('  vext timeout at level', n, flush=True)
    kids = 0; mn = 10**9
    for l in out_txt.split("\n"):
        if not l: continue
        try:
            s, nn, m, tau, fp, gl = parse_child(l)
            gt = gl.split(' '); assert int(gt[1]) == len(gt) - 2 and nn <= 41
        except Exception:
            continue
        kids += 1
        if fp not in pool[nn]: pool[nn][fp] = (s, m, tau, gl)
        if s < mn: mn = s
        if s < 0: print("!!! NEGATIVE SLACK", l, flush=True); lowfile.write("NEG " + l + "\n")
        if s <= 1 and nn >= 15 and is_conn(gl): lowfile.write(l + "\n")
    ps = sorted(v[0] for v in pool[n + 1].values() if is_conn(v[3]))
    stats[n + 1] = dict(pool=len(pool[n + 1]), minslack=ps[0] if ps else None, hist=dict(collections.Counter(ps).most_common(8)))
    lowfile.flush(); json.dump(stats, open('out/beam_%s_stats.json' % tag, 'w'))
    print(n, "parents", len(P), "kids", kids, "-> n+1", stats[n + 1], "t=%.0fs" % (time.time() - t0), flush=True)
    # keep only the best W*3 to bound memory
    if len(pool[n + 1]) > 20 * W:
        items = sorted(pool[n + 1].items(), key=lambda kv: kv[1][0] + random.random()); pool[n + 1] = dict(items[:20 * W])
json.dump(stats, open('out/beam_%s_stats.json' % tag, 'w'))
# dump final low pools
with gzip.open('out/beam_%s_pools.jsonl.gz' % tag, 'wt') as f:
    for n in sorted(pool):
        for fp, v in sorted(pool[n].items(), key=lambda kv: kv[1][0])[:300]:
            f.write(json.dumps(dict(n=n, slack=v[0], m=v[1], tau=v[2], line=v[3])) + "\n")
