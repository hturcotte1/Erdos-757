"""Controls for the F7 detectors and the (P3) tests: named configurations with known answers + random linear 3-graphs
(some with a planted F7), compared across (1) referee ref_filter (definitional bijection F7 test, vertex-subset P3),
(2) prover filter_hits (Lemma F, edge-subset P3), (3) falsifier find_f7 (e757.cpsat_model) and a referee networkx monomorphism test,
(4) Python vertex-subset P3."""
import itertools, random, subprocess, sys, json
sys.path.insert(0, '/home/user/Erdos-757')
from e757.cpsat_model import find_f7
import networkx as nx
from networkx.algorithms import isomorphism as iso
R = '/home/user/Erdos-757/experiments/referee/L008-round1'
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
FANO = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
AG = []  # AG(2,3): points (x,y) in Z3^2 -> 3x+y ; lines
pts = [(x,y) for x in range(3) for y in range(3)]
lines = set()
for a in pts:
    for b in pts:
        if a < b:
            c = ((-a[0]-b[0]) % 3, (-a[1]-b[1]) % 3)
            lines.add(tuple(sorted((3*a[0]+a[1], 3*b[0]+b[1], 3*c[0]+c[1]))))
AG = sorted(lines); assert len(AG) == 12
PASCH = [(0,1,2),(0,3,4),(1,3,5),(2,4,5)]
def ap_pattern(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(idx[a], idx[(a+c)//2], idx[c]) for a, c in itertools.combinations(A, 2) if (a+c) % 2 == 0 and (a+c)//2 in idx]
ABASE = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
C16 = [-323,0,136,200,243,246,249,272,286,298,323,400,528,596,1056,5000]
recs = json.load(open('/home/user/Erdos-757/data/small_records.json'))
def relabel(es, n, N, rng):
    perm = rng.sample(range(N), n); return [tuple(sorted(perm[v] for v in e)) for e in es]
named = []
rng = random.Random(757)
named.append(('F7', F7, True, True))
named.append(('F7 relabelled into 16 vertices', relabel(F7, 7, 16, rng), True, True))
for i in range(5): named.append(('F7 minus edge %d' % i, [e for j, e in enumerate(F7) if j != i], False, True))
named.append(('Fano', FANO, False, False))
named.append(('Fano minus a line', FANO[1:], False, False))
named.append(('AG(2,3)', AG, True, False))
AG8 = [e for e in AG if 8 not in e]
named.append(('AG(2,3) minus a point (8 pts, 8 lines)', AG8, True, False))
named.append(('Pasch', PASCH, False, True))
named.append(('A_base AP pattern', ap_pattern(ABASE), False, True))
named.append(('C16 AP pattern', ap_pattern(C16), False, True))
named.append(('D14 (L007 Step 6.4)', [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)], True, True))
named.append(('13 edges on 13 vertices: A_base pattern on 14 pts plus nothing? -> R12+vertex', None, None, None))
named.pop()
def f7_nx(es):
    # monomorphism of F7's incidence graph into es's incidence graph, colours kept
    def inc(E):
        G = nx.Graph()
        for i, e in enumerate(E):
            G.add_node(('e', i), t=1)
            for v in e: G.add_node(('v', v), t=0); G.add_edge(('e', i), ('v', v))
        return G
    GM = iso.GraphMatcher(inc(es), inc(F7), node_match=lambda a, b: a['t'] == b['t'])
    return GM.subgraph_is_monomorphic()
def p3_py(es):
    vs = sorted(set(v for e in es for v in e)); n = len(vs)
    ms = [sum(1 << vs.index(v) for v in e) for e in es]
    for S in range(1 << n):
        s = bin(S).count('1')
        if s < 2: continue
        k = sum(1 for m in ms if m & S == m)
        if k > s - 2: return False
    return True
def linear(es): return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(es, 2))
def rand_linear(n, m, rng, plant=False):
    es = []
    if plant:
        P = rng.sample(range(n), 7); es = [tuple(sorted(P[v] for v in e)) for e in F7]
    tries = 0
    while len(es) < m and tries < 5000:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        if e in es or any(len(set(e) & set(f)) >= 2 for f in es): continue
        es.append(e)
    return es
for k in range(1500):
    n = rng.randint(7, 13); m = rng.randint(5, min(14, n + 1)); plant = rng.random() < 0.3
    es = rand_linear(n, m, rng, plant)
    named.append(('random %d (n=%d, planted=%s)' % (k, n, plant), es, None, None))
lines_out = []; rows = []
for name, es, f7exp, p3exp in named:
    a = bool(find_f7(es)); b = f7_nx(es); c = p3_py(es); lin = linear(es)
    rows.append((name, es, a, b, c, lin, f7exp, p3exp))
    lines_out.append('HIT: ' + ' '.join('(%d,%d,%d)' % tuple(e) for e in es))
open(R + '/controls/controls.txt', 'w').write('\n'.join(lines_out) + '\n')
mine = [l for l in subprocess.run(R + '/bin/ref_filter HIT < ' + R + '/controls/controls.txt', shell=True, capture_output=True, text=True, env={'VERBOSE': '1'}).stdout.splitlines() if l.startswith('FLAGS')]
assert len(mine) == len(rows)
# prover filter_hits: run per line to get flags (contain_F7 / P3 counts per single-line file)
def prover_flags(es):
    out = subprocess.run(R + '/bin/filter_hits HIT', shell=True, capture_output=True, text=True, input='HIT: ' + ' '.join('(%d,%d,%d)' % tuple(e) for e in es) + '\n').stdout
    s = out.strip().splitlines()[-1]
    f7 = int(s.split('contain_F7=')[1].split()[0]); p3bad = int(s.split('P3_violated=')[1].split()[0])
    return bool(f7), not bool(p3bad)
bad = 0; stats = {'f7': 0, 'p3fail': 0, 'n': 0}
for (name, es, a, b, c, lin, f7exp, p3exp), fl in zip(rows, mine):
    d = dict(x.split('=') for x in fl.split()[1:])
    myf7 = d['f7'] == '1'; myp3 = d['p3'] == '1'; mylin = d['lin'] == '1'
    pf7, pp3 = prover_flags(es)
    ok = (a == b == myf7 == pf7) and (c == myp3 == pp3) and (lin == mylin)
    if f7exp is not None: ok = ok and (myf7 == f7exp) and (myp3 == p3exp)
    stats['n'] += 1; stats['f7'] += myf7; stats['p3fail'] += (not myp3)
    if f7exp is not None or not ok:
        print(('OK  ' if ok else 'BAD ') + '%-45s F7: find_f7=%d nx=%d ref=%d prover=%d | P3: py=%d ref=%d prover=%d | linear=%d' % (name, a, b, myf7, pf7, c, myp3, pp3, lin))
    bad += not ok
print('controls total', stats, 'disagreements/wrong', bad)
