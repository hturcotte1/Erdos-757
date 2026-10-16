"""S5b: run the frozen verifier (read-only) on every file in jin/ in ONE process and summarise.
Writes its own log (s5_frozen.log) so that no shell redirect is needed."""
import collections, glob, subprocess, sys, time

t0 = time.time()
files = sorted(glob.glob('jin/*.json'))
p = subprocess.run([sys.executable, '/home/user/Erdos-757/judge/judge.py'] + files, capture_output=True, text=True)
open('s5_frozen.log', 'w').write(p.stdout + p.stderr)
lines = [l for l in p.stdout.splitlines() if l.startswith('JUDGE:')]
cnt = collections.Counter((l.split()[1], l.split()[2]) for l in lines)
print('files', len(files), '| verdict lines', len(lines), '| exit code', p.returncode)
print('verdicts:', dict(cnt))
print('n=14 h=8:', sum('n=14 h=8 ' in l for l in lines), '| n=15 h=9:', sum('n=15 h=9 ' in l for l in lines),
      '| n=16 h=10:', sum('n=16 h=10 ' in l for l in lines))
print('time %.1fs' % (time.time() - t0))
