"""(L023) For every key of the dry-run tree of (25,23,11,4) whose stored list in (U1)'s out/cells is not one of the 26 unrefereed
lists, check that it is identical (set of FOUND lines) to the refereed list of the same key extracted in repro4/cells (L012/L013/L014/L016)."""
import re, os
R = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
un = set(tuple(map(int, re.findall(r'\d+', l.split('route')[0]))) for l in open('provenance_tree_D4_output.txt') if l.startswith('UNREFEREED'))
keys = [tuple(map(int, m.groups())) for m in (re.match(r'CELL \((\d+), (\d+), (\d+), (\d+)\)', l) for l in open('tree_25_23_11_4.txt')) if m]
seeded = set(l.strip() for l in open('repro4/seeded_names.txt'))
eq = df = miss = 0
for k in keys:
    if k in un: continue
    name = 'cell_%d_%d_%d_D%d.txt' % k
    if name not in seeded: miss += 1; print('NOT IN REFEREED SEEDS', k); continue
    a = sorted(l.strip() for l in open(os.path.join('repro4/cells', name)) if l.startswith('FOUND:'))
    b = sorted(l.strip() for l in open(os.path.join(R, name)) if l.startswith('FOUND:'))
    if a == b: eq += 1
    else: df += 1; print('DIFFERENT', k)
print('SUMMARY keys %d unrefereed %d refereed-checked %d equal %d different %d missing %d' % (len(keys), len(un & set(keys)), eq + df + miss, eq, df, miss))
