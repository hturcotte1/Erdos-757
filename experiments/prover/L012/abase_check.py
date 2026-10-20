"""(L012) Positive control: realize.c on the AP pattern of A_base (abase_pattern.txt, vertex i = i-th smallest point); counts and
whether A_base itself (normalised to [0,1], or its reflection) is among the realizations (exact Fractions)."""
import subprocess
from fractions import Fraction as F
Ab = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
out = subprocess.run(['./bin/realize', '14', 'print'], stdin=open('abase_pattern.txt'), capture_output=True, text=True).stdout.splitlines()
t = [F(a, 1056) for a in Ab]; r = [1 - x for x in t]; found = 0
for l in out:
    if l.startswith('REALIZATION'):
        h, vals = l.split(':'); D = int(h.split('=')[1]); x = [F(int(v), D) for v in vals.split()]
        found += (x == t or x == r)
print([l for l in out if l.startswith('TOTAL')][0]); print('realizations equal to A_base normalised (or its reflection):', found)
