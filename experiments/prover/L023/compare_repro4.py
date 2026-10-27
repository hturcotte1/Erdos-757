"""(L023) Compare the lists recomputed in repro4/cells (fresh directory seeded with the refereed lists of L012/L013/L014/L016 only)
with the stored lists of the induction run, for every key that repro4 computed (no INFO-free files), as sets of FOUND lines."""
import glob, os, re
R = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
seeded = set(l.strip() for l in open('repro4/seeded_names.txt'))
eq = df = 0
for p in sorted(glob.glob('repro4/cells/cell_*.txt')):
    name = os.path.basename(p)
    if name in seeded: continue
    a = sorted(l.strip() for l in open(p) if l.startswith('FOUND:'))
    q = os.path.join(R, name)
    if not os.path.exists(q): print('NEW', name, len(a), '(no stored list)'); continue
    b = sorted(l.strip() for l in open(q) if l.startswith('FOUND:'))
    ok = a == b; eq += ok; df += (not ok)
    print('%s %s recomputed %d stored %d' % ('EQUAL' if ok else 'DIFFERENT', name, len(a), len(b)))
print('SUMMARY recomputed lists compared %d equal %d different %d' % (eq + df, eq, df))
