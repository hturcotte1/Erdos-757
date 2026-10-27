# realizable (4,5)-sets: greedy / randomised one-point extension (new point in >=1 new 3-AP), exact integers, (4,5) verified, slack by exact tau.
import sys, json, random, itertools, time, collections
from fractions import Fraction
from common import *
from e757.core import is_45_set, distinct_distances, ap_edges
random.seed(int(sys.argv[1])); TL = float(sys.argv[2]); out = sys.argv[3]
P, cls = load_pieces()
sm = json.load(open(os.path.join(ROOT, 'data/small_records.json')))['sets']
fam = {x['K']: x['set'] for x in json.load(open(os.path.join(ROOT, 'data/reader_5_9_family.json')))['family']}
def glue_sets(A, B, q=1000003, t=10**12):
    A = sorted(A); B = sorted(B); C = A + [q * b + t for b in B]
    return C
def ok45_with(X, Xset, sums, x):
    # quick weak-Sidon reject, then full check on 4-sets containing x
    if x in Xset: return False
    for a in X:
        s = x + a
        if s in sums: return False
    for a, b, c in itertools.combinations(X, 3):
        if distinct_distances((x, a, b, c)) < 5: return False
    return True
def slack_batch(sets_):
    ls = []
    for S in sets_:
        n, e = graph_of_set(S); ls.append(line(n, e))
    return run_eval(ls)
def candidates(X):
    Xs = set(X); c = set()
    for a, b in itertools.combinations(sorted(X), 2):
        if (a + b) % 2 == 0: c.add((a + b) // 2)
        c.add(2 * a - b); c.add(2 * b - a)
    return [x for x in c if x not in Xs]
def extend_once(X, k_eval=40):
    X = sorted(X); sums = set(a + b for a, b in itertools.combinations(X, 2)); Xs = set(X)
    cand = [x for x in candidates(X) if all((x + a) not in sums for a in X)]
    random.shuffle(cand); good = []
    for x in cand:
        if len(good) >= k_eval: break
        if ok45_with(X, Xs, sums, x): good.append(x)
    if not good: return None
    res = slack_batch([X + [x] for x in good])
    return [(r[3], x, r) for x, r in zip(good, res)]
best = collections.defaultdict(lambda: 999); log = []
def walk(X, tag, greedy=True, maxn=40):
    X = sorted(X)
    while len(X) < maxn:
        ch = extend_once(X)
        if not ch: break
        ch.sort(key=lambda t: t[0] + (random.random() if not greedy else random.random() * 0.5))
        s, x, r = ch[0] if greedy else random.choice(ch[:5])
        X = sorted(X + [x]); n = len(X)
        if r[4] != 0: print("!!! realizable set not in C ?", tag); 
        if s < best[n]: best[n] = s
        log.append((tag, n, r[1], r[2], s, r[6]))
        if s < 0: print("!!! NEGATIVE SLACK realizable", X, flush=True); json.dump(dict(set=X, n=n, slack=s), open('out/COUNTEREXAMPLE_real.json', 'w')); return
        if s <= 1 and n >= 15: open('out/low_real.txt', 'a').write(json.dumps(dict(n=n, slack=s, m=r[1], tau=r[2], set=X)) + "\n")
t0 = time.time(); it = 0
bases = {'A+A': glue_sets(sm['14']['set'], sm['14']['set']), 'A+12': glue_sets(sm['14']['set'], sm['12']['set']), '12+12b': glue_sets(sm['12']['set'], sm['12b']['set']),
         'A+12c+10': glue_sets(glue_sets(sm['14']['set'], sm['12c']['set']), sm['10']['set'])}
while time.time() - t0 < TL:
    it += 1; r = random.random()
    if r < 0.4:
        k = random.choice(list(bases)); X = bases[k]; tag = k
        # random sub-selection of 22..all points
        if random.random() < 0.5: X = random.sample(X, random.randint(20, len(X)))
    else:
        K = random.choice([2, 3, 4, 5]); S = fam[K]; sz = random.randint(24, min(len(S), 36)); X = random.sample(S, sz); tag = 'S%d-sub%d' % (K, sz)
    walk(X, tag, greedy=random.random() < 0.7, maxn=40)
json.dump(dict(iterations=it, best_slack_by_n=dict(sorted(best.items())), steps=len(log), steps_by_n=dict(sorted(collections.Counter(l[1] for l in log).items()))), open(out, 'w'), indent=1)
print(json.dumps(dict(sorted(best.items()))))
