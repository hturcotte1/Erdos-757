# Referee round 2: falsification probe of I11 (L011: 11 tau <= 3n + 2m on C for n <= 22) on fresh members of C: all H - v and
# H - {v,w} of the 699 classes (vertex deletion keeps C; deleted vertices' edges removed; isolated vertices kept).
import re, subprocess
from collections import Counter
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
G = [parse(l) for l in open('out/r4_699.txt')]
def sub(E, rm):
    keep = [v for v in range(23) if v not in rm]; mp = {v: i for i, v in enumerate(keep)}
    return [tuple(mp[x] for x in e) for e in E if not (set(e) & rm)]
for k in (1, 2):
    nn = 23 - k; lines = []
    for E in G:
        if k == 1: rms = [{v} for v in range(23)]
        else: rms = [{v, w} for v in range(23) for w in range(v + 1, 23)]
        for rm in rms:
            F = sub(E, rm); lines.append('%d ' % len(F) + ' '.join('%d %d %d' % e for e in F) + '\n')
    open('out/i11_in.txt', 'w').write(''.join(lines))
    out = subprocess.run(['nice', '-n', '5', './out/fr', str(nn), 'print'], stdin=open('out/i11_in.txt'), capture_output=True, text=True).stdout.splitlines()
    sv = [l for l in out if l.startswith('SURV')]
    viol = 0; slack = Counter(); taus = Counter()
    for l in sv:
        t = int(l.split()[1].split('=')[1]); m = int(l.split(':', 1)[1].split()[0]); s = 3 * nn + 2 * m - 11 * t
        slack[s] += 1; taus[t] += 1
        if s < 0: viol += 1
    print('H minus %d vertices: graphs %d, in C %d (expected all), I11 violations %d, tau distribution %s, min slack %d'
          % (k, len(lines), len(sv), viol, dict(taus), min(slack)))
