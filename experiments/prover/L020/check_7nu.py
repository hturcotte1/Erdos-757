"""L020 check of 7 nu(G) >= 2|E(G)| (Theorem 2) on all graphs with maximum degree <= 3 and N <= 11 vertices
(nauty geng -D3, graph6 on stdin); prints the number of graphs, failures, and the equality cases with |E| > 0."""
import sys, networkx as nx
cnt = 0; fail = 0; eq = []; mn = None
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    G = nx.from_graph6_bytes(line.encode())
    M = G.number_of_edges(); nu = len(nx.max_weight_matching(G, maxcardinality=True))
    cnt += 1
    if 7 * nu < 2 * M: fail += 1
    if M > 0 and 7 * nu == 2 * M: eq.append(line)
print('graphs', cnt, 'failures', fail, 'equality cases with |E|>0:', len(eq), eq[:10])
