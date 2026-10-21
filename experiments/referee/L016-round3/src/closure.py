# closure.py n m t D LIST CELLDIR CANON: for every class X of LIST and every vertex w of maximum degree d, the components of X-w are
# canonicalised (nauty via L012's refereed canon, used only as an isomorphism oracle) and looked up in CELLDIR/cell_nK_mK_*_D{d}.txt
# (own canonicalisation of those lists through the same oracle). Checks: every component found (exactly one tau), sum tau_K in {t-1,t},
# S' = 3(n-1)+2(m-d)-11 sum tau_K >= 0, and the type multiset is one of own decompositions(n-1, m-d, S'). Consistency check, not completeness.
import sys, os, subprocess, collections, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp import decompositions
n, m, t, D = map(int, sys.argv[1:5]); LIST, CELLDIR, CANON = sys.argv[5], sys.argv[6], sys.argv[7]
def parse(line): return [tuple(map(int, x.strip('()').split(','))) for x in line.split()[1:]]
classes = [parse(l) for l in open(LIST) if l.startswith('FOUND')]
print('classes', len(classes))
def components(edges, nv, w):
    par = list(range(nv))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    rest = [e for e in edges if w not in e]
    for a, b, c in rest: par[f(b)] = f(a); par[f(c)] = f(a)
    groups = collections.defaultdict(list)
    for v in range(nv):
        if v != w: groups[f(v)].append(v)
    comps = []
    for root, vs in groups.items():
        vs.sort(); idx = {v: i for i, v in enumerate(vs)}
        es = sorted(tuple(sorted(idx[x] for x in e)) for e in rest if e[0] in idx)
        comps.append((len(vs), len(es), '%d ' % len(es) + ' '.join('%d %d %d' % e for e in es)))
    return comps
records = []          # (ci, w, d, [(nK, mK, compstr)])
uniq = collections.defaultdict(dict)   # nK -> compstr -> None (then canonical)
pairs = 0
for ci, X in enumerate(classes):
    deg = collections.Counter(v for e in X for v in e)
    assert len(X) == m and max(max(e) for e in X) < n
    d = max(deg.values())
    for w in range(n):
        if deg.get(w, 0) != d: continue
        comps = components(X, n, w); pairs += 1
        for nK, mK, s in comps:
            if mK > 0: uniq[nK][s] = None
        records.append((ci, w, d, comps))
print('(class, max-degree vertex) pairs', pairs, 'unique components with edges', sum(len(v) for v in uniq.values()))
def canon_batch(nK, strings):
    if not strings: return []
    out = subprocess.run([CANON, str(nK)], input='\n'.join(strings) + '\n', capture_output=True, text=True, check=True).stdout.split('\n')
    out = [l for l in out if l.startswith('C ')]
    assert len(out) == len(strings), (nK, len(out), len(strings))
    return out
for nK in uniq:
    keys = list(uniq[nK]); cf = canon_batch(nK, keys)
    for k, c in zip(keys, cf): uniq[nK][k] = c
# lower lists: for every (nK, mK, d) that occurs, canonicalise all cell_nK_mK_*_D{d}.txt lists
need = set()
for ci, w, d, comps in records:
    for nK, mK, s in comps:
        if mK > 0: need.add((nK, mK, d))
lookup = {}   # (nK, mK, d) -> dict canonical -> tK
missing_lists = []
for (nK, mK, d) in sorted(need):
    table = {}
    files = sorted(glob.glob('%s/cell_%d_%d_*_D%d.txt' % (CELLDIR, nK, mK, d)))
    if not files: missing_lists.append((nK, mK, d))
    for fpath in files:
        tK = int(os.path.basename(fpath).split('_')[3])
        lines = [l.strip() for l in open(fpath) if l.startswith('FOUND')]
        for c in canon_batch(nK, lines):
            if c in table and table[c] != tK: print('ERROR: same class in two tau lists', nK, mK, d, c)
            table[c] = tK
    lookup[(nK, mK, d)] = table
print('lower lists needed for (nK,mK,d):', sorted(need)); print('missing lists:', missing_lists)
problems = 0; typecount = collections.Counter(); deccache = {}
for ci, w, d, comps in records:
    types = []; ok = True
    for nK, mK, s in comps:
        if mK == 0: types.append((1, 0, 0)); continue
        c = uniq[nK][s]; tab = lookup.get((nK, mK, d), {})
        if c not in tab: ok = False; print('NOT FOUND: class %d vertex %d component (%d,%d) %s' % (ci, w, nK, mK, s)); break
        types.append((nK, mK, tab[c]))
    if not ok: problems += 1; continue
    st = sum(x[2] for x in types); Sp = 3 * (n - 1) + 2 * (m - d) - 11 * st
    key = (d, Sp)
    if key not in deccache: deccache[key] = set(decompositions(n - 1, m - d, Sp)) if Sp >= 0 else set()
    if st not in (t - 1, t) or Sp < 0 or tuple(sorted(types)) not in deccache[key]:
        problems += 1; print('BAD DECOMPOSITION: class %d vertex %d types %s sum tau %d Sp %d' % (ci, w, sorted(types), st, Sp)); continue
    typecount[tuple(sorted(types))] += 1
print('type multiset counts:'); 
for k, v in sorted(typecount.items(), key=lambda kv: -kv[1])[:40]: print('  ', v, list(k))
print('RESULT closure (%d,%d,%d,%d): classes %d pairs %d problems %d %s' % (n, m, t, D, len(classes), pairs, problems, 'OK' if problems == 0 and not missing_lists else 'PROBLEMS'))
