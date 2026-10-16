"""Referee L004, check D: completeness test against data NOT produced by the census pipeline.
Collect 14-point sets (and all 14-subsets of larger sets whose h could drop to 8) from other engines / generators in the
repository, deduplicate by affine normal form, and for every (4,5)-set with h = 8 and m = 12 check that its class is
one of the census classes. Also tallies (m, h) for h <= 8 (m = 11, h = 8 sets would be non-saturated extremal sets,
outside the claim's scope).
usage: python3 collect14.py CENSUS_POSTDIR > log"""
import sys, json, gzip, glob, os, itertools, collections
from fractions import Fraction
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "realize14.py")).read().split("if __name__")[0])  # three_aps, is45, sidon_max, normal_form

R = '/home/user/Erdos-757/'
POST = sys.argv[1]
census_nf = set()
for f in sorted(glob.glob(os.path.join(POST, "real_*.json.gz"))):
    for r in json.load(gzip.open(f, "rt"))["real"]:
        census_nf.add(normal_form(r["set"]))
print("census classes", len(census_nf), flush=True)

seen = set(); tally = collections.Counter(); res = collections.Counter(); hits = collections.defaultdict(list)


def toint(v):
    v = [Fraction(x) for x in v]
    L = 1
    for x in v: L = L * x.denominator // gcd(L, x.denominator)
    return sorted(int(x * L) for x in v)


def consider(S, src):
    if len(set(S)) != 14: return
    nf = normal_form(S)
    if nf in seen: return
    seen.add(nf); tally[src] += 1
    s = set(nf); m = 0
    for a, c in itertools.combinations(nf, 2):
        if (a + c) % 2 == 0 and (a + c) // 2 in s: m += 1
    if m < 11: return
    if not is45(nf): res[(m, "not45")] += 1; return
    h = sidon_max(nf)
    res[(m, h)] += 1
    if h <= 8:
        hits[(m, h)].append((nf, src))


def add(A, src):
    A = toint(sorted(set(A)))
    if len(A) < 14: return
    if len(A) == 14: consider(A, src); return
    for S in itertools.combinations(A, 14): consider(list(S), src)


AB = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
add(AB, "A_base")
for k, v in json.load(open(R + 'data/small_records.json'))['sets'].items():
    add(v['set'], 'small_records')
for r in json.load(open(R + 'experiments/20261014-0610-extremal-census/results_sets_n14.json')):
    add(r['set'], 'cpsat_n14')
for s in json.load(open(R + 'experiments/20261014-0610-extremal-census/results/n14_realizable_sets_partial.json')):
    add(s, 'n14_partial_sets')
an = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'set' and isinstance(v, list): an.append(v)
            else: walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(json.load(open(R + 'experiments/20261013-2257-anneal16/best.json')))
for s in an: add(s, 'anneal')
for fn in ('random_sets.json', 'adv_sets.json'):
    d = json.load(open(R + 'experiments/falsify/q8-omega-inequality/' + fn))
    for k, L in d.items():
        for s in L:
            if 14 <= len(s) <= 16: add(s, 'q8_' + fn)
print("after small sources", dict(tally), flush=True)
for line in gzip.open(R + 'experiments/20261014-0020-lp-fit/dataset.jsonl.gz', 'rt'):
    r = json.loads(line); n, a = r['n'], r['alpha']
    if (n == 14 and a <= 9) or (n == 15 and a <= 9) or (n == 16 and a <= 10) or (n == 17 and a <= 11) or (n == 18 and a <= 11):
        add(r['set'], 'lpfit_n%d' % n)
print("after lpfit", dict(tally), flush=True)
w = json.load(open(R + 'experiments/20261014-0640-abase-extensions/witnesses.json'))
for p in w['pairs']:
    x, y = Fraction(p['x']), Fraction(p['y'])
    if x in AB or y in AB or x == y: continue
    add(AB + [x, y], 'abase_ext')
print("candidates", len(seen), "by source", dict(tally))
print("(m, h or not45) tally for m >= 11:", sorted(res.items(), key=str))
for (m, h), L in sorted(hits.items()):
    inc = sum(1 for nf, _ in L if nf in census_nf)
    srcs = collections.Counter(s for _, s in L)
    print("m=%d h=%d: %d sets, in census classes: %d, sources %s" % (m, h, len(L), inc, dict(srcs)))
    if m == 12 and h == 8 and inc != len(L):
        for nf, s in L:
            if nf not in census_nf: print("  NOT IN CENSUS:", s, nf)
    if m == 11:
        for nf, s in L[:20]: print("  m=11 extremal:", s, nf)
