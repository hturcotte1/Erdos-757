"""Referee round 2, L017: independent enumeration of the Hall-deficient distributions of the six co-vertices
of a degree-3 vertex v over the r components of G = H - v (Theorem 4(iii)).  Pairs P1={0,1}, P2={2,3}, P3={4,5};
a distribution is a surjective map co-vertex -> component (every component is met, Theorem 4(ii)).
Hall-deficient = no matching of the three pairs into distinct components (checked by brute force) = Hall's
condition violated (checked separately; the two must agree)."""
import itertools
def neighbours(assign):
    return [frozenset(assign[2*j:2*j+2]) for j in range(3)]
def has_saturating_matching(assign, r):
    N = neighbours(assign)
    return any(all(phi[j] in N[j] for j in range(3)) for phi in itertools.permutations(range(r), 3))
def hall_violated(assign):
    N = neighbours(assign)
    return any(len(frozenset().union(*[N[j] for j in J])) < k for k in (1, 2, 3) for J in itertools.combinations(range(3), k))
def canon(assign):
    best = None
    for pp in itertools.permutations(range(3)):
        for sw in itertools.product((0, 1), repeat=3):
            seq = []
            for j in pp:
                a, b = assign[2*j], assign[2*j+1]
                if sw[j]: a, b = b, a
                seq += [a, b]
            mp = {}; out = []
            for c in seq:
                if c not in mp: mp[c] = len(mp)
                out.append(mp[c])
            t = tuple(out)
            if best is None or t < best: best = t
    return best
def describe(c):
    return ' '.join(('P%d in F%d' % (j+1, c[2*j]+1)) if c[2*j] == c[2*j+1] else ('P%d split(F%d,F%d)' % (j+1, c[2*j]+1, c[2*j+1]+1)) for j in range(3))
grand = 0
for r in range(1, 7):
    pats = {}; nd = 0; tot = 0
    for assign in itertools.product(range(r), repeat=6):
        if len(set(assign)) != r: continue
        tot += 1
        hv = hall_violated(assign); hm = has_saturating_matching(assign, r)
        assert hv == (not hm), (assign, hv, hm)
        if hv:
            nd += 1; c = canon(assign); pats[c] = pats.get(c, 0) + 1
    print('r=%d: %d surjective distributions, %d Hall-deficient, %d patterns up to symmetry' % (r, tot, nd, len(pats)))
    for c in sorted(pats): print('    %s   [%d labelled distributions]' % (describe(c), pats[c]))
    grand += len(pats)
print('TOTAL Hall-deficient patterns:', grand, '(certificate: 7 = (a) r=1; (b),(c1),(c2),(e),(f) r=2; (d) r=3)')
