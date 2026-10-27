import json
L=[l.split() for l in open('out_19_16_8.txt') if l.startswith('RES')]
real=[int(p[1]) for p in L if p[2]=='REAL']; notr=[int(p[1]) for p in L if p[2]=='NOT']; cap=[int(p[1]) for p in L if p[2]=='CAP']
v=json.load(open('verify_19_16_8.json'))
json.dump(dict(cell='(19,16,8) Delta<=4', list='../20261027-0340-induction-n28-n29-f25/lists/cell_19_16_8_D4.txt', classes=len(L), realizable=len(real), not_realizable=len(notr), capped=len(cap),
  sweep_complete=True, realizable_indices=real, not_realizable_indices=notr, verified_sets_first=len(v), verified_all_45=all(x['is_45'] for x in v), verified_h=sorted({x['h'] for x in v}), verified_num_aps=sorted({x['num_aps'] for x in v}),
  claim='results/claims/C008-f19-h11.json', verdict='PASS NO-IMPROVEMENT C008-f19-h11 n=19 h=11 ratio=11/19'), open('results_19_16_8.json','w'))
json.dump(dict(status='not run: f(19)=11 settled by a realizable (19,16,8) class (C008); the D5 sweep was unnecessary', tested=0, of=785127), open('results_19_17_8_partial.json','w'))
print(len(L),len(real),len(notr),len(cap))
