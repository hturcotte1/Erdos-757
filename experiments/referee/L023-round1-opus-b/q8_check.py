"""Referee L023 (opus-b): Proposition 6 / Theorem 3 via Q8, own code only (imports only realize_own.py of this folder).
 1. parse X_0..X_5 from the certificate text; compare with the worker's exported list and the prover's JSON (as edge sets);
 2. Q8 in C (linear, F7-free, (P3) by brute force over all vertex subsets);
 3. Q8 not realizable: (a) all 3^6 = 729 midpoint assignments, each leaf checked for forced EQ/SIDON/NONLIN (no pruning);
    (b) pruned DFS; (c) the number of injective midpoint labellings (certificate: 95);
 4. for every X_i: all copies of Q8 (pairs a,b with 3 edges each whose 6 other vertices coincide), with an explicit embedding
    of the standard Q8 checked edge by edge."""
import re, json, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from realize_own import decide, count_injective_labellings
from q8lib import q8_copies

ROOT = '/home/user/Erdos-757'
txt = open(ROOT + '/results/proofs/L023-f25-equals-15.md').read()
X = []
for line in txt.splitlines():
    m = re.match(r'X_(\d) FOUND: (.*)$', line)
    if m:
        X.append([tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', m.group(2))])
assert len(X) == 6, len(X)
# compare with the exported list and the JSON
lst = [l for l in open(ROOT + '/experiments/20261027-0340-induction-n28-n29-f25/lists/cell_25_23_11_D4.txt') if l.startswith('FOUND')]
Lw = [[tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in lst]
J = json.load(open(ROOT + '/experiments/prover/L023/six_classes_25_23_11_D4.json'))['classes']
Lj = [[tuple(e) for e in c] for c in J]
norm = lambda L: sorted(sorted(tuple(sorted(e)) for e in c) for c in L)
print('certificate text: %d graphs; equal to worker list: %s; equal to prover JSON: %s' % (len(X), norm(X) == norm(Lw), norm(X) == norm(Lj)))
json.dump({'X%d' % i: X[i] for i in range(6)}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'six_from_text.json'), 'w'))

def linear(E):
    for e, f in itertools.combinations(E, 2):
        if len(set(e) & set(f)) >= 2: return False
    return True
def has_F7(E):
    # F7 = {012,034,056,135,246}: a centre with three edges {c,x1,x2},{c,x3,x4},{c,x5,x6} (disjoint pairs) and two further edges, each
    # meeting each of the three pairs in exactly one vertex, the two using complementary vertices.  Brute force over 5-edge subsets
    # with 7 vertices is used instead of the description (independent of it):
    F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
    F7s = set(frozenset(e) for e in F7)
    Es = [frozenset(e) for e in E]
    for sub in itertools.combinations(Es, 5):
        V = sorted(set().union(*sub))
        if len(V) != 7: continue
        S = set(sub)
        for perm in itertools.permutations(V):
            mp = dict(zip(perm, range(7)))
            if all(frozenset(mp[v] for v in e) in F7s for e in sub): return True
    return False
def P3(E, V):
    for r in range(2, len(V) + 1):
        for S in itertools.combinations(V, r):
            Ss = set(S)
            if sum(1 for e in E if set(e) <= Ss) > r - 2: return False
    return True

# standard Q8: a=0, b=1, c1..c6 = 2..7
a, b = 0, 1; c = [None, 2, 3, 4, 5, 6, 7]
Q8 = [(a, c[1], c[2]), (a, c[3], c[4]), (a, c[5], c[6]), (b, c[2], c[3]), (b, c[4], c[5]), (b, c[6], c[1])]
print('Q8 edges', Q8)
print('Q8 linear', linear(Q8), 'F7-free', not has_F7(Q8), '(P3) all subsets', P3(Q8, list(range(8))))
st, sols = decide(Q8, 8, prune=False, stop_at_first=False)
print('Q8 exhaustive 3^6 leaves: realizable leaves %d; stats %s' % (len(sols), json.dumps(st)))
st2, sols2 = decide(Q8, 8, prune=True, stop_at_first=False)
print('Q8 pruned DFS: realizable leaves %d; stats %s' % (len(sols2), json.dumps(st2)))
print('Q8 injective midpoint labellings:', count_injective_labellings(Q8))
# sanity: a realizable 8-point relative: drop one edge of Q8 (5 edges) must be realizable? (not claimed; reported only)
for drop in range(6):
    E5 = [e for i, e in enumerate(Q8) if i != drop]
    st5, s5 = decide(E5, 8, prune=True, stop_at_first=True)
    print('  Q8 minus edge %d: %s (witness is (4,5): %s)' % (drop, 'REALIZABLE' if s5 else 'NOT-REALIZABLE', (s5[0][1] is not None) if s5 else '-'))

for i, E in enumerate(X):
    cps = q8_copies(E)
    pairs = sorted(set((A, B) for A, B, _, _ in cps))
    print('X_%d: Q8 copies (ordered pairs a,b): %d %s; first embedding a=%d b=%d c1..c6=%s edges %s' % (i, len(pairs), pairs, cps[0][0], cps[0][1], cps[0][2], cps[0][3]))
