"""(L016) Closure check of a recursion cell list: python3 closure.py CELLDIR n m t D [all|first]
For every listed class X and every vertex w of maximum degree d = Delta(X) (or only the first one with 'first'): the components of
X - w (isolated vertices = type (1,0,0)) are put in canonical form by bin/canon and looked up in the lists cell(n_K, m_K, *, d) of
CELLDIR (every key (n_K, m_K, tau, d) with a file); a component must be found (this also gives its tau_K, an isomorphism invariant),
t' = sum of tau_K must lie in {t-1, t}, S' = 3(n-1) + 2(m-d) - 11 t' >= 0, ceil(3m/n) <= d <= D, and the sorted multiset of component
types must be one of engine.decompositions(n-1, m-d, S').  If the lower lists are complete and X is a member of C(n,m,t,D) (Lemma E'),
all of this must hold; so the check tests the stored classes against the lower lists (consistency), not the completeness of the list."""
import sys, os, re, subprocess, math, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
celldir = sys.argv[1]; n, m, t, D = map(int, sys.argv[2:6]); mode = sys.argv[6] if len(sys.argv) > 6 else 'all'
os.environ['CELLDIR'] = celldir; os.environ.setdefault('ENGINELOG', os.devnull)
import engine
def load_found(p):
    return [l.strip() for l in open(p) if l.startswith('FOUND:')]
def edges_of(l): return [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
LIST = os.environ.get('LIST', os.path.join(celldir, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D)))   # the list to check (default: the CELLDIR file)
X_list = load_found(LIST)
print('checking list', LIST, 'against the lower lists of', celldir)
files = collections.defaultdict(list)
for f in os.listdir(celldir):
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', f)
    if mm: a, b, c, dd = map(int, mm.groups()); files[(a, b, dd)].append((c, f))
index = {}
def lookup_table(k, mk, d):
    key = (k, mk, d)
    if key not in index:
        tab = {}
        for tau_k, f in files.get(key, []):
            for l in load_found(os.path.join(celldir, f)): tab[l] = tau_k
        index[key] = tab
    return index[key]
jobs = []          # (class index, w, list of component descriptors)
comp_lines = collections.defaultdict(list)   # k -> list of FOUND lines of relabelled components
probs = 0
for xi, l in enumerate(X_list):
    E = edges_of(l); deg = collections.Counter(v for e in E for v in e)
    assert len(E) == m and set(deg) <= set(range(n))
    d = max(deg.values()); ws = sorted(v for v in range(n) if deg[v] == d)
    if mode == 'first': ws = ws[:1]
    if not (math.ceil(3 * m / n) <= d <= D): print('PROBLEM degree', xi, d); probs += 1
    for w in ws:
        G = [e for e in E if w not in e]; V = [v for v in range(n) if v != w]
        adj = collections.defaultdict(set)
        for e in G:
            for a in e: adj[a].update(e)
        seen = set(); comps = []
        for v in V:
            if v in seen: continue
            st = [v]; seen.add(v); cv = []
            while st:
                u = st.pop(); cv.append(u)
                for x in adj[u]:
                    if x not in seen: seen.add(x); st.append(x)
            comps.append(sorted(cv))
        desc = []
        for cv in comps:
            if len(cv) == 1: desc.append(('iso',)); continue
            rl = {v: i for i, v in enumerate(cv)}; ce = sorted(tuple(sorted(rl[v] for v in e)) for e in G if e[0] in rl)
            comp_lines[len(cv)].append('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in ce))
            desc.append(('comp', len(cv), len(ce), len(comp_lines[len(cv)]) - 1))
        jobs.append((xi, w, d, desc))
canon_of = {}
for k, lines in comp_lines.items():
    out = subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(k)], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True).stdout.splitlines()
    assert len(out) == len(lines)
    canon_of[k] = ['FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in engine.canon_to_edges(c)) for c in out]
dec_cache = {}; types_seen = collections.Counter(); nchecked = 0
for xi, w, d, desc in jobs:
    types = []; ok = True
    for dsc in desc:
        if dsc[0] == 'iso': types.append((1, 0, 0)); continue
        _, k, mk, j = dsc; f = canon_of[k][j]; tab = lookup_table(k, mk, d)
        if f not in tab: ok = False; print('PROBLEM component not found: class', xi, 'w', w, (k, mk), f[:120]); break
        types.append((k, mk, tab[f]))
    if not ok: probs += 1; continue
    tp = sum(c[2] for c in types); Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
    if tp not in (t - 1, t) or Sp < 0: print('PROBLEM tau(X-w)', xi, w, tp, Sp); probs += 1; continue
    key = (n - 1, m - d, Sp)
    if key not in dec_cache: dec_cache[key] = set(tuple(sorted(x)) for x in engine.decompositions(*key))
    T = tuple(sorted(types))
    if T not in dec_cache[key]: print('PROBLEM decomposition not in the engine list', xi, w, T); probs += 1; continue
    types_seen[(d, tp, T)] += 1; nchecked += 1
print('closure (%d,%d,%d,%d) mode=%s: classes %d, (class, max-degree vertex) pairs checked %d, problems %d' % (n, m, t, D, mode, len(X_list), nchecked, probs))
for (d, tp, T), c in sorted(types_seen.items(), key=lambda x: -x[1]): print('   d=%d t\'=%d %s: %d' % (d, tp, list(T), c))
print('RESULT closure', 'OK' if probs == 0 else 'PROBLEMS')
