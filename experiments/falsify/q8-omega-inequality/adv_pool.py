import json, sys, time, collections
from q8lib import *
from gen_random import gen
out = {}
for n, N in ((12, 6000), (14, 8000), (16, 12000)):
    t = time.time()
    sets, tries = gen(n, N, 5000 + n)
    cases = [(i, n, masks_of(A), 1, 0, 0) for i, A in enumerate(sets)]
    r = run_cases(cases)
    slack0 = {i: min(r[i]['hist']['Q']) for i in r}   # D=empty only
    cnt = collections.Counter(slack0.values())
    print(n, 'gen', len(sets), 'tries', tries, 'D=empty slack dist', sorted(cnt.items())[:10], time.time()-t, flush=True)
    # secondary: D<=2 battery
    r2 = run_cases([(i, n, masks_of(A), 1, 2, 0) for i, A in enumerate(sets)])
    score = {i: (slack0[i], -sum(c for s, c in r2[i]['hist']['Q'].items() if s <= 1)) for i in r2}
    order = sorted(range(len(sets)), key=lambda i: score[i])
    out[str(n)] = [sets[i] for i in order[:300]]
    json.dump(out, open(os.path.join(HERE, 'adv_sets.json'), 'w'))
    print(n, 'top score', [score[i] for i in order[:3]], 'cut', score[order[299]], flush=True)
json.dump(out, open(os.path.join(HERE, 'adv_sets.json'), 'w'))
