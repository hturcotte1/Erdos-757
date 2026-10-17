"""Referee (L013 round 2): audit of the prover's cell directory against the referee's decompositions.
For every cell file: count classes, route; for recursion cells: the branch set must equal {(d,tp): ceil(3m/n) <= d <= D, tp in {t-1,t},
S' >= 0}; the decomposition list must equal decomp_ref.decomps(n-1, m-d, S') (as multisets); the input count of every decomposition must
equal prod C(|cell(type,d)|+k-1, k); ext_d counters: graphs == searched == inputs, bad_tau == 0."""
import sys, os, re, json, math
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp_ref import decomps
D_ = sys.argv[1]
cells = {}
for fn in os.listdir(D_):
    mt = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
    if not mt: continue
    key = tuple(map(int, mt.groups())); reps = 0; info = None
    for l in open(os.path.join(D_, fn)):
        if l.startswith('FOUND:'): reps += 1
        elif l.startswith('INFO '): info = json.loads(l[5:])
    cells[key] = (reps, info)
def size(typ, d):
    if typ == (1, 0, 0): return 1
    k = typ + (d,)
    if k in cells: return cells[k][0]
    n, m, t = typ
    # engine guard returns [] without a file in these cases
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or d < 1: return 0
    raise KeyError(k)
probs = []; nrec = ndir = nonempty = classes = nbr = ndec = 0
for key, (reps, info) in sorted(cells.items()):
    n, m, t, D = key
    if info is None: probs.append(('noinfo', key)); continue
    classes += reps; nonempty += reps > 0
    if info['route'] == 'direct': ndir += 1; continue
    nrec += 1
    want = [(d, tp) for d in range(max(1, -(-3 * m // n)), D + 1) for tp in (t - 1, t) if 3 * (n - 1) + 2 * (m - d) - 11 * tp >= 0 and tp >= 0]
    got = [(b['d'], b['tp']) for b in info['branches']]
    if sorted(want) != sorted(got): probs.append(('branchset', key, want, got))
    for b in info['branches']:
        nbr += 1; d, tp, Sp = b['d'], b['tp'], b['Sp']
        if Sp != 3 * (n - 1) + 2 * (m - d) - 11 * tp: probs.append(('Sp', key, b['d'], b['tp']))
        mine = sorted(decomps(n - 1, m - d, Sp)); theirs = sorted(tuple(sorted(tuple(x) for x in dec)) for dec, _ in b['dec'])
        ndec += len(mine)
        if mine != theirs: probs.append(('decomp', key, d, tp, len(mine), len(theirs)))
        if b['decompositions'] != len(theirs): probs.append(('ndec', key, d, tp))
        tot = 0
        for dec, sz in b['dec']:
            c = Counter(tuple(x) for x in dec); p = 1
            for typ, k in c.items(): p *= math.comb(size(typ, d) + k - 1, k)
            if p != sz: probs.append(('inputs', key, d, tp, dec, p, sz))
            tot += p
        if tot != b['inputs']: probs.append(('totinputs', key, d, tp, tot, b['inputs']))
        if b['inputs']:
            e = b['ext']
            if not (e['graphs'] == e['searched'] == b['inputs'] and e['bad_tau'] == 0): probs.append(('ext', key, d, tp, e))
            if e.get('tg_too_small', 0): probs.append(('tg_too_small', key, d, tp))
print(json.dumps(dict(cells=len(cells), recursion=nrec, direct=ndir, nonempty=nonempty, classes=classes, branches=nbr, decompositions=ndec, problems=len(probs))))
for p in probs[:50]: print('PROBLEM', p)
