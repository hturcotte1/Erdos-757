import json, random, sys, time
from q8lib import *
from e757.anneal import random_linear_map, evaluate
from e757.saturated import to_integers
def gen(n, count, seed, nfree=0):
    rng = random.Random(seed); sets = []; tries = 0; seen = set()
    t = time.time()
    while len(sets) < count:
        tries += 1
        try: m = random_linear_map(n, rng, nfree=nfree)
        except RuntimeError: continue
        ev = evaluate(m)
        if not ev['is45']: continue
        ints = to_integers(ev['vals'])
        ints = sorted(ints)
        if len(set(ints)) != n: continue
        if not is_45_set(ints): continue   # exact recheck with core
        key = tuple(ints)
        if key in seen: continue
        seen.add(key); sets.append(ints)
    return sets, tries
if __name__ == '__main__':
    out = {}
    for n in (12, 14, 16):
        t = time.time(); s, tries = gen(n, 300, 1000 + n)
        out[str(n)] = s; print(n, len(s), 'tries', tries, 'time', time.time() - t, flush=True)
    json.dump(out, open(os.path.join(HERE, 'random_sets.json'), 'w'))
