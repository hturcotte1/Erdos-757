"""Own check: every list in U1's out/cells whose key is refereed (present in the 247 refereed tarball lists seeded in engine/cells
before any computation) is identical to the refereed list as a set of FOUND lines."""
import os, re, glob
U1 = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
MINE = '/home/user/Erdos-757/experiments/referee/L023-round1-fable/engine/cells'
twice = {'22_14_8_D3','21_11_7_D3','11_5_3_D3','8_4_2_D3','5_3_1_D3','19_13_7_D3','16_12_6_D3','13_11_5_D3','18_10_6_D3','15_9_5_D3','12_8_4_D3','9_7_3_D3'}
gap = {'24_20_10_D3','23_17_9_D3','21_19_9_D3','20_16_8_D3','17_15_7_D3'}
def F(p):
    return frozenset(l.rstrip('\n') for l in open(p) if l.startswith('FOUND:'))
eq = diff = 0; only_u1 = []
for p in sorted(glob.glob(U1 + '/cell_*.txt')):
    k = re.search(r'cell_(.*)\.txt', p).group(1)
    q = os.path.join(MINE, 'cell_%s.txt' % k)
    if k in twice or k in gap or not os.path.exists(q): only_u1.append(k); continue
    if F(p) == F(q): eq += 1
    else: diff += 1; print('DIFFERENT', k)
print('U1 lists with a refereed counterpart: equal %d, different %d; U1-only (unrefereed/twice/gap/other) %d' % (eq, diff, len(only_u1)))
# the tree of (25,23,11,4): 172 keys per tree.py; count how many of its keys are refereed
keys = set()
for line in open('/home/user/Erdos-757/experiments/prover/L023/tree_25_23_11_4.txt'):
    m = re.match(r'CELL \((\d+), (\d+), (\d+), (\d+)\)', line)
    if m: keys.add('%s_%s_%s_D%s' % m.groups())
ref = sum(1 for k in keys if os.path.exists(os.path.join(MINE, 'cell_%s.txt' % k)) and k not in twice and k not in gap)
print('tree keys %d; refereed %d; twice-computed %d; gap %d; other %d' % (len(keys), ref, len(keys & twice), len(keys & gap), len(keys) - ref - len(keys & twice) - len(keys & gap)))
print('other:', sorted(k for k in keys if not os.path.exists(os.path.join(MINE, 'cell_%s.txt' % k)) and k not in twice and k not in gap))
