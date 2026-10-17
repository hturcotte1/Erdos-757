"""(L013, prover) Text summary of positive_control.jsonl (C8 (b))."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
out = []
for l in open(os.path.join(HERE, 'positive_control.jsonl')):
    if not l.strip(): continue
    r = json.loads(l)
    if 'status' in r: out.append('(%s): %s' % (','.join(r['cell'].split()[:4]), r['status'])); continue
    n, m, t, D = r['cell']
    if r['members_generated'] == 0: out.append('(%d,%d,%d,%d): no member generated in %s tries (vacuous)' % (n, m, t, D, format(r['tries'], ',')))
    else: out.append('(%d,%d,%d,%d): %d generated (%d distinct classes), %s in the engine\'s list of %s classes' % (n, m, t, D, r['members_generated'], r['distinct_classes_generated'], 'all %d' % r['found_in_cell'] if r['missing'] == 0 else '%d of them (MISSING %d)' % (r['found_in_cell'], r['missing']), format(r['cell_classes'], ',')))
print('; '.join(out) + '.')
