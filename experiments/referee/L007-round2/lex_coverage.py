"""Class coverage of the (d0 + lex-leader) symmetry break: enumerate ALL solutions of a cell with blocking clauses and
check that every isomorphism class of the authors' enumerator output (conn_dfs2_all) is represented."""
import sys, subprocess, re, json
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
out = {}
for arg in sys.argv[1:]:
    n, m, t, D = map(int, arg.split(','))
    txt = subprocess.run(['./rerun/conn_dfs2_all', str(n), str(m), str(t), str(D)], capture_output=True, text=True).stdout
    auth = [[tuple(sorted(map(int, q.split(',')))) for q in re.findall(r'\(([0-9,]+)\)', l)] for l in txt.splitlines() if l.startswith('FOUND:')]
    for lex in ((False, True) if n <= 10 else (True,)):
        col = []
        solve_cell(n, m, t, D=(D if D < 100 else None), conn='eager', lexleader=lex, collect=col)
        A = classes(auth); B = classes([e for _, e in col])
        covered = all(any(h1 == h2 and nx.is_isomorphic(G1, G2, node_match=nm) for h2, G2 in B) for h1, G1 in A)
        extra = all(any(h1 == h2 and nx.is_isomorphic(G1, G2, node_match=nm) for h2, G2 in A) for h1, G1 in B)
        out['%s lex=%s' % (arg, lex)] = dict(sat_solutions=len(col), sat_classes=len(B), authors_outputs=len(auth), authors_classes=len(A), all_author_classes_covered=covered, no_extra_classes=extra)
        print(arg, 'lex' if lex else 'nolex', out['%s lex=%s' % (arg, lex)], flush=True)
json.dump(out, open('lex_coverage.json', 'w'), indent=1)
