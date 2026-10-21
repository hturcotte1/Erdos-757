"""(L016) the seed lists: L013's cells.tar.gz (167 lists) and L014's cells.tar.gz (145) + cell_15_13_6_D3.txt.gz, unpacked into
SEED13 and SEED14; overlapping lists must have identical FOUND sets; prints the union size.  python3 seed_check.py SEED13 SEED14"""
import os, sys
a, b = sys.argv[1], sys.argv[2]
A = set(f for f in os.listdir(a) if f.startswith('cell_')); B = set(f for f in os.listdir(b) if f.startswith('cell_'))
def reps(p): return sorted(l.strip() for l in open(p) if l.startswith('FOUND:'))
def done(p): return any(l.startswith('INFO ') for l in open(p))
common = A & B; diff = [f for f in sorted(common) if reps(os.path.join(a, f)) != reps(os.path.join(b, f))]
print('L013 lists', len(A), 'L014 lists', len(B), 'common', len(common), 'common with different FOUND sets', len(diff), diff)
print('lists without INFO line', [f for f in A if not done(os.path.join(a, f))], [f for f in B if not done(os.path.join(b, f))])
print('union', len(A | B))
