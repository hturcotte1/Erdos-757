"""(L023) Positive and negative controls for realize_sdr.py (the independent exact realizability test).
 (a) sets: A_base (14 points) and the judged 21-point set C006: AP hypergraph on the sorted indices; decide();
     the true midpoint labelling must be among the REAL labellings and its solution must be the set itself after x -> (x - min)/(max - min).
 (b) graph lists: every class of a list, compared with rexact's verdicts (file of 'RES idx REAL|NOT' lines or rexact.py JSON).
usage: python3 ctl_realize.py sets | python3 ctl_realize.py list CELLFILE VERDICTS idx1,idx2,...|all"""
import sys, json, re, time
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from realize_sdr import decide, solve, classify, parse, labellings
from e757.core import ap_edges, is_45_set
def from_set(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    aps = ap_edges(A)
    E = [tuple(sorted((idx[a], idx[b], idx[c]))) for a, b, c in aps]
    mids = {tuple(sorted((idx[a], idx[b], idx[c]))): idx[b] for a, b, c in aps}
    return A, E, mids
if sys.argv[1] == 'sets':
    ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    C006 = json.load(open('/home/user/Erdos-757/results/claims/C006-tight-21pt-h12.json'))['set']
    for name, S in (('A_base', ABASE), ('C006', C006)):
        A, E, mids = from_set(S); n = len(A)
        assert is_45_set(A) and len(E) == n - 2
        t0 = time.time(); st, ex = decide(E, n)
        true = tuple(mids[e] for e in E)
        x = solve(E, n, true); k = classify(x, E, n)
        lo, hi = A[0], A[-1]
        norm = [Fr(a - lo, hi - lo) for a in A]
        print('SET %s n=%d m=%d %s %s true_labelling=%s solution_equals_normalized_set=%s secs=%.1f' % (
            name, n, len(E), 'REALIZABLE' if st['REAL'] else 'NOT-REALIZABLE', json.dumps(st), k, x == norm, time.time() - t0), flush=True)
else:
    cellfile, verd, sel = sys.argv[2], sys.argv[3], sys.argv[4]
    graphs = [parse(l) for l in open(cellfile) if l.startswith('FOUND:')]
    V = {}
    if verd.endswith('.json'):
        for r in json.load(open(verd)): V[r['cls']] = 'REAL' if r['realizable'] else 'NOT'
    else:
        for l in open(verd):
            if l.startswith('RES'): p = l.split(); V[int(p[1])] = p[2]
    idxs = range(len(graphs)) if sel == 'all' else [int(s) for s in sel.split(',')]
    agree = dis = 0
    for i in idxs:
        E = graphs[i]; n = 1 + max(max(e) for e in E); assert len(E) == n - 2
        t0 = time.time(); st, ex = decide(E, n)
        mine = 'REAL' if st['REAL'] else 'NOT'
        ok = (mine == V.get(i)); agree += ok; dis += (not ok)
        extra = ''
        if ex:
            from realize_sdr import to_int_set
            s = sorted(to_int_set(ex[0][1])); extra = ' example_is_45=%s num_aps=%d' % (is_45_set(s), len(ap_edges(s)))
        print('CLASS %d n=%d mine=%s rexact=%s %s %s%s secs=%.1f' % (i, n, mine, V.get(i), 'AGREE' if ok else 'DISAGREE', json.dumps(st), extra, time.time() - t0), flush=True)
    print('SUMMARY classes %d agree %d disagree %d' % (agree + dis, agree, dis))
