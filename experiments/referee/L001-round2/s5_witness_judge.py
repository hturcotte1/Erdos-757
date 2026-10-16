"""Step 5: (a) check EVERY entry of the authors' witnesses.json against the definitions;
(b) write judge input files for A, all 50 A u {x}, and a sample of 200 pairs B (plus the 3 extreme-coordinate pairs)."""
import json, sys, random, os
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import *

E = '/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/'
W = json.load(open(E + 'witnesses.json'))
R = json.load(open(E + 'results.json'))
AF = [F(a) for a in ABASE]
bad = 0
for w in W['pairs']:
    x, y = F(w['x']), F(w['y'])
    S = [F(v) for v in w['S']]
    ok = (len(S) == 10 and len(set(S)) == 10 and set(S) <= set(AF) | {x, y} and x not in AF and y not in AF and x != y
          and is_sidon(to_ints(S)[0]) and is45(AF + [x, y]))
    bad += not ok
print('witnesses.json pairs:', len(W['pairs']), 'failures:', bad)
bad = 0
for w in W['generic_y']:
    x = F(w['x'])
    S = [F(v) for v in w['S9']]
    ok = len(S) == 9 and len(set(S)) == 9 and set(S) <= set(AF) | {x} and is_sidon(to_ints(S)[0]) and is45(AF + [x])
    bad += not ok
print('witnesses.json generic_y:', len(W['generic_y']), 'failures:', bad)
# stored pairs in results.json == witness pairs (as exact Fractions)
st = {frozenset((F(a), F(b))) for a, b, h in R['stored']}
wp = {frozenset((F(w['x']), F(w['y']))) for w in W['pairs']}
print('results.json stored == witnesses.json pairs (exact):', st == wp, len(st), len(wp))
# judge inputs
os.makedirs('jin', exist_ok=True)
def dump(name, pts, h):
    json.dump({'id': name, 'type': 'construction', 'set': [str(p) for p in pts], 'claimed_h': h,
               'notes': 'referee L001 round 2 check'}, open('jin/%s.json' % name, 'w'))
dump('r2-abase', AF, 8)
for i, w in enumerate(W['generic_y']):
    dump('r2-ax-%02d' % i, AF + [F(w['x'])], 9)
rng = random.Random(5)
sample = rng.sample(W['pairs'], 200)
ext = sorted(W['pairs'], key=lambda w: min(F(w['x']), F(w['y'])))[:2] + \
      sorted(W['pairs'], key=lambda w: max(F(w['x']), F(w['y'])))[-2:]
for i, w in enumerate(sample + ext):
    dump('r2-b-%03d' % i, AF + [F(w['x']), F(w['y'])], 10)
print('judge files written:', len(os.listdir('jin')))
