"""Run the frozen judge (read-only) on the referee's spot claim files; save its output in this directory."""
import subprocess, glob, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(HERE, 'spot', '*.json')))
JUDGE = os.path.join('/home/user/Erdos-757', 'judge', 'judge.py')
r = subprocess.run([sys.executable, JUDGE] + files, capture_output=True, text=True)
with open(os.path.join(HERE, 'spot_judge.txt'), 'w') as fh:
    fh.write(r.stdout + r.stderr)
print('exit', r.returncode, 'files', len(files), 'PASS NO-IMPROVEMENT', r.stdout.count('PASS NO-IMPROVEMENT'),
      'NEW-RECORD', r.stdout.count('NEW-RECORD'), 'FAIL', r.stdout.count('FAIL'))
lines = r.stdout.splitlines()
print(lines[0]); print(lines[-1])
