"""Explain the P<0 found when Delta=4 subsets were (wrongly) included: list induced subgraphs of the A_base AP hypergraph
with a vertex of degree 4 and A + DEF < 0 (KT^{L*} is a statement about C_3 only; L021 Theorem 1(a) handles Delta >= 4)."""
from itertools import combinations
import kt_data_check as K  # runs the main check on import
from rlib import degs, min_transversals
S = K.bases['14']; Eall = K.ap_edges(S); n0 = len(S)
found = 0
for k in range(3, n0 + 1):
    for Vs in combinations(range(n0), k):
        Ei = K.induced(Eall, Vs)
        loc = {x: i for i, x in enumerate(Vs)}
        El = [tuple(sorted(loc[x] for x in e)) for e in Ei]
        if not El or max(degs(k, El)) <= 3:
            continue
        t, _ = min_transversals(k, El)
        A = 27 * k + 35 * len(El) - 132 * t
        if A < 0:
            d, nc = K.DEF(k, El)
            if A + d < 0:
                found += 1
                if found <= 3:
                    print('Delta4 subset', [S[i] for i in Vs], '(n,m,tau)', (k, len(El), t), 'A', A, 'DEF', d, 'P', A + d)
print('Delta-4 induced subgraphs of A_base with P < 0:', found)
