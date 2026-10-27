#!/usr/bin/env python3
"""Referee #3: check |E| <= 3*nu + floor(nu/2) (Chvatal-Hanson for Delta <= 3, as quoted in L017 Thm 7 / 4.6(c)) and
11*nu >= 3|E| with equality only for |E| = 0, on graph6 input (geng -D3).  nu by networkx maximum-cardinality matching."""
import sys, networkx as nx
cnt = 0; viol = 0; viol11 = 0; eq = {}
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    G = nx.from_graph6_bytes(line.encode()); cnt += 1
    M = G.number_of_edges(); nu = len(nx.max_weight_matching(G, maxcardinality=True))
    if M > 3 * nu + nu // 2: viol += 1; print('CH VIOLATION', line, M, nu)
    if 11 * nu < 3 * M or (M > 0 and 11 * nu == 3 * M): viol11 += 1; print('11nu VIOLATION', line, M, nu)
    if M == 3 * nu + nu // 2 and M > 0:
        eq[nu] = eq.get(nu, 0) + 1
print('graphs', cnt, 'CH violations', viol, '11nu>=3M violations', viol11, 'CH-equality counts by nu', dict(sorted(eq.items())))
