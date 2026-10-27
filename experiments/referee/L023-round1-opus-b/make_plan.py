"""Build the sample plan for ext_check.py: decompositions of (19,13) with total slack 6 (own generator decomp_own_lib.own), inputs as
multisets of class indices per type group (in the order of the decomposition's sorted types); full enumeration for decompositions with
<= FULL inputs, a seeded random sample (seed 20261027) of SAMPLE inputs for the others.  Prints the own input count per decomposition
(to be compared with the engine's INFO record)."""
import json, random, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext_check import child
from decomp_own_lib import own
FULL = int(sys.argv[1]); SAMPLE = int(sys.argv[2]); OUT = sys.argv[3]
rng = random.Random(20261027)
plan = []; tot = 0; sel = 0
for dec in own(19, 13, 6):
    dec = sorted(dec)
    groups = []
    for typ, grp in itertools.groupby(dec):
        k = len(list(grp)); L = len(child(typ))
        groups.append((typ, k, list(itertools.combinations_with_replacement(range(L), k))))
    size = 1
    for g in groups: size *= len(g[2])
    tot += size
    if size == 0: print('DEC', dec, 'inputs 0'); continue
    def build(choice):
        flat = []
        for (typ, k, cs), c in zip(groups, choice): flat += list(cs[c])
        return flat
    types_flat = []
    for typ, k, cs in groups: types_flat += [typ] * k
    if size <= FULL:
        combos = [build(ch) for ch in itertools.product(*[range(len(g[2])) for g in groups])]
    else:
        seen = set(); combos = []
        while len(combos) < SAMPLE:
            ch = tuple(rng.randrange(len(g[2])) for g in groups)
            if ch in seen: continue
            seen.add(ch); combos.append(build(ch))
    sel += len(combos)
    plan.append([types_flat, combos])
    print('DEC', dec, 'inputs', size, 'selected', len(combos))
print('TOTAL inputs', tot, 'selected', sel)
json.dump(plan, open(OUT, 'w'))
