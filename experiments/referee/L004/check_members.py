"""Referee L004: membership of SAT-sampled models (labelled, F7 handled lazily) in the census (orbit keys).
usage: python3 check_members.py CENSUS_KEYS.gz MODELS.gz [MODELS2.gz ...] ; writes distinct models to stdout-summary."""
import gzip, sys, subprocess, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
keys = set(l.split()[0] for l in gzip.open(sys.argv[1], 'rt'))
models = set()
for f in sys.argv[2:]:
    for l in gzip.open(f, 'rt'):
        if l.strip() and not l.startswith('#'): models.add(' '.join(sorted(l.split())))
out = subprocess.run([os.path.join(HERE, 'pchk'), '14'], input=''.join(m + '\n' for m in models), capture_output=True, text=True, check=True).stdout.splitlines()
c = collections.Counter(); missing = []
for l in out:
    f = l.split(); sat, lin, k30, f7, al, canon, sy = map(int, f[1:8]); key = f[8]
    assert sat and lin and k30 and al <= 8, l
    if f7: c['f7'] += 1; continue
    if key in keys: c['in_census'] += 1
    else: c['MISSING'] += 1; missing.append(f[9])
print('distinct models', len(models), dict(c))
for m in missing[:20]: print('MISSING', m)
