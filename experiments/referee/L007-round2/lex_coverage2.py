"""Class coverage of the lex-leader symmetry break on (14,11,>=6,Delta<=3) against the stored 998-graph list
(rerun/mine_14_11_6_deg3.txt, my re-run of enum_conn), and on (11,7,>=4) against conn_dfs2_all."""
import re, json, subprocess
import networkx as nx
from sat_ref import solve_cell
from f7_ref import inc
nm = lambda a, b: a['t'] == b['t']
def classes(lst):
    reps = []
    for es in lst:
        G = inc(es); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t')
        if not any(h == h2 and nx.is_isomorphic(G, G2, node_match=nm) for h2, G2 in reps): reps.append((h, G))
    return reps
def parse_txt(txt):
    return [[tuple(sorted(map(int, q.split(',')))) for q in re.findall(r'\(([0-9,]+)\)', l)] for l in txt.splitlines() if l.startswith('FOUND:')]
out = {}
for (n, m, t, D, src) in [(14, 11, 6, 3, 'rerun/mine_14_11_6_deg3.txt'), (11, 7, 4, 100, None)]:
    auth = parse_txt(open(src).read()) if src else parse_txt(subprocess.run(['./rerun/conn_dfs2_all', str(n), str(m), str(t), str(D)], capture_output=True, text=True).stdout)
    col = []
    solve_cell(n, m, t, D=(D if D < 100 else None), conn='eager', lexleader=True, collect=col, d0s=([3] if n == 14 else None))
    A = classes(auth); B = classes([e for _, e in col])
    cov = all(any(h1 == h2 and nx.is_isomorphic(G1, G2, node_match=nm) for h2, G2 in B) for h1, G1 in A)
    ext = all(any(h1 == h2 and nx.is_isomorphic(G1, G2, node_match=nm) for h2, G2 in A) for h1, G1 in B)
    key = '%d,%d,%d,%d' % (n, m, t, D)
    out[key] = dict(sat_solutions=len(col), sat_classes=len(B), authors_outputs=len(auth), authors_classes=len(A), all_author_classes_covered=cov, no_extra_classes=ext)
    print(key, out[key], flush=True)
json.dump(out, open('lex_coverage2.json', 'w'), indent=1)
