"""Referee L023 round 1: every list in (U1)'s out/cells whose key is a refereed key (my seeds, from the refereed tarballs) must
have the same FOUND set as the refereed list. Reports the U1 keys that are not refereed."""
import os, re
U1 = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
SEEDC = '/dev/shm/L023ref/engine_run/my_seed_output.txt'
seeded = set()
for l in open(SEEDC):
    m = re.match(r'SEED \((\d+), (\d+), (\d+), (\d+)\)', l)
    if m: seeded.add(tuple(map(int, m.groups())))
eq = diff = 0; unref = []
for f in sorted(os.listdir(U1)):
    m = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', f)
    if not m: continue
    k = tuple(map(int, m.groups()))
    if k not in seeded: unref.append(k); continue
    A = set(l.strip() for l in open(os.path.join(U1, f)) if l.startswith('FOUND:'))
    B = set(l.strip() for l in open('/dev/shm/L023ref/engine_run/cells/' + f) if l.startswith('FOUND:'))
    if A == B: eq += 1
    else: diff += 1; print('DIFFERENT', k, len(A), len(B))
print('U1 lists with a refereed key:', eq + diff, 'equal', eq, 'different', diff)
print('U1 lists without a refereed key:', len(unref))
print(sorted(unref))
