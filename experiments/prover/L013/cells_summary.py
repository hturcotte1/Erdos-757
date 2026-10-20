"""(L013, prover) Table of every cell of a cell directory (n m tau Delta classes route secs, and for recursion cells the number of
branches, inputs, F7-free extensions, extensions in C and connected extensions), written to cells_table.tsv; prints the non-empty cells
(the non-vacuity list) and totals.  Usage: python3 cells_summary.py CELLDIR"""
import sys, os, re, json
cd = sys.argv[1]; rows = []
for fn in sorted(os.listdir(cd)):
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
    if not mm: continue
    L = open(os.path.join(cd, fn)).read().splitlines(); info = json.loads([l for l in L if l.startswith('INFO ')][0][5:])
    k = tuple(map(int, mm.groups())); c = sum(1 for l in L if l.startswith('FOUND:'))
    br = info.get('branches', []); inp = sum(b['inputs'] for b in br)
    f7 = sum(b.get('ext', {}).get('hits_F7free', 0) for b in br); inC = sum(b.get('ext', {}).get('hits_in_C', 0) for b in br)
    rows.append(k + (c, info['route'], info.get('secs'), len(br), inp, f7, inC, info.get('connected_hits', '')))
rows.sort()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cells_table.tsv'), 'w') as f:
    f.write('n\tm\ttau\tDelta\tclasses\troute\tsecs\tbranches\tinputs\text_F7free\text_in_C\tconnected_ext\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
print('cells: %d (direct %d, recursion %d); non-empty: %d; total classes: %d' % (len(rows), sum(1 for r in rows if r[5] == 'direct'),
      sum(1 for r in rows if r[5] == 'recurse'), sum(1 for r in rows if r[4]), sum(r[4] for r in rows)))
print('recursion cells (n,m,tau,Delta): classes [branches, inputs, F7-free extensions, extensions in C, connected]:')
for r in rows:
    if r[5] == 'recurse': print('   (%d,%d,%d,%d): %d  [%d, %d, %d, %d, %s]' % (r[:5] + r[7:]))
print('non-empty direct cells (n,m,tau,Delta): classes:')
print('   ' + ', '.join('(%d,%d,%d,%d): %d' % r[:5] for r in rows if r[5] == 'direct' and r[4]))
print('empty direct cells:', len([r for r in rows if r[5] == 'direct' and not r[4]]))
