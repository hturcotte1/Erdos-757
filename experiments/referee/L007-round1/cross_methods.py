"""Cross-validate two different canonical methods on non-empty cells with n >= 10: the referee's lex-min enumerator
(ref_enum) and the falsifier's BFS canonical growth (conn_dfs2_all).  Compare the sets of isomorphism classes."""
import sys, subprocess
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L007-round1')
from ref_classes import *
D0 = '/home/user/Erdos-757/experiments/referee/L007-round1/'
for c in sys.argv[1:]:
    n, m, t, D = map(int, c.split(','))
    a = subprocess.run([D0 + 'ref_enum', str(n), str(m), str(t), str(D), '1', '1'], capture_output=True, text=True).stdout
    b = subprocess.run([D0 + 'rerun/conn_dfs2_all', str(n), str(m), str(t), str(D)], capture_output=True, text=True).stdout
    A = parse_lines(a.splitlines(), 'G:'); B = parse_lines(b.splitlines(), 'FOUND:')
    ca = classes(A); cb = classes(B)
    ina = sum(1 for r in ca if any(nx.is_isomorphic(r[2], q[2], node_match=nm) for q in cb if len(q[0]) == len(r[0])))
    inb = sum(1 for q in cb if any(nx.is_isomorphic(q[2], r[2], node_match=nm) for r in ca))
    print('cell', (n, m, t, D), 'ref_enum outputs', len(A), 'classes', len(ca), '| conn_dfs2_all outputs', len(B), 'classes', len(cb),
          '| ref classes in other', ina, '| other classes in ref', inb, 'AGREE' if ina == len(ca) == len(cb) == inb else 'DISAGREE', flush=True)
