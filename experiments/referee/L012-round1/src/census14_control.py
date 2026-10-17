"""Referee control: every one of the 2,910 saturated extremal 14-point census sets (L004) must be found by rreal as a realization
of its own AP pattern (labels = rank order; normalised values compared modulo p)."""
import gzip, json, itertools, subprocess
P = 2147483647
lines = []
for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt'):
    c = json.loads(l); S = sorted(c['set']); idx = {a: i for i, a in enumerate(S)}
    E = sorted(tuple(sorted((idx[a], idx[(a + b) // 2], idx[b]))) for a, b in itertools.combinations(S, 2) if (a + b) % 2 == 0 and (a + b) // 2 in idx)
    assert len(E) == 12
    t = [((a - S[0]) * pow(S[-1] - S[0], P - 2, P)) % P for a in S]
    lines.append('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in E) + ' | ' + ','.join(map(str, t)))
out = subprocess.run(['./out/bin/rreal', '14'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
st = [dict(x.split('=') for x in l.split()[1:]) for l in out if l.startswith('STAT')]
print('n=14 census sets %d, own set found %d, total realizations %d, singular %d' % (len(st), sum(int(s['target_found']) >= 1 for s in st), sum(int(s['realizations']) for s in st), sum(int(s['singular']) for s in st)))
