"""L021 sanity checks: A and DEF (epsilon = 1/6, list L*) on F7, the (9,8,4) violator of
experiments/falsify/i11-inequality, A_base's pattern class (14,12,6), and hypertrees with a perfect matching (k = 0..5)."""
import sys, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
pieces = [Piece(p['edges'], p['name']) for p in R['pieces']]
def report(name, n, edges):
    t = tau_masks(masks(edges)); A = A_value(n, len(edges), t); D = deficiency(n, edges, pieces, proper=False)
    s = 3 * n + 2 * len(edges) - 11 * t; J = 19 * n + 12 * len(edges) - 66 * t
    print(f'{name}: (n,m,tau)=({n},{len(edges)},{t}) I11 slack {s}, J_1/6 slack (x6) {J}, A={A}, DEF={D}, A+DEF={A+D}')
report('F7', 7, [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)])
d = json.load(open('/home/user/Erdos-757/experiments/falsify/i11-inequality/f7free_nonO_violation_9_8_4.json'))
report('(9,8,4) violator', d['n'], [tuple(e) for e in d['edges']])
# hypertrees with perfect matching: chain construction
for k in range(0, 6):
    edges = [(0, 1, 2)]; nv = 3; leaves = [2]
    for i in range(k):
        x = leaves.pop(); y, z = nv, nv + 1; nv += 2
        edges.append((x, y, z))
        edges.append((y, nv, nv + 1)); edges.append((z, nv + 2, nv + 3)); leaves += [nv + 1, nv + 3]; nv += 4
    report(f'hypertree with perfect matching k={k}', nv, edges)
