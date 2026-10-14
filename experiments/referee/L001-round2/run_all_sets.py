"""Write claim-format files for all 1,743 extension sets (with the authors' witness as witness_sidon_subset) into
jin_all/, then run the frozen judge (read-only) on them; save its stdout to judge_all.log."""
import json, os, subprocess, glob, time, collections
from fractions import Fraction as F
D = '/home/user/Erdos-757/experiments/referee/L001-round2/'
W = json.load(open('/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/witnesses.json'))
A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
os.makedirs(D + 'jin_all', exist_ok=True)
for i, w in enumerate(W['pairs']):
    json.dump({'id': 'r2all-%04d' % i, 'type': 'construction', 'set': [str(a) for a in A] + [w['x'], w['y']],
               'claimed_h': 10, 'witness_sidon_subset': w['S'], 'notes': 'referee L001 r2'},
              open(D + 'jin_all/r2all-%04d.json' % i, 'w'))
files = sorted(glob.glob(D + 'jin_all/*.json'))
t = time.time()
p = subprocess.run(['python3', '/home/user/Erdos-757/judge/judge.py'] + files, capture_output=True, text=True,
                   cwd='/home/user/Erdos-757', timeout=850)
open(D + 'judge_all.log', 'w').write(p.stdout + p.stderr)
lines = [l for l in p.stdout.splitlines() if l.startswith('JUDGE:')]
print('exit', p.returncode, '| files', len(files), '| verdict lines', len(lines), '| %.1fs' % (time.time() - t))
print(collections.Counter(' '.join(l.split()[1:3]) + ' ' + ' '.join(w for w in l.split() if w.startswith(('n=', 'h=')))
                          for l in lines))
print([l for l in lines if 'NO-IMPROVEMENT' not in l][:5])
