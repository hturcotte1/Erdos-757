"""Minimal non-realizable sub-configurations (edge subsets) of the non-realizable tight class (10,7,4)#0
{012,034,157,268,379,489,569} (L022 Theorem 5): every edge subset with >= 5 edges is tested with rexact.decide (all
labellings); prints the inclusion-minimal non-realizable ones (members of M_R with maximum degree <= 3).
usage: python3 minimal_obstruction_10_7_4.py"""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9')
from rexact import decide
E = [(0,1,2), (0,3,4), (1,5,7), (2,6,8), (3,7,9), (4,8,9), (5,6,9)]
nonreal = []
for k in range(5, 8):
    for sub in itertools.combinations(E, k):
        if any(set(s) <= set(sub) for s in nonreal):
            continue
        vs = sorted({x for e in sub for x in e}); mp = {v: i for i, v in enumerate(vs)}
        sols, st = decide([tuple(mp[x] for x in e) for e in sub], len(vs), find_all=False)
        if not sols:
            nonreal.append(sub)
            deg = {}
            for e in sub:
                for x in e: deg[x] = deg.get(x, 0) + 1
            print('minimal non-realizable:', sub, 'vertices', len(vs), 'max degree', max(deg.values()), flush=True)
print('number of minimal non-realizable edge subsets:', len(nonreal))

# Part 2: maximum degree of every stored obstruction of the (21,18,9) run (experiments/20261027-0400-realize-21-18-9/obstructions.json)
import json
obs = json.load(open('/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9/obstructions.json'))
for o in obs:
    deg = {}
    for e in o['subedges']:
        for x in e: deg[x] = deg.get(x, 0) + 1
    print('obstruction of (21,18,9) class', o['cls'], 'edges', o['k'], 'vertices', o['nverts'], 'max degree', max(deg.values()))
print('all stored obstructions have a vertex of degree >= 4:', all(max({x: sum(1 for e in o['subedges'] if x in e) for e in o['subedges'] for x in e}.values()) >= 4 for o in obs))
