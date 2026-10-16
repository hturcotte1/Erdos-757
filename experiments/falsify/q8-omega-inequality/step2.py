import json, sys, time, collections
from q8lib import *
from e757.core import alpha
S = json.load(open(os.path.join(HERE, sys.argv[1] if len(sys.argv)>1 else 'random_sets.json')))
tag = sys.argv[2] if len(sys.argv)>2 else 'step2'
summary = {}
allviol = []
for nk, sets in S.items():
    n = int(nk); t = time.time()
    cases = []
    hs = collections.Counter()
    for i, A in enumerate(sets):
        ms = masks_of(A)
        cases.append((2*i, n, ms, 1, 3, 0)); cases.append((2*i+1, n, ms, 2, 2000, i+7))
        if n == 12 or (n == 14 and i < 100): cases.append((100000+i, n, ms, 0, 0, 0))   # full 3^n states
        hs[len(ms)] += 1
    res = run_cases(cases, vcap=20)
    tot = collections.Counter(); hist = collections.Counter(); minslack=None; eq=0
    for cid, r in res.items():
        for k in ('states','violQ','violAct','violD4','eqQ'): tot[k] += r[k]
        for s, c in r['hist']['Q'].items(): hist[s] += c
        for v in r['viol']: allviol.append((n, cid, v))
    summary[nk] = dict(sets=len(sets), edges=dict(hs), **tot, minslackQ=min(hist), hist_lowest=sorted(hist.items())[:6], time=time.time()-t)
    print(nk, summary[nk], flush=True)
# tau/n statistics for D=empty : min over sets of (3n-7tau) given in hist anyway
json.dump(dict(summary=summary, violations=allviol), open(os.path.join(HERE, tag + '_results.json'), 'w'))
