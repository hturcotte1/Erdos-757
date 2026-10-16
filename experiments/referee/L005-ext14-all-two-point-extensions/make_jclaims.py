"""Write claim files (in this scratch folder only, subfolder jclaims/) for the frozen verifier: 2 random (4,5) T1b
extensions B (expected PASS, h = 10) from each of 8 classes (7 random + A_base class 2440), and 3 points of the deficient
locus D of A_base (expected FAIL: not (4,5))."""
import json, gzip, random, itertools, os
import cases, locus
sets = [json.loads(l)['set'] for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') if l.strip()]
rng = random.Random(757)
cls = rng.sample(range(len(sets)), 7) + [2440]
written = []
for c in cls:
    A = sorted(12 * v for v in sets[c])
    Px = sorted(cases.ap_partners(A))
    ok1 = [x for x in Px if all(locus.ndist((x,) + q) >= 5 for q in itertools.combinations(A, 3))]
    found = []
    tries = 0
    while len(found) < 2 and tries < 5000:
        tries += 1
        x = rng.choice(ok1)
        y = rng.choice(sorted(cases.ap_partners(A + [x])))
        if locus.b_is45(A, x, y):
            found.append((x, y))
    for t, (x, y) in enumerate(found):
        cid = 'REF-L005-c%d-%d' % (c, t)
        json.dump({'id': cid, 'type': 'construction', 'set': sorted(A + [x, y]), 'claimed_h': 10,
                   'notes': 'referee L005 spot check: class %d scaled by 12 plus T1b pair (%d,%d)' % (c, x, y)},
                  open('jclaims/%s.json' % cid, 'w'))
        written.append(cid)
A = sorted(12 * v for v in sets[2440])
h, M, W, P = locus.deficient_locus(A)
for t, (x, y) in enumerate(sorted(P)[:3]):
    cid = 'REF-L005-locus-%d' % t
    json.dump({'id': cid, 'type': 'construction', 'set': sorted(A + [x, y]),
               'notes': 'referee L005: deficient-locus point (%d,%d) of A_base*12, expected not (4,5)' % (x, y)},
              open('jclaims/%s.json' % cid, 'w'))
    written.append(cid)
print(written)
