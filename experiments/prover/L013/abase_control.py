"""(L013, prover) Positive control (e): the AP hypergraphs of A_base and of all 2,910 saturated extremal 14-point classes (L004 census,
data/census_n14_m12_classes.jsonl.gz) are recomputed from the point sets (3-APs a<b<c with a+c=2b; vertex i = i-th smallest point),
re-verified in C with tau = 6 (pure Python, check_cells.verify), canonicalised by bin/canon and looked up in the engine's list
cell(14,12,6,4) (computed by the recursion in out/cells_D4).  Usage: python3 abase_control.py"""
import os, sys, gzip, json, subprocess, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from check_cells import verify, parse_edges
def ap_pattern(A):
    A = sorted(A); idx = {a: i for i, a in enumerate(A)}; S = set(A)
    return [(idx[a], idx[(a + c) // 2], idx[c]) for a, c in itertools.combinations(A, 2) if (a + c) % 2 == 0 and (a + c) // 2 in S]
def canon(graphs, n):
    lines = ['%d ' % len(E) + ' '.join('%d %d %d' % e for e in E) for E in graphs]
    out = subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
    return [tuple(tuple(map(int, p.split('.'))) for p in l.split()[2:]) for l in out]
cellf = os.path.join(HERE, 'out', 'cells_D4', 'cell_14_12_6_D4.txt')
reps = [tuple(parse_edges(l)) for l in open(cellf) if l.startswith('FOUND:')]
Ab = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
P = ap_pattern(Ab); l012 = parse_edges(open(os.path.join(HERE, '..', 'L012', 'abase_pattern.txt')).read())
print('A_base: %d APs; equal to L012/abase_pattern.txt: %s; verify in C with (14,12,6,Delta<=4): %s' % (len(P), sorted(P) == sorted(l012), verify(P, 14, 12, 6, 4) or 'OK'))
c = canon([P], 14)[0]; print('A_base pattern in cell(14,12,6,4) (%d classes): %s (class index %s)' % (len(reps), c in reps, reps.index(c) if c in reps else None))
rows = [json.loads(l) for l in gzip.open(os.path.join(HERE, '..', '..', '..', 'data', 'census_n14_m12_classes.jsonl.gz'), 'rt')]
pats = [ap_pattern(r['set']) for r in rows]
same = sum(1 for r, p in zip(rows, pats) if sorted(map(tuple, (sorted(e) for e in r['edges']))) == sorted(tuple(sorted(e)) for e in p))
bad = [i for i, p in enumerate(pats) if verify(p, 14, 12, 6, 4)]
cs = canon(pats, 14); inn = sum(1 for x in cs if x in reps); occ = sorted(set(reps.index(x) for x in cs if x in reps))
print('census: %d sets; recomputed AP patterns equal to the stored edges: %d; failing verify (C, tau=6, Delta<=4): %d; patterns found in cell(14,12,6,4): %d; classes of the cell that occur: %d of %d %s'
      % (len(rows), same, len(bad), inn, len(occ), len(reps), occ))
