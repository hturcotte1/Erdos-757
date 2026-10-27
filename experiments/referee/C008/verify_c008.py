#!/usr/bin/env python3
"""Independent referee verifier for claim C008-f19-h11 (does NOT import e757/ or judge/).

Checks, from the definitions in kb/00_START_HERE.md section 1:
  (1) parsing (integers only, no floats/strings), distinctness, agreement with set_19pt_h11.json;
  (2) (4,5): every 4-subset B has >= 5 distinct absolute differences, i.e. |B-B| >= 11
      -- three ways: brute force; weak Sidon + linear 3-AP hypergraph; coincidence counting;
  (3) h(A) exactly -- four ways: all 2^19 subsets (numpy, obstruction masks built from the
      Sidon definition); direct definition check on all C(19,12) and C(19,11) subsets;
      CP-SAT (OR-tools, 1 worker); SAT with a cardinality constraint (PySAT);
  (4) 3-AP hypergraph: m, midpoints, linearity, F7-freeness (two methods), tau by brute force,
      degrees, connectivity, e(S) <= |S|-2 for all |S| >= 2, Henning-Yeo slack, excess D;
  (5) exact Fractions: 11/19 vs 4/7; the K8 lower bound for n = 19.
"""
import itertools
import json
import sys
from fractions import Fraction
from collections import Counter

import numpy as np

REPO = '/home/user/Erdos-757'
CLAIM = REPO + '/results/claims/C008-f19-h11.json'
SETFILE = REPO + '/experiments/20261027-0815-realize-f19/set_19pt_h11.json'

out = {}
def rep(k, v):
    out[k] = v
    print(f'{k}: {v}', flush=True)

# ---------------------------------------------------------------- (1) parsing
claim = json.load(open(CLAIM))
raw = claim['set']
assert all(type(x) is int for x in raw), 'non-integer entry in set'
A = sorted(raw)
n = len(A)
rep('n', n)
rep('all_int', all(type(x) is int for x in raw))
rep('distinct', len(set(A)) == n)
rep('sorted_as_given', raw == A)
raw2 = json.load(open(SETFILE))
rep('same_as_set_19pt_h11.json', sorted(raw2) == A and len(raw2) == n)
rep('claim_keys', sorted(claim.keys()))
rep('claimed_h', claim.get('claimed_h'))
W = claim['witness_sidon_subset']
assert all(type(x) is int for x in W)
rep('witness_size', len(W))
rep('witness_distinct', len(set(W)) == len(W))
rep('witness_subset_of_A', set(W) <= set(A))

def sidon_by_differences(S):
    S = sorted(S)
    d = [y - x for x, y in itertools.combinations(S, 2)]
    return len(d) == len(set(d))

def sidon_by_sums(S):
    S = sorted(S)
    s = [S[i] + S[j] for i in range(len(S)) for j in range(i, len(S))]  # x <= y, includes 2x
    return len(s) == len(set(s))

rep('witness_sidon_differences', sidon_by_differences(W))
rep('witness_sidon_sums', sidon_by_sums(W))

# ---------------------------------------------------------------- (2) (4,5) property
# (a) brute force over all 4-subsets
min_dist = 99
cnt_by_dist = Counter()
min_BB = 99
for B in itertools.combinations(A, 4):
    dd = {abs(x - y) for x, y in itertools.combinations(B, 2)}
    BB = {x - y for x in B for y in B}   # full difference set, includes 0 and negatives
    cnt_by_dist[len(dd)] += 1
    min_dist = min(min_dist, len(dd))
    min_BB = min(min_BB, len(BB))
rep('num_4subsets', sum(cnt_by_dist.values()))
rep('4subsets_by_num_distances', dict(sorted(cnt_by_dist.items())))
rep('min_distinct_distances_over_4subsets', min_dist)
rep('min_|B-B|_over_4subsets', min_BB)
is45_bf = (min_dist >= 5) and (min_BB >= 11)
rep('is_45_bruteforce', is45_bf)

# 3-APs (a < b < c, a + c = 2b), found by scanning all triples (no hashing shortcut)
idx = {x: i for i, x in enumerate(A)}
APs = []
for i, j, k in itertools.combinations(range(n), 3):
    if A[i] + A[k] == 2 * A[j]:
        APs.append((i, j, k))
m = len(APs)

# (b) weak Sidon (sums x+y, x<y distinct) + linear AP hypergraph
sums = [A[i] + A[j] for i, j in itertools.combinations(range(n), 2)]
weak_sidon = len(sums) == len(set(sums))
linear = all(len(set(e) & set(f)) <= 1 for e, f in itertools.combinations(APs, 2))
rep('weak_sidon', weak_sidon)
rep('AP_hypergraph_linear', linear)
rep('is_45_via_weakSidon_and_linear', weak_sidon and linear)

# (c) coincidence counting: a 4-set fails iff it contains >= 2 pairs-of-pairs with equal distance
pairs = list(itertools.combinations(range(n), 2))
bydiff = {}
for (i, j) in pairs:
    bydiff.setdefault(A[j] - A[i], []).append((i, j))
