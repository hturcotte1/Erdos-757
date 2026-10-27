# Can random saturated C-graphs (m=n-2, from random growth) be realised exactly as (4,5)-sets?  Random midpoint assignment + exact solve + check_values.
import sys, random, subprocess, json, os
from fractions import Fraction
from common import *
from e757.saturated import solve_midpoint_map, check_values
random.seed(1)
def assign(n, es, rng):
    # random SDR avoiding a random pair (lo,hi): randomised augmenting path matching edges->vertices
    for _ in range(30):
        lo, hi = rng.sample(range(n), 2)
        owner = {}
        def aug(i, seen):
            vs = list(es[i]); rng.shuffle(vs)
            for v in vs:
                if v in (lo, hi) or v in seen: continue
                seen.add(v)
                if v not in owner or aug(owner[v], seen): owner[v] = i; return True
            return False
        order = list(range(len(es))); rng.shuffle(order)
        if all(aug(i, set()) for i in order):
            mid = {}
            for v, i in owner.items():
                a, b = [u for u in es[i] if u != v]; mid[v] = (a, b)
            if len(mid) == n - 2: return lo, hi, mid
    return None
rng = random.Random(5); out = {}
for n in (10, 12, 14, 16, 20):
    f = 'out/dump_%d.txt' % n
    env = dict(os.environ, I11_DUMP=f, I11_CONN='0', I11_DMAX='5', I11_OUT='/dev/null')
    subprocess.run([os.path.join(HERE, 'i11_new'), 'grow', str(n), str(n - 2), str(n - 2), '60000', str(n), '1'], capture_output=True, env=env)
    tried = ok = 0; classes = 0
    for l in open(f):
        t = l.split(); nn = int(t[0]); es = [tuple(int(x) for x in w.split(',')) for w in t[2:]]
        a = assign(nn, es, rng)
        if not a: continue
        lo, hi, mid = a; tried += 1
        vals = solve_midpoint_map(nn, lo, hi, mid)
        if vals is None: continue
        good, why = check_values(vals, [(i, j, k) for j, (i, k) in mid.items()])
        ok += good
    out[n] = dict(graphs=sum(1 for _ in open(f)), tried=tried, realized=ok)
    print(n, out[n], flush=True)
json.dump(out, open('out/realize_rand.json', 'w'))
