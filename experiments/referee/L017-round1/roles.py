# Referee L017 round 1: independent recomputation of the Theorem 4(iv) role counts (C5 / Corollary 13.3)
# and of the non-co-transversal pair types (Remark 13.2) on the stored Delta<=3 tight and slack-1 lists.
import os, re, sys, subprocess, itertools, collections, json
HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = os.path.join(HERE, 'cells')
LISTS = [  # (cell, path) -- Delta<=3 lists
 ((3,1,1),  'L012/cells/cell_3_1_1_D3.txt'),
 ((10,7,4), 'L012/cells/cell_10_7_4_D3.txt'),
 ((14,12,6),'L012/cells/cell_14_12_6_D3.txt'),
 ((17,13,7),'L012/cells/cell_17_13_7_D3.txt'),
 ((8,5,3),  'L012/cells/cell_8_5_3_D3.txt'),
 ((12,10,5),'L012/cells/cell_12_10_5_D3.txt'),
 ((15,11,6),'L012/cells/cell_15_11_6_D3.txt'),
 ((19,16,8),'L012/cells/cell_19_16_8_D3.txt'),
 ((22,17,9),'L012/cells/cell_22_17_9_D3.txt'),
 ((26,22,11),'L016/cells_new/runF/cell_26_22_11_D3.txt'),
]
def parse(path):
    gs = []
    for line in open(path):
        if line.startswith('FOUND:'):
            gs.append([tuple(int(x) for x in t.split(',')) for t in re.findall(r'\(([^)]*)\)', line)])
    return gs
def run_cotrans(graphs_nm):
    inp = ''.join('%d %d %s\n' % (n, len(E), ' '.join('%d %d %d' % e for e in E)) for n, E in graphs_nm)
    out = subprocess.run([os.path.join(HERE, 'src', 'cotrans')], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()
    res = []
    for line in out:
        tok = line.split(); t = int(tok[0].split('=')[1]); ncv = int(tok[1].split('=')[1])
        cv = set(map(int, tok[2:2+ncv])); rest = tok[2+ncv:]; npairs = int(rest[0].split('=')[1]); nums = list(map(int, rest[1:]))
        NP = {frozenset((nums[2*i], nums[2*i+1])) for i in range(npairs)}
        res.append((t, cv, NP))
    return res
summary = {}
grand = collections.Counter()
for (cell, rel) in LISTS:
    n, m, t0 = cell
    gs = parse(os.path.join(CELLS, rel))
    data = run_cotrans([(n, E) for E in gs])
    cnt = collections.Counter(); types = collections.Counter(); nonzero = collections.Counter()
    for E, (t, cv, NP) in zip(gs, data):
        assert len(E) == m
        V = sorted(set(v for e in E for v in e)); assert len(V) == n and V == list(range(n))
        deg = collections.Counter(v for e in E for v in e)
        assert max(deg.values()) <= 3
        # membership checks: linear
        for e, f in itertools.combinations(E, 2): assert len(set(e) & set(f)) <= 1
        assert t == t0, (cell, t)
        assert 3*n + 2*m - 11*t in (0, 1)
        inedge = set()
        for e in E:
            for a, b in itertools.combinations(e, 2): inedge.add(frozenset((a, b)))
        att = [v for v in range(n) if deg[v] <= 2]
        # Lemma U'' (vertex form): every vertex co-transversal (s(F) <= 1 < 3 + 2d, d >= 1)
        cnt['vertex_pred'] += n; cnt['vertex_fail'] += len(cv)
        # pair lemma: non-co-transversal pair => 2|d(x,y)| <= s+5
        s = 3*n + 2*m - 11*t
        for pr in NP:
            x, y = tuple(pr)
            dxy = deg[x] + deg[y] - (1 if pr in inedge else 0)
            if 2*dxy > s + 5: cnt['pairlemma_fail'] += 1
            types[(min(deg[x], deg[y]), max(deg[x], deg[y]), 1 if pr in inedge else 0)] += 1
        cnt['pairs'] += n*(n-1)//2; cnt['np_pairs'] += len(NP)
        npa = lambda a, b: frozenset((a, b)) in NP
        # role_b: 3 pairwise non-co-transversal attachment vertices
        rb = sum(1 for tr in itertools.combinations(att, 3) if npa(tr[0], tr[1]) and npa(tr[0], tr[2]) and npa(tr[1], tr[2]))
        pairs_ok = [pr for pr in itertools.combinations(att, 2) if frozenset(pr) not in inedge]  # possible P_j inside F
        # role_c: two disjoint P-pairs with all four cross pairs non-co-transversal
        rc = 0
        for P, Q in itertools.combinations(pairs_ok, 2):
            if set(P) & set(Q): continue
            if all(npa(x, y) for x in P for y in Q): rc += 1
        # role_e: P = {a,b} (not in an edge) and e with {a,e},{b,e} non-co-transversal
        re_ = 0
        for P in pairs_ok:
            for e in att:
                if e in P: continue
                if npa(P[0], e) and npa(P[1], e): re_ += 1
        # role_f1: P = {a,b} (not in an edge) and {c,e} (any two further attachment vertices) with 4 cross pairs non-co-transversal
        rf1 = 0
        for P in pairs_ok:
            others = [v for v in att if v not in P]
            for c, e in itertools.combinations(others, 2):
                if all(npa(x, y) for x in P for y in (c, e)): rf1 += 1
        # role_f2: {d,f} attachment vertices, non-co-transversal (may share an edge)
        rf2 = sum(1 for d, f in itertools.combinations(att, 2) if npa(d, f))
        for k, val in (('b', rb), ('c', rc), ('e', re_), ('f1', rf1), ('f2', rf2)):
            if val: nonzero[k] += 1
        cnt['graphs'] += 1
        cnt['graphs_with_np'] += 1 if NP else 0
    grand.update(cnt)
    summary[str(cell)] = {'classes': len(gs), 'counts': dict(cnt), 'classes_with_nonzero_role': dict(nonzero),
                          'np_pair_types': {str(k): v for k, v in sorted(types.items())}}
    print(cell, len(gs), dict(cnt), 'nonzero roles:', dict(nonzero), 'types:', dict(types), flush=True)
json.dump(summary, open(os.path.join(HERE, 'roles_output.json'), 'w'), indent=1)
print('TOTAL', dict(grand))
