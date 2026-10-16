"""Referee round 3 (L002), check C: collect 12-point candidate sets from sources that were NOT produced by the
n=12 census pipeline (random generators, other sizes, other engines), including every 12-subset of larger sets
whose h could drop to 7.  Writes deduplicated (by affine normal form) lines '12 x1 ... x12' to stdout and a
source tally to stderr.  The (4,5) test and h are computed afterwards by ./vr (own C code)."""
import sys, json, gzip, math
from itertools import combinations
from fractions import Fraction

R = '/home/user/Erdos-757/'
seen = set(); tally = {}


def norm(v):
    v = sorted(v)
    if len(set(v)) != len(v):
        return None
    # rationals -> integers
    if any(isinstance(x, Fraction) for x in v):
        L = 1
        for x in v:
            L = L * Fraction(x).denominator // math.gcd(L, Fraction(x).denominator)
        v = [int(Fraction(x) * L) for x in v]
    v = [x - v[0] for x in v]
    g = 0
    for x in v:
        g = math.gcd(g, x)
    v = [x // g for x in v]
    r = sorted(v[-1] - x for x in v)
    return tuple(min(v, r))


def emit(S, src):
    t = norm(S)
    if t is None or t in seen:
        return
    seen.add(t)
    tally[src] = tally.get(src, 0) + 1
    sys.stdout.write('12 ' + ' '.join(map(str, t)) + ' # ' + src + '\n')


def add(A, src, maxdrop=None):
    A = sorted(set(A))
    if len(A) < 12:
        return
    if len(A) == 12:
        emit(A, src); return
    for S in combinations(A, 12):
        emit(S, src)


def ints(x):
    return [Fraction(s) if isinstance(s, str) else s for s in x]


# 1. data/small_records.json (all sets of size >= 12)
for k, v in json.load(open(R + 'data/small_records.json'))['sets'].items():
    add(v['set'], 'small_records')
# 2. n=14 sets from the CP-SAT extremal census (different engine, different size)
for r in json.load(open(R + 'experiments/20261014-0610-extremal-census/results_sets_n14.json')):
    add(r['set'], 'cpsat_n14')
for s in json.load(open(R + 'experiments/20261014-0610-extremal-census/results/n14_realizable_sets_partial.json')):
    add(s, 'cpsat_n14_partial')
# 3. annealer bests (n=16, 18)
def walk(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'set' and isinstance(v, list) and len(v) >= 12 and all(isinstance(x, int) for x in v):
                out.append(v)
            else:
                walk(v, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, out)
an = []
walk(json.load(open(R + 'experiments/20261013-2257-anneal16/best.json')), an)
for s in an:
    if len(s) <= 18:
        add(s, 'anneal')
# 4. falsifier random/adversarial sets (sizes 12..14 only)
for fn in ('random_sets.json', 'adv_sets.json'):
    d = json.load(open(R + 'experiments/falsify/q8-omega-inequality/' + fn))
    for k, L in d.items():
        for s in L:
            if 12 <= len(s) <= 14:
                add(s, 'q8_' + fn)
# 5. lp-fit dataset: random saturated sets and random subsets; only those whose 12-subsets can have h = 7
for line in gzip.open(R + 'experiments/20261014-0020-lp-fit/dataset.jsonl.gz', 'rt'):
    r = json.loads(line)
    n, a = r['n'], r['alpha']
    if (n == 12 and a == 7) or (n == 13 and a <= 8) or (n == 14 and a <= 9) or (n == 15 and a <= 9) or \
       (n == 16 and a <= 10) or (n == 18 and a <= 11):
        add(r['set'], 'lpfit_n%d' % n)
# 6. A_base two-point extensions (16 points) from experiments/20261014-0640-abase-extensions
AB = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
w = json.load(open(R + 'experiments/20261014-0640-abase-extensions/witnesses.json'))
for p in w['pairs']:
    x, y = Fraction(p['x']), Fraction(p['y'])
    x = int(x) if x.denominator == 1 else x
    y = int(y) if y.denominator == 1 else y
    if x in AB or y in AB or x == y:
        continue
    add(AB + [x, y], 'abase_ext')
sys.stderr.write('candidates=%d by source=%s\n' % (len(seen), json.dumps(tally)))
