"""Run the frozen judge (read-only, as a subprocess) on all claim files in ./jin and save its stdout here."""
import subprocess, glob, time, collections, re
from fractions import Fraction as Fr
D = '/home/user/Erdos-757/experiments/referee/L001-round4/'
JUDGE = '/home/user/Erdos-757/judge/judge.py'
files = sorted(glob.glob(D + 'jin/*.json'))
t0 = time.time()
p = subprocess.run(['python3', JUDGE] + files, capture_output=True, text=True)
with open(D + 'judge_run.log', 'w') as f:
    f.write(p.stdout + p.stderr + '\nexit=%d seconds=%.1f\n' % (p.returncode, time.time() - t0))
lines = p.stdout.splitlines()
c = collections.Counter(re.search(r'JUDGE: (\S+ \S+)', l).group(1) for l in lines)
nh = collections.Counter(re.search(r'n=(\d+) h=(\d+)', l).groups() for l in lines if 'PASS' in l)
print('files', len(files), 'verdict lines', len(lines), 'exit', p.returncode, dict(c), 'seconds %.1f' % (time.time() - t0))
for (n, h), k in sorted(nh.items()):
    r = Fr(int(h), int(n))
    print('  n=%s h=%s: %d sets; h/n = %s ; h/n < 4/7 ? %s' % (n, h, k, r, r < Fr(4, 7)))
