"""(L023) The 8-vertex configuration H8: two vertices a, b with three edges each whose six other vertices coincide
(by linearity the two link matchings then form a hexagon): edges {a,c1,c2},{a,c3,c4},{a,c5,c6},{b,c2,c3},{b,c4,c5},{b,c6,c1}.
(1) H8 is in C; realize_sdr: no 8-point (4,5)-set has these 6 APs (all injective labellings fail).
(2) Every X_i contains H8 (search over pairs a, b and triples of edges at each).
(3) Falsification test on real data: no AP hypergraph of the 2,910 saturated extremal 14-point classes (data/census_n14_m12_classes.jsonl.gz),
    of A_base, of C006 or of C25 contains H8."""
import sys, re, json, gzip, itertools
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from realize_sdr import decide
from verify_c import in_C
from e757.core import ap_edges
H8 = [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 7, 2)]
print('H8 edges', H8, 'in C:', in_C(H8, 8))
st, ex = decide(H8, 8)
print('H8 realize_sdr:', 'REALIZABLE' if st['REAL'] else 'NOT-REALIZABLE', json.dumps(st))
def contains_h8(E, n):
    inc = [[] for _ in range(n)]
    for e in E:
        for v in e: inc[v].append(frozenset(e))
    occ = []
    for a in range(n):
        if len(inc[a]) < 3: continue
        for ea in itertools.combinations(inc[a], 3):
            La = set().union(*ea) - {a}
            if len(La) != 6: continue
            for b in range(n):
                if b == a or b in La or len(inc[b]) < 3: continue
                for eb in itertools.combinations(inc[b], 3):
                    if set().union(*eb) - {b} == La: occ.append((a, b, sorted(map(sorted, ea)), sorted(map(sorted, eb))))
    return occ
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
for gi, E in enumerate(parse(l) for l in open('cell_25_23_11_D4.txt') if l.startswith('FOUND:')):
    occ = contains_h8(E, 25)
    print('X_%d contains H8: %s (%d occurrences as ordered pairs (a,b)); first: %s' % (gi, bool(occ), len(occ), occ[0] if occ else None))
cnt = hit = 0
for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt'):
    r = json.loads(l); cnt += 1
    if contains_h8([tuple(e) for e in r['edges']], r['n']): hit += 1
print('census 14-point saturated extremal classes: %d, containing H8: %d' % (cnt, hit))
def from_set(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [tuple(sorted(idx[v] for v in e)) for e in ap_edges(A)], len(A)
ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
C006 = json.load(open('/home/user/Erdos-757/results/claims/C006-tight-21pt-h12.json'))['set']
C25 = json.load(open('c25_set.json'))
for name, S in (('A_base', ABASE), ('C006', C006), ('C25', C25)):
    E, n = from_set(S); print('%s contains H8: %s' % (name, bool(contains_h8(E, n))))
