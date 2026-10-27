"""How many of the 45 classes are hit by the prover's pattern-(f) gluings from (18,13,7,3) and the
pattern-(b) sample from (25,19,10,3)?  (own WL + exact isomorphism)."""
import sys, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
cls = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
table = {}
inv = {}
for i, c in enumerate(cls):
    k = hg.wl_invariant(c['n'], [tuple(e) for e in c['edges']], table)[0]
    inv[k] = i
for f in ['bf_18_13_7.json', 'bf_25_19_10_sample.json']:
    d = json.load(open('/home/user/Erdos-757/experiments/prover/L020/' + f))
    g29 = [g for g in d if g['n'] == 29]
    hit = set()
    unmatched = 0
    for g in g29:
        es = [tuple(e) for e in g['edges']]
        k = hg.wl_invariant(29, es, table)[0]
        if k in inv and hg.iso_exact(29, es, 29, [tuple(e) for e in cls[inv[k]]['edges']]) is not None:
            hit.add(inv[k])
        else:
            unmatched += 1
    print(f, 'graphs with 29 vertices', len(g29), 'distinct classes among the 45 hit', len(hit), 'not among the 45', unmatched)
