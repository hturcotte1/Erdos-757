"""Spot check of L019 Theorem 3 (pair-pair coverage), Theorem 4(a),(d) and Lemma 7 in the hereditary class
L' = {linear, F7-free 3-graphs}, where the setting of C1 is NOT vacuous: the first violators of I11 in L' have 9 vertices
(the two (9,8,4) graphs; I11 holds in L' up to 8 vertices by the round-1 opus enumeration of all labelled linear
3-graphs on 8 vertices).  The proofs of Theorems 1-4 and Lemma 7 use only heredity, linearity and 0.8, so they apply
verbatim in L' with N = 8.
Part A: find all 8-edge subsets of AG(2,3) and random linear 3-graphs on 9 vertices that are violators in L'.
Part B: for each violator H and each degree-3 vertex v with H-v connected, F = H-v and the co-vertex pairs: check
  s(F) <= 1; Theorem 3 (some minimum transversal of F meets P_i and P_j, every i<j); Theorem 4(a) (no minimum transversal
  meets all three; tau(H) = tau(F)+1; s(H) = s(F)-2); Theorem 4(d); Lemma 7 (every instance).
Part C: Theorem 2(ii) with k = 2 directly: for sampled F in L' with 8 vertices and slack <= 1 and every pair of disjoint
  pairs Q1,Q2 with F+w(Q1,Q2) in L', some minimum transversal of F meets Q1 and Q2."""
import itertools, random, collections
from ref2 import *


def inLp(E):
    return is_linear(E) and not f7_copies(E)


def connected(V, E):
    V = list(V)
    if not V:
        return True
    seen = {V[0]}
    stack = [V[0]]
    while stack:
        a = stack.pop()
        for e in E:
            if a in e:
                for b in e:
                    if b not in seen:
                        seen.add(b)
                        stack.append(b)
    return seen == set(V)


def canon(E, n):
    # cheap invariant-based dedup key (not a full canonical form): sorted degree sequence + edge-degree profile
    d = degrees(range(n), E)
    return (tuple(sorted(d.values())), tuple(sorted(tuple(sorted(d[x] for x in e)) for e in E)))


st = collections.Counter()
viol = {}
# Part A1: 8-edge subsets of AG(2,3)
pts = [(a, b) for a in range(3) for b in range(3)]
lines = set()
for p in pts:
    for dv in [(0, 1), (1, 0), (1, 1), (1, 2)]:
        lines.add(frozenset(3 * ((p[0] + k * dv[0]) % 3) + (p[1] + k * dv[1]) % 3 for k in range(3)))
AG = sorted(lines, key=sorted)
for sub in itertools.combinations(AG, 8):
    E = list(sub)
    if not inLp(E):
        continue
    t, _ = all_min_T(range(9), E)
    if slack(9, 8, t) < 0:
        viol.setdefault(canon(E, 9), E)
        st['AG_subsets_violating'] += 1
print('Part A1: 8-line subsets of AG(2,3) in L\' violating I11:', st['AG_subsets_violating'], 'invariant classes', len(viol))
# Part A2: random linear 3-graphs on 9 vertices with 8 edges
rng = random.Random(2026)
for _ in range(20000):
    E = []
    pairs = set()
    for _ in range(400):
        e = frozenset(rng.sample(range(9), 3))
        ps = set(itertools.combinations(sorted(e), 2))
        if ps & pairs:
            continue
        E.append(e)
        pairs |= ps
        if len(E) == 8:
            break
    if len(E) != 8 or f7_copies(E):
        continue
    t, _ = all_min_T(range(9), E)
    if slack(9, 8, t) < 0:
        st['random_violators'] += 1
        viol.setdefault(canon(E, 9), E)
print('Part A2: random violators found', st['random_violators'], '; invariant classes overall', len(viol))

# Part B
for key, H in viol.items():
    V = list(range(9))
    tH, TH = all_min_T(V, H)
    sH = slack(9, len(H), tH)
    dH = degrees(V, H)
    print('violator', sorted(map(sorted, H)), 'tau', tH, 'slack', sH, 'degrees', sorted(dH.values()))
    for v in V:
        if dH[v] != 3:
            continue
        F = [e for e in H if v not in e]
        VF = [x for x in V if x != v]
        if not connected(VF, F):
            st['v_with_F_disconnected'] += 1
            continue
        P = [tuple(sorted(e - {v})) for e in H if v in e]
        tF, TF = all_min_T(VF, F)
        sF = slack(8, len(F), tF)
        st['instances'] += 1
        if sF > 1:
            st['FAIL_sF'] += 1
        meets = lambda T, p: bool(T & set(p))
        # Theorem 4(a)
        if any(all(meets(T, p) for p in P) for T in TF):
            st['FAIL_4a_C1_holds_but_H_violator'] += 1
        if tH != tF + 1 or sH != sF - 2:
            st['FAIL_4a_counts'] += 1
        for i, j in itertools.combinations(range(3), 2):
            k = 3 - i - j
            Tij = [T for T in TF if meets(T, P[i]) and meets(T, P[j])]
            if not Tij:
                st['FAIL_thm3'] += 1
            if any(meets(T, P[k]) for T in Tij):
                st['FAIL_4d'] += 1
            # Lemma 7
            for T in Tij:
                for t in P[k]:
                    for g in F:
                        if t not in g or len(g & T) != 1:
                            continue
                        (y,) = tuple(g & T)
                        private = [h for h in F if (h & T) == {y}]
                        if private == [g]:
                            st['lemma7_instances'] += 1
                            if not (T & set(P[i]) == {y} or T & set(P[j]) == {y}):
                                st['FAIL_lemma7'] += 1
print('Part B', {k: v for k, v in sorted(st.items())})

# Part C: Theorem 2(ii), k = 2, N = 8, in L'
stc = collections.Counter()
seenF = set()
for _ in range(4000):
    E = []
    pairs = set()
    for _ in range(300):
        e = frozenset(rng.sample(range(8), 3))
        ps = set(itertools.combinations(sorted(e), 2))
        if ps & pairs:
            continue
        E.append(e)
        pairs |= ps
        if len(E) == 5:
            break
    if len(E) != 5 or f7_copies(E):
        continue
    t, TF = all_min_T(range(8), E)
    if slack(8, 5, t) > 1:
        continue
    stc['F_samples_slack<=1'] += 1
    seenF.add(canon(E, 8))
    nonedge = [p for p in itertools.combinations(range(8), 2) if p not in pairs]
    for Q1, Q2 in itertools.combinations(nonedge, 2):
        if set(Q1) & set(Q2):
            continue
        G = E + [frozenset((8,) + Q1), frozenset((8,) + Q2)]
        if not inLp(G):
            stc['gadget_not_in_Lp'] += 1
            continue
        stc['gadgets_in_Lp'] += 1
        if not any(T & set(Q1) and T & set(Q2) for T in TF):
            stc['FAIL_thm2ii'] += 1
print('Part C', dict(stc), 'invariant classes of F sampled', len(seenF))
fails = [k for d in (st, stc) for k, v in d.items() if k.startswith('FAIL') and v]
print('FAILURES:', fails or 0)
