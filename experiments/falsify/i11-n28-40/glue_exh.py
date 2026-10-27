# exhaustive 1- and 2-vertex identifications of two copies of A_base (14,12,6), and A_base with the (10,7,4)/(8,5,3)/(12,10,5) tight pieces;
# then all single-edge extensions (extend mode).  slack = 3n+2m-11tau.
import itertools, json, collections, subprocess
from common import *
P, cls = load_pieces(); tight = json.load(open('pieces.json'))
pieces = {'Abase': P['Abase']}
for i, d in enumerate(tight):
    pieces['t%d_%d_%d_%d' % (i, d['n'], d['m'], d['slack'])] = (d['n'], [tuple(e) for e in d['edges']])
def glue(A, B, old, new):
    n, e = A; pn, pe = B; mp = dict(zip(new, old)); nxt = n
    for v in range(pn):
        if v not in mp: mp[v] = nxt; nxt += 1
    return nxt, list(e) + [tuple(mp[v] for v in x) for x in pe]
summary = {}
allg = []
for nameB, B in pieces.items():
    A = P['Abase']; lines = []; meta = []
    for j in (1, 2):
        for old in itertools.permutations(range(A[0]), j):
            for new in itertools.combinations(range(B[0]), j) if j == 2 else itertools.combinations(range(B[0]), j):
                if j == 2 and old[0] > old[1] and False: continue
                n, e = glue(A, B, old, new); lines.append(line(n, e)); meta.append((j, n, e))
    res = run_eval(lines)
    cnt = collections.Counter(); mn = {}
    for (j, n, e), r in zip(meta, res):
        if r is None or r[4] != 0: continue
        key = (j, r[0]); cnt[key] += 1
        if key not in mn or r[3] < mn[key][0]: mn[key] = (r[3], r[1], r[2])
        allg.append(line(n, e))
    summary[nameB] = {'%d-ident n=%d' % k: dict(count=cnt[k], min_slack=mn[k][0], m=mn[k][1], tau=mn[k][2]) for k in sorted(cnt)}
    print(nameB, summary[nameB], flush=True)
json.dump(summary, open('out/glue_exh.json', 'w'), indent=1)
open('out/glue_exh_graphs.txt', 'w').write("\n".join(allg) + "\n")
