#!/usr/bin/env python3
"""Exact (Fraction) verification of survivors of filt (2-point maps).  Reads hit lines
'id a b ap bp p q h0 gn Ttyp' for a seed file, re-checks structure for K<=KV (count, weak Sidon, AP set = union of copies,
linear, literal is_45 for K<=2), recomputes the transfer matrix exactly and the slope (iteration to 240), and the
copy-distance bound (phi^d(O) cap O empty for all d>=2 up to the rigorous bound) -> JSON rows."""
import sys, json, math
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261020-2115-selfsimilar-search')
from ss_lib import *

def fixed_point_bound(O, a, b, ap, bp):
    """Return D such that phi^d(O) cap O is empty for every d > D unless a point is the fixed point L (rigorous)."""
    r = F(O[bp] - O[ap], O[b] - O[a])
    L = (F(O[ap]) - r * O[a]) / (1 - r)
    if L in set(O): return None
    dmax = max(abs(F(x) - L) for x in O); dmin = min(abs(F(x) - L) for x in O)
    d = 1
    while abs(r) ** d * dmax >= dmin: d += 1
    return d

def verify(O, a, b, ap, bp, KV=6, literal_upto=2):
    phi, r = make_phi(O, a, b, ap, bp)
    row = {'O': O, 'map': [a, b, ap, bp], 'r': str(r), 'struct': []}
    allok = True
    for K in range(1, KV + 1):
        c = structure_check(O, phi, K, literal=(K <= literal_upto))
        c['ok'] = c['count_ok'] and c['ap_equal'] and c['is_45_fast'] and c.get('is_45_literal', True)
        allok &= c['ok']; row['struct'].append(c)
    best, M, R0 = transfer(O, a, b, ap, bp)
    s, _ = slope(M, R0)
    row.update(best=best, M=M, R0=R0, slope=str(s), limit=str(s / (len(O) - 2)), all_struct_ok=allok,
               h_seq=hseq(M, R0, 8), dbound=fixed_point_bound(O, a, b, ap, bp))
    return row

if __name__ == '__main__':
    O = list(map(int, sys.argv[1].split(','))); a, b, ap, bp = map(int, sys.argv[2:6])
    print(json.dumps(verify(O, a, b, ap, bp), default=str)[:3000])