coinc = []
for d, L in bydiff.items():
    for p, q in itertools.combinations(L, 2):
        coinc.append(frozenset(p) | frozenset(q))
rep('num_equal_distance_pair_pairs', len(coinc))
rep('equal_distance_pair_pairs_union_sizes', dict(Counter(len(u) for u in coinc)))
fails = 0
for B in itertools.combinations(range(n), 4):
    Bs = set(B)
    c = sum(1 for u in coinc if u <= Bs)
    if c >= 2:
        fails += 1
rep('4subsets_with_>=2_coincidences', fails)
rep('is_45_via_coincidences', fails == 0)

# ---------------------------------------------------------------- (3) h(A)
# obstruction masks straight from the definition: S is Sidon iff it contains no union of two
# distinct pairs with equal positive difference
obst = sorted({sum(1 << v for v in u) for u in coinc})
rep('num_obstruction_masks', len(obst))
N = 1 << n
masks = np.arange(N, dtype=np.int64)
bad = np.zeros(N, dtype=bool)
for U in obst:
    bad |= (masks & U) == U
pc = np.bitwise_count(masks.astype(np.uint64)).astype(np.int64)
good_pc = pc[~bad]
h_np = int(good_pc.max())
rep('h_all_2^19_subsets', h_np)
rep('num_sidon_subsets_by_size_all_2^19', {int(k): int(v) for k, v in zip(*np.unique(good_pc, return_counts=True))})
num_max_np = int(np.sum(good_pc == h_np))

# direct definition on all 12- and 11-subsets (pure Python)
n12 = sum(1 for S in itertools.combinations(A, 12) if sidon_by_differences(S))
rep('num_sidon_12_subsets_direct', n12)
max11 = [S for S in itertools.combinations(A, 11) if sidon_by_differences(S)]
rep('num_sidon_11_subsets_direct', len(max11))
rep('witness_among_them', tuple(sorted(W)) in set(max11))
rep('agree_numpy_vs_direct_count', num_max_np == len(max11))
# sanity of the sum definition on all maximum sets
rep('all_11_sets_sidon_by_sums', all(sidon_by_sums(S) for S in max11))

# CP-SAT (one worker)
from ortools.sat.python import cp_model
def cpsat(at_least=None):
    md = cp_model.CpModel()
    x = [md.NewBoolVar(f'x{i}') for i in range(n)]
    for U in obst:
        vs = [i for i in range(n) if U >> i & 1]
        md.Add(sum(x[i] for i in vs) <= len(vs) - 1)
    if at_least is None:
        md.Maximize(sum(x))
    else:
        md.Add(sum(x) >= at_least)
    s = cp_model.CpSolver()
    s.parameters.num_workers = 1
    s.parameters.max_time_in_seconds = 120
    st = s.Solve(md)
    sol = [A[i] for i in range(n) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and s.Value(x[i])]
    return s.StatusName(st), (s.ObjectiveValue() if at_least is None else None), sol
st, obj, sol = cpsat()
rep('cpsat_max_status', st)
rep('cpsat_max_objective', obj)
rep('cpsat_solution_is_sidon', sidon_by_differences(sol))
st12, _, _ = cpsat(12)
rep('cpsat_at_least_12_status', st12)

# PySAT with cardinality encoding
from pysat.card import CardEnc, EncType
from pysat.solvers import Minisat22
def sat_at_least(k):
    cls = []
    for U in obst:
        cls.append([-(i + 1) for i in range(n) if U >> i & 1])
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.seqcounter)
    with Minisat22(bootstrap_with=cls + card.clauses) as s:
        r = s.solve()
        mdl = s.get_model() if r else None
    sol = [A[i] for i in range(n) if mdl and mdl[i] > 0]
    return r, sol
r11, s11 = sat_at_least(11)
r12, _ = sat_at_least(12)
rep('pysat_at_least_11', r11)
rep('pysat_at_least_11_model_sidon', sidon_by_differences(s11) and len(s11) >= 11)
rep('pysat_at_least_12', r12)

h = h_np
rep('h_final', h)
rep('h_equals_claimed', h == claim['claimed_h'] == len(W))

# ---------------------------------------------------------------- (4) AP hypergraph
rep('m_num_3APs', m)
rep('APs_as_values', [(A[i], A[j], A[k]) for i, j, k in APs])
mids = [j for _, j, _ in APs]
rep('midpoints_distinct', len(set(mids)) == m)
rep('min_or_max_is_midpoint', (0 in mids) or (n - 1 in mids))
rep('non_midpoints_sorted_index', [v for v in range(n) if v not in set(mids)])
deg = Counter(v for e in APs for v in e)
degseq = sorted((deg.get(v, 0) for v in range(n)), reverse=True)
rep('degree_sequence', degseq)
rep('max_degree', max(degseq))
rep('degree_histogram', dict(sorted(Counter(degseq).items(), reverse=True)))
# connectivity (union-find)
par = list(range(n))
def f(x):
    while par[x] != x:
        par[x] = par[par[x]]; x = par[x]
    return x
