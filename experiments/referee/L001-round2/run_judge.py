"""Run the frozen judge (read-only use) on the files in jin/ and save its stdout to judge.log here."""
import subprocess, glob, time, collections
files = sorted(glob.glob('/home/user/Erdos-757/experiments/referee/L001-round2/jin/*.json'))
t = time.time()
p = subprocess.run(['python3', '/home/user/Erdos-757/judge/judge.py'] + files, capture_output=True, text=True,
                   cwd='/home/user/Erdos-757', timeout=850)
open('/home/user/Erdos-757/experiments/referee/L001-round2/judge.log', 'w').write(p.stdout + p.stderr)
lines = [l for l in p.stdout.splitlines() if l.startswith('JUDGE:')]
print('exit', p.returncode, '| files', len(files), '| verdict lines', len(lines), '| %.1fs' % (time.time() - t))
print(collections.Counter(' '.join(l.split()[1:3]) + ' ' + ' '.join(w for w in l.split() if w.startswith(('n=', 'h=')))
                          for l in lines))
print([l for l in lines if 'NO-IMPROVEMENT' not in l][:5])
