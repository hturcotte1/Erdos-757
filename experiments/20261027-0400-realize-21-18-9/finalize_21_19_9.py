"""Summarise the (rexact_c) sweep of cell(21,19,9,4): results_21_19_9.json (counts, index lists, labellings) and sets_21_19_9_realizable.json
(explicit integer sets verified in Python for the first LIMIT realizable classes: is_45_set, #APs, h).   usage: finalize_21_19_9.py [LIMIT]"""
import sys, re, json, subprocess
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 300
tot = 0; real = []; notr = []; labs = {}; cur = None
for l in open('out_21_19_9_full.txt'):
    if l.startswith('RES'):
        p = l.split(); cur = int(p[1]); tot += 1
        (real if p[2] == 'REAL' else notr).append(cur)
    elif l.startswith('LAB') and cur is not None: labs[cur] = l[4:].strip()
ncls = sum(1 for l in open('work/cell_21_19_9.txt'))
json.dump(dict(cell='(21,19,9) Delta<=4, list ../20261027-0340-induction-n28-n29-f25/lists/cell_21_19_9_D4.txt', classes_in_list=ncls, tested=tot,
               sweep_complete=(tot == ncls), realizable=len(real), not_realizable=len(notr), realizable_indices=real, not_realizable_indices=notr,
               first_labelling={str(k): labs[k] for k in real[:LIMIT] if k in labs}), open('results_21_19_9.json', 'w'))
print('tested', tot, 'of', ncls, 'realizable', len(real), 'not', len(notr), 'complete', tot == ncls)
subprocess.run(['python3', 'verify_lab.py', 'work/cell_21_19_9.txt', 'out_21_19_9_full.txt', '21', 'verify_realizable_21_19_9.json', str(LIMIT)], check=True, stdout=subprocess.DEVNULL)
v = json.load(open('verify_realizable_21_19_9.json'))
json.dump([dict(cls=x['cls'], set=x['set'], is_45=x['is_45'], num_aps=x['num_aps'], h=x['h']) for x in v if 'set' in x], open('sets_21_19_9_realizable.json', 'w'))
print('verified sets', len(v), 'all (4,5)', all(x['is_45'] for x in v), 'h values', sorted({x['h'] for x in v}))
