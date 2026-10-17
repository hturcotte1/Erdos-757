# Referee round 2: base cells (enumerated directly by the prover with enum_conn) re-enumerated with unmodified nauty genbg
# (connected bipartite incidence graphs, edge side degree exactly 3, vertex side degree 1..D, -Z1 = linear), my graph6 decoder,
# my filter fr (C membership, tau, connectivity, degree) and BLISS classes; compared with the prover's lists (explicit maps).
import sys, os, subprocess, json, glob
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..'); sys.argv_s = list(sys.argv); sys.argv = ['x', '0']
exec(open(os.path.join(H, 'bliss_classify.py')).read().split("nv = int(sys.argv[1])")[0]); sys.argv = sys.argv_s
def g6_edges(line):
    b = [ord(c) - 63 for c in line.strip()]
    if b[0] > 62: raise ValueError('n>62')
    nn = b[0]; bits = []
    for x in b[1:]:
        for k in range(5, -1, -1): bits.append((x >> k) & 1)
    E = []; p = 0
    for j in range(1, nn):
        for i in range(j):
            if bits[p]: E.append((i, j))
            p += 1
    return nn, E
def check(n, m, t, D, tmo):
    fin = os.path.join(R, 'out', 'gb_%d_%d_%d_%d.txt' % (n, m, t, D))
    try:
        g = subprocess.run(['nice', '-n', '5', os.path.join(R, 'out', 'genbg'), '-q', '-c', '-Z1', '-d1:3', '-D%d:3' % D, str(n), str(m), '%d:%d' % (3 * m, 3 * m)],
                           capture_output=True, text=True, timeout=tmo).stdout.splitlines()
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
    with open(fin, 'w') as f:
        for l in g:
            nn, E = g6_edges(l); assert nn == n + m
            nb = {}
            for a, c in E:
                assert a < n <= c, 'not bipartite in the expected order'
                nb.setdefault(c, []).append(a)
            assert len(nb) == m and all(len(x) == 3 for x in nb.values())
            f.write('%d ' % m + ' '.join('%d %d %d' % tuple(sorted(x)) for x in nb.values()) + '\n')
    out = subprocess.run(['nice', '-n', '5', os.path.join(R, 'out', 'fr'), str(n), 'print'], stdin=open(fin), capture_output=True, text=True).stdout.splitlines()
    os.remove(fin)
    keep = []
    for l in out:
        if not l.startswith('SURV'): continue
        f = dict(kv.split('=') for kv in l.split(':')[0].split()[1:])
        if f['conn'] == '1' and int(f['tau']) == t and int(f['maxdeg']) <= D:
            a = list(map(int, l.split(':', 1)[1].split())); keep.append([tuple(a[1 + 3 * i:4 + 3 * i]) for i in range(a[0])])
    mine = {}
    for E in keep:
        k, p = canon(n, E); mine.setdefault(k, (E, p))
    fn = os.path.join(R, 'out', 'cells_x', 'cells', 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    prov = [parse(l) for l in open(fn) if l.startswith('FOUND')]
    pk = {}
    for E in prov:
        k, p = canon(n, E); pk.setdefault(k, (E, p))
    ok = set(mine) == set(pk) and len(pk) == len(prov) and all(verify_map(n, mine[k][0], mine[k][1], pk[k][0], pk[k][1]) for k in mine)
    return 'genbg %d graphs, in cell %d -> %d classes; prover %d; EQUAL=%s' % (len(g), len(keep), len(mine), len(prov), ok)
cells = []
for fn in sorted(glob.glob(os.path.join(R, 'out', 'cells_x', 'cells', 'cell_*.txt'))):
    info = [json.loads(l[5:]) for l in open(fn) if l.startswith('INFO ')][0]
    if info['route'] != 'direct': continue
    cells.append(tuple(int(x) for x in os.path.basename(fn)[5:-4].replace('D', '').split('_')))
tmo = int(sys.argv[1]) if len(sys.argv) > 1 else 120
sel = cells if len(sys.argv) <= 2 else [c for c in cells if '%d_%d_%d_%d' % c in sys.argv[2:]]
for c in sorted(sel, key=lambda c: (c[0] + c[1], c)):
    n, m, t, D = c
    if 3 * m > D * n: print(c, 'trivially empty (3m > D n); prover count', sum(1 for l in open(os.path.join(R, 'out', 'cells_x', 'cells', 'cell_%d_%d_%d_D%d.txt' % c)) if l.startswith('FOUND')), flush=True); continue
    print(c, check(n, m, t, D, tmo), flush=True)
print('ALLDONE')
