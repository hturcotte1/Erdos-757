"""Format results.json (from aggregate.py) as markdown tables -> tables.md"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(here, 'results.json')))
cells = sorted(R.items(), key=lambda kv: (kv[1]['slack'], kv[1]['n']))
out = []
def pct(a, b): return 'n/a' if b == 0 else ('%d/%d' % (a, b) if a == b else '%d/%d (%.4f)' % (a, b, a / b))
out.append('### Table 1: classes, transversals, vertex and pair coverage\n')
out.append('| slack | cell (n,m,tau) | D listed | classes (Delta<=3) | Delta range | m<=n-4 | #min transversals min..max | vertices in no min transv. | P2 pairs covered | max key of a P2 failure (bound floor((s+5)/2)) | classes with a P2 failure | pair-pair covered, all disjoint pairs | pair-pair covered, pairs not inside an edge |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for k, r in cells:
    out.append('| %d | (%d,%d,%d) | %d | %d (%d) | %d..%d | %s | %d..%d | %d | %s | %s (%d) | %d | %s | %s |' % (r['slack'], r['n'], r['m'], r['tau'], r['D_listed'], r['classes'], r['classes_deg_le3'], r['maxdeg_range'][0], r['maxdeg_range'][1], 'yes' if r['m_le_n_minus_4'] else 'no', r['nT_min'], r['nT_max'], r['vertices_in_no_min_transversal'],
        pct(r['p2_pairs'] - r['p2_fail'], r['p2_pairs']), r['max_P2_fail_key'], r['P2_bound_floor_s5_2'], r['classes_with_P2_failure'], pct(r['pp_all_cov'], r['pp_all']), pct(r['pp_good_cov'], r['pp_good'])))
out.append('\n### Table 2: triples of three disjoint pairs, extension F+v (v adjacent to the three pairs)\n')
out.append('| slack | cell | triples | admissible (F+v in C) | admissible and uncoverable | adm. with all six d_F=2 (R2): count / uncoverable | adm. with all six d_F>=2 (R1): count / uncoverable | min #min-transversals covering an admissible triple | uncoverable triples (all non-admissible unless col 5>0) |')
out.append('|---|---|---|---|---|---|---|---|---|')
for k, r in cells:
    out.append('| %d | (%d,%d,%d) | %d | %d | %d | %d / %d | %d / %d | %s | %d |' % (r['slack'], r['n'], r['m'], r['tau'], r['triples'], r['triples_admissible'], r['admissible_uncoverable'], r['adm_R2'], r['adm_R2_unc'], r['adm_R1'], r['adm_R1_unc'], r['adm_min_cover_count'], r['uncoverable_total']))
out.append('\n### Table 3: uncoverable triples that are NOT admissible: violated class-C condition (a triple can violate several)\n')
out.append('bits: N = some pair lies inside an edge of F (non-linear), F = F7 appears in F+v (counted for every triple, linear or not), P = e(S) <= |S|-2 violated. "A" = P-violation by a set S containing two of the pairs and tight in F (|S\'|-e = 2); "B" = P-violation only through a set containing all six vertices with |S\'|-e <= 3. minS = size |S| (including v) of the smallest violating S.\n')
out.append('| slack | cell | uncoverable | N only-P/ N+P / F+P / N+F+P / P only / other | P violated (A / B-only) | min violating |S| histogram (B-only) |')
out.append('|---|---|---|---|---|---|')
nm = {1: 'N', 2: 'F', 3: 'NF', 4: 'P', 5: 'NP', 6: 'FP', 7: 'NFP', 0: 'ok'}
for k, r in cells:
    c = r['uncoverable_nonadm_by_combo']['L,F,P bits (1=nonlinear,2=F7,4=P3 violated)']
    out.append('| %d | (%d,%d,%d) | %d | %s | %d / %d | %s |' % (r['slack'], r['n'], r['m'], r['tau'], r['uncoverable_total'], ', '.join('%s:%d' % (nm[int(i)], v) for i, v in sorted(c.items())) or '-', r['uncoverable_violates_A'], r['uncoverable_violates_B_only'], ', '.join('%s:%d' % (a, b) for a, b in r['B_only_minS'].items()) or '-'))
out.append('\n### Table 4: P2 failures by key = d_x + d_y - [x,y share an edge], summed over the classes of each slack (pairs failing / pairs)\n')
bys = {}
for k, r in cells:
    d = bys.setdefault(r['slack'], {})
    for key, tot in r['p2_by_key_total'].items():
        a = d.setdefault(int(key), [0, 0]); a[1] += tot
    for key, (fl, tot) in r['p2_fail_by_key'].items(): d[int(key)][0] += fl
out.append('| slack | ' + ' | '.join('key %d' % i for i in range(1, 9)) + ' |')
out.append('|---|' + '---|' * 8)
for s in sorted(bys):
    out.append('| %d | ' % s + ' | '.join('%d/%d' % tuple(bys[s][i]) if i in bys[s] else '-' for i in range(1, 9)) + ' |')
open(os.path.join(here, 'tables.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
