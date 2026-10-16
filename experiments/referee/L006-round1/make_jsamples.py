"""Generate sample two-point extensions B of census classes (types T0, T1a, T1b, T2-generic) with own code; write claim files
for the frozen verifier. Every B is checked (4,5) here; h is left to the verifier (claimed_h = 9)."""
import gzip, json, itertools, random, os
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'
OUT = '/home/user/Erdos-757/experiments/referee/L006-round1/jsamples'
def nd(Q): return len({abs(u - v) for u, v in itertools.combinations(Q, 2)})
def is45(S): return all(nd(Q) >= 5 for Q in itertools.combinations(S, 4))
def partners(P):
    out = set()
    for u, v in itertools.permutations(P, 2):
        if (u + v) % 2 == 0: out.add((u + v) // 2)
        out.add(2 * u - v)
    return out - set(P)
cen = json.load(gzip.open(CENSUS, 'rt'))
rng = random.Random(6)
made = []
for c in (20392, 23942, 18917, 12070):
    A = sorted(4 * a for a in cen[c]['set'])
    Px = sorted(partners(A))
    singles = [x for x in Px if is45(A + [x])]
    def far():
        return rng.randrange(10**6, 10**7) * 4 + 1
    samples = {}
    while 'T0' not in samples:
        x, y = far(), far()
        if x != y and is45(A + [x, y]): samples['T0'] = (x, y)
    for x in singles:
        y = far()
        if is45(A + [x, y]): samples['T1a'] = (x, y); break
    for x in rng.sample(singles, len(singles)):
        Y = sorted(partners(A + [x])); rng.shuffle(Y)
        hit = next(((x, y) for y in Y if is45(A + [x, y])), None)
        if hit: samples['T1b'] = hit; break
    while 'T2' not in samples:
        a = rng.choice(A); x = far(); y = 2 * x - a
        if is45(A + [x, y]) and x not in Px and y not in Px: samples['T2'] = (x, y)
    for typ, (x, y) in samples.items():
        B = sorted(A + [x, y]); assert len(set(B)) == 14
        cid = f'R-L006-c{c}-{typ}'
        json.dump({'id': cid, 'type': 'construction', 'set': B, 'claimed_h': 9,
                   'notes': f'referee L006 sample: class {c} (x4 coords), type {typ}, x={x}, y={y}'}, open(os.path.join(OUT, cid + '.json'), 'w'))
        made.append(cid)
print(len(made), made)
