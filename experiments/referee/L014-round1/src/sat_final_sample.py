"""Referee L014 r1: third method for the final step on a sample: for sampled inputs G (22 vertices) every 3-set of pairwise
disjoint admissible pairs is decided by SAT (pysat, Glucose4 + sequential-counter cardinality): tau(H) <= 9 iff some 9-set of
vertices of G covers every edge of G and meets all three pairs.  The hit sets are compared with myext's output.
Also: tau(H) = 10 for every one of myext's 10,986 hits by OR-tools CP-SAT (minimum vertex cover of H).
Usage: python3 sat_final_sample.py top_inputs.txt top_hits.txt SEED"""
import sys, random, itertools
from pysat.solvers import Glucose4
from pysat.card import CardEnc, EncType
from ortools.sat.python import cp_model
INP, HITS, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3])
inputs = [list(map(int, l.split())) for l in open(INP)]
hits = {}
for l in open(HITS):
    if l.startswith('X '):
        a = list(map(int, l.split()[1:])); k = a[0] - 1; v = a[2:]
        new = tuple(sorted(tuple(sorted((v[3*i+1], v[3*i+2]))) for i in range(18, 21)))
        hits.setdefault(k, set()).add(new)
# ranges of the decompositions in the input file order: 94513, 0, 9387, 6, 29898
ranges = [('22,18,9', 0, 94513), ('10,8,4+12,10,5', 94513, 103900), ('8,6,3+14,12,6', 103900, 103906), ('3,1,1+19,17,8', 103906, 133804)]
rng = random.Random(SEED); sample = set()
for name, lo, hi in ranges:
    k = {'22,18,9': 150, '10,8,4+12,10,5': 100, '8,6,3+14,12,6': 6, '3,1,1+19,17,8': 150}[name]
    sample |= set(rng.sample(range(lo, hi), min(k, hi - lo)))
hk = sorted(hits); sample |= set(rng.sample(hk, min(200, len(hk))))
tot_sets = tot_hits = diff = 0
for idx in sorted(sample):
    a = inputs[idx]; m = a[0]; E = [tuple(a[1 + 3*i: 4 + 3*i]) for i in range(m)]
    deg = [0] * 22
    for e in E:
        for v in e: deg[v] += 1
    pairs = [(x, y) for x in range(22) for y in range(x + 1, 22) if deg[x] <= 2 and deg[y] <= 2 and not any(x in e and y in e for e in E)]
    s = Glucose4()
    for e in E: s.add_clause([v + 1 for v in e])
    card = CardEnc.atmost(lits=list(range(1, 23)), bound=9, top_id=22 + len(pairs), encoding=EncType.seqcounter)
    for c in card.clauses: s.add_clause(c)
    sel = {}
    for i, (x, y) in enumerate(pairs):
        sv = 23 + i; sel[(x, y)] = sv; s.add_clause([-sv, x + 1, y + 1])
    assert s.solve(), 'G has no 9-cover?'
    mine = set()
    for t in itertools.combinations(pairs, 3):
        if len(set(t[0]) | set(t[1]) | set(t[2])) < 6: continue
        tot_sets += 1
        if not s.solve(assumptions=[sel[p] for p in t]): mine.add(tuple(sorted(t)))
    s.delete()
    theirs = hits.get(idx, set())
    tot_hits += len(mine)
    if mine != theirs: diff += 1; print('DIFF at input', idx, len(mine), len(theirs))
print('SAT sample: inputs', len(sample), '3-sets decided', tot_sets, 'hits', tot_hits, 'inputs with different hit sets', diff)
# CP-SAT: tau(H) for all hits
bad = 0; n = 0
for l in open(HITS):
    if not l.startswith('X '): continue
    a = list(map(int, l.split()[1:])); v = a[2:]; E = [v[3*i:3*i+3] for i in range(a[1])]
    md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(23)]
    for e in E: md.AddBoolOr([x[u] for u in e])
    md.Minimize(sum(x)); so = cp_model.CpSolver(); so.parameters.num_workers = 1; st = so.Solve(md)
    n += 1
    if so.StatusName(st) != 'OPTIMAL' or int(so.ObjectiveValue()) != 10: bad += 1
print('CP-SAT tau(H) == 10 for', n - bad, 'of', n, 'hits')
