# Referee round 2: two-sided control at n=14: (4,5)-realizations of the 11 classes of cell(14,12,6,4) (rz) vs the 2,910 L004 classes.
import subprocess, json, gzip, itertools, re
from fractions import Fraction
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def canon_aff(vals):
    lo, hi = min(vals), max(vals); a = sorted(Fraction(x - lo) / (hi - lo) for x in vals); b = sorted(1 - x for x in a); return min(tuple(a), tuple(b))
def weak_sidon(s):
    t = [x + y for x, y in itertools.combinations(s, 2)]; return len(t) == len(set(t))
def is45(s):
    return all(len(set(abs(x - y) for x, y in itertools.combinations(q, 2))) >= 5 for q in itertools.combinations(s, 4))
cl = [l for l in open('out/cells_x/cells/cell_14_12_6_D4.txt') if l.startswith('FOUND')]
open('out/c14_11.txt', 'w').write(''.join(cl))
out = subprocess.run(['nice', '-n', '5', './out/rz', '14', 'print'], stdin=open('out/c14_11.txt'), capture_output=True, text=True).stdout.splitlines()
aff = set(); per = []; cur = 0; cur45 = 0; nreal = 0; n45 = 0; bf = 0
for l in out:
    if l.startswith('REAL'):
        y = [int(t) for t in l.split(':')[1].split()]; nreal += 1; cur += 1
        w = weak_sidon(y)
        if bf < 4000: assert w == is45(y); bf += 1
        if w: aff.add(canon_aff(y)); n45 += 1; cur45 += 1
    elif l.startswith('G '): per.append((cur, cur45)); cur = cur45 = 0
census = set(canon_aff(sorted(json.loads(l)['set'])) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt'))
print('classes %d; realizations per class (all, (4,5)): %s' % (len(per), per))
print('realizations %d, (4,5) %d; affine classes of (4,5)-realizations %d; census %d; equal: %s' % (nreal, n45, len(aff), len(census), aff == census))