for e in APs:
    for v in e[1:]:
        par[f(v)] = f(e[0])
rep('num_components', len({f(v) for v in range(n)}))
# tau by brute force
def hits(T):
    return all(any(v in T for v in e) for e in APs)
small = [T for k in range(0, 8) for T in itertools.combinations(range(n), k) if hits(set(T))]
rep('num_transversals_size_<=7', len(small))
t8 = [T for T in itertools.combinations(range(n), 8) if hits(set(T))]
rep('num_transversals_size_8', len(t8))
tau = 8 if (not small and t8) else None
rep('tau', tau)
rep('n_minus_tau_equals_h', n - tau == h)
rep('witness_complement_is_transversal', hits({idx[x] for x in A if x not in set(W)}))
# AP-free 11-subsets vs Sidon 11-subsets (Lemma 2.3 consistency)
apfree11 = sum(1 for S in itertools.combinations(range(n), 11)
               if not any(set(e) <= set(S) for e in APs))
rep('num_APfree_11_subsets', apfree11)
rep('APfree_count_equals_Sidon_count', apfree11 == len(max11))
# F7-freeness, method 1: injective homomorphism search
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
Eset = {frozenset(e) for e in APs}
inc = {v: [e for e in APs if v in e] for v in range(n)}
f7_hits = 0
for v in range(n):
    for e1, e2, e3 in itertools.permutations(inc[v], 3):
        o1 = [u for u in e1 if u != v]; o2 = [u for u in e2 if u != v]; o3 = [u for u in e3 if u != v]
        for a in (o1, o1[::-1]):
            for b in (o2, o2[::-1]):
                for c in (o3, o3[::-1]):
                    phi = {0: v, 1: a[0], 2: a[1], 3: b[0], 4: b[1], 5: c[0], 6: c[1]}
                    if len(set(phi.values())) != 7:
                        continue
                    if frozenset((phi[1], phi[3], phi[5])) in Eset and frozenset((phi[2], phi[4], phi[6])) in Eset:
                        f7_hits += 1
rep('F7_copies_by_homomorphism_search', f7_hits)
# F7-freeness, method 2: all 5-edge subsets with 7 vertices, networkx incidence-graph isomorphism
import networkx as nx
def incg(edges):
    G = nx.Graph()
    for t, e in enumerate(edges):
        G.add_node(('e', t), kind='e')
        for v in e:
            G.add_node(('v', v), kind='v')
            G.add_edge(('e', t), ('v', v))
    return G
GF7 = incg(F7)
nm = nx.algorithms.isomorphism.categorical_node_match('kind', None)
f7_sub = 0; cand = 0
for E5 in itertools.combinations(APs, 5):
    if len(set().union(*map(set, E5))) == 7:
        cand += 1
        if nx.is_isomorphic(incg(E5), GF7, node_match=nm):
            f7_sub += 1
rep('5edge_subsets_on_7_vertices', cand)
rep('F7_copies_by_5subset_isomorphism', f7_sub)
rep('F7_free', f7_hits == 0 and f7_sub == 0)
# class-C condition e(S) <= |S| - 2 for all |S| >= 2
e_cnt = np.zeros(N, dtype=np.int16)
for (i, j, k) in APs:
    U = (1 << i) | (1 << j) | (1 << k)
    e_cnt += ((masks & U) == U).astype(np.int16)
viol = int(np.sum((pc >= 2) & (e_cnt > pc - 2)))
rep('eS_le_S_minus_2_violations', viol)
# cell, Henning-Yeo slack and excess
rep('cell_(n,m,tau)', (n, m, tau))
rep('HY_17tau_le_5n_plus_3m', (17 * tau, 5 * n + 3 * m, 17 * tau <= 5 * n + 3 * m))
rep('HY_slack_delta', 5 * n + 3 * m - 17 * tau)
rep('excess_D=17h-9n', 17 * h - 9 * n)
rep('D_equals_delta_plus_3(n-m)', 17 * h - 9 * n == (5 * n + 3 * m - 17 * tau) + 3 * (n - m))

# ---------------------------------------------------------------- (5) fractions, lower bound
r = Fraction(h, n)
rep('ratio', str(r))
rep('ratio_lt_4/7', r < Fraction(4, 7))
rep('ratio_minus_4/7', str(r - Fraction(4, 7)))
# K8 lower bound for every 19-point (4,5)-set: tau <= floor((5n+3m)/17) with m <= n-2
tmax = max((5 * 19 + 3 * mm) // 17 for mm in range(0, 18))
rep('K8_max_tau_n19', tmax)
rep('K8_min_h_n19', 19 - tmax)
rep('(9n+6)/17_n19', str(Fraction(9 * 19 + 6, 17)))
rep('ceil((9n+6)/17)_n19', -((-(9 * 19 + 6)) // 17))

json.dump(out, open(REPO + '/experiments/referee/C008/verify_c008_out.json', 'w'), indent=1, default=str)
print('DONE')
