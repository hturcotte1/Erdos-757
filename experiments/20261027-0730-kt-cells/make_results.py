import json
R = json.load(open('closure2_results.json')); P = json.load(open('deps_provenance.json'))
neg = [s for s in R['summary'] if s['A'] < 0]; pos = [s for s in R['summary'] if s['A'] >= 0]
res = dict(
  verdict_KT_n_le_27 = 'KT^{L*} holds on every connected member of C_3 with n<=27 (A<0 cells: all graphs have A+DEF>=0; A>=0: trivial); no new irreducible special piece',
  n_cells_A_negative=len(neg), graphs_A_negative=sum(s['graphs'] for s in neg),
  nonempty_A_negative_cells={str(tuple(s['cell'])): dict(A=s['A'], graphs=s['graphs'], irreducible=s['irreducible'], P_zero=s['P_zero'], minP=s['minP']) for s in neg if s['graphs']},
  irreducible_pieces=len(R['pieces']), new_pieces=[p for p in R['pieces'] if p['n'] >= 25],
  equality_cases_outside_Lstar=sum(s['P_zero'] for s in neg),
  new_cells={'(25,14,9,3)': 0, '(26,17,10,3)': 0, '(27,13,9,3)': 18, '(27,20,11,3)': 0},
  reused_empty_cells=['(26,13,9,3)', '(27,15,10,3)', '(27,16,10,3)'],
  A_nonneg_cells_checked=[dict(cell=s['cell'], A=s['A'], graphs=s['graphs'], minP=s['minP'], source=s['source']) for s in pos],
  missing_A_nonneg_cells_not_needed_for_KT=R['missing'],
  all_cells=R['summary'])
json.dump(res, open('results.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ('all_cells', 'A_nonneg_cells_checked')}, indent=1))
