# random gluings (amalgams) of tight pieces / records / census classes: identify 1-3 vertices per added copy.
import sys, json, random, collections, gzip
from common import *
seed = int(sys.argv[1]); total = int(sys.argv[2]); outprefix = sys.argv[3]
random.seed(seed)
P, cls = load_pieces()
tight = json.load(open('pieces.json'))
tight = [(d['n'], [tuple(e) for e in d['edges']]) for d in tight]
others = [P[k] for k in ['Abase', 'rec12', 'rec12b', 'rec12c', 'rec11', 'rec10', 'rec8', 'S0', 'S1']] + cls[:]
def pick():
    r = random.random()
    if r < 0.55: return random.choice(tight)
    if r < 0.8: return P['Abase']
    return random.choice(others)
def glue(pieces):
    n, edges = pieces[0]; edges = list(edges); idents = []
    for (pn, pe) in pieces[1:]:
        j = random.choices([1, 2, 3], [0.55, 0.35, 0.10])[0]
        j = min(j, pn, n)
        old = random.sample(range(n), j); new = random.sample(range(pn), j)
        mp = {}
        for a, b in zip(new, old): mp[a] = b
        nxt = n
        for v in range(pn):
            if v not in mp: mp[v] = nxt; nxt += 1
        edges += [tuple(mp[v] for v in e) for e in pe]
        n = nxt; idents.append(j)
    return n, edges, idents
stat = collections.defaultdict(lambda: [0, 0, 10**9, 0])  # n -> [generated, inC, minslack, ...]
low = []
best = collections.defaultdict(list)
hist = collections.defaultdict(collections.Counter)
done = 0
while done < total:
    batch = []; meta = []
    for _ in range(20000):
        k = random.choices([2, 3, 4], [0.5, 0.35, 0.15])[0]
        pcs = [pick() for _ in range(k)]
        n, e, idn = glue(pcs)
        if n > 56 or n < 20: continue
        batch.append(line(n, e)); meta.append((n, e, idn))
    res = run_eval(batch); done += len(batch)
    for (n, e, idn), r in zip(meta, res):
        if r is None: continue
        s = stat[n]; s[0] += 1
        if r[4] != 0: continue
        s[1] += 1; hist[n][r[3]] += 1
        if r[3] < s[2]: s[2] = r[3]
        if r[6] == 1 and r[7] == 0 and r[3] <= 12:
            L = best[n]; L.append((r[3], r[1], r[2], e, idn))
            if len(L) > 400: L.sort(key=lambda x: x[0]); del L[60:]
        if r[3] <= 1 and r[6] == 1: low.append(dict(n=r[0], m=r[1], tau=r[2], slack=r[3], idents=idn, edges=e))
out = {str(n): dict(generated=s[0], inC=s[1], minslack=s[2], hist=dict(sorted(hist[n].items())[:12])) for n, s in sorted(stat.items())}
for n in best: best[n].sort(key=lambda x: x[0]); best[n] = [dict(slack=a, m=b, tau=c, edges=d, idents=f) for a, b, c, d, f in best[n][:60]]
json.dump(dict(seed=seed, best={str(k): v for k, v in best.items()}, total=done, per_n=out, low=low[:2000], n_low=len(low)), open(outprefix + '.json', 'w'))
print(json.dumps({k: (v['generated'], v['inC'], v['minslack']) for k, v in out.items()}))
print('low (slack<=1 connected):', len(low), collections.Counter((d['n'], d['m'], d['tau'], d['slack']) for d in low).most_common(10))
