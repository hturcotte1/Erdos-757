"""Referee L023 round 1: seed cells/ with refereed lists only (L012, L013, L014 cells.tar.gz, L014 cell_15_13_6_D3.txt.gz,
L016 cells_new.tar.gz, extracted into seed/<src>/). A list counts only if it carries an INFO line (complete engine output).
Duplicated keys across sources must have identical FOUND sets."""
import os, re, glob, gzip, hashlib
seen = {}; src_of = {}; conflicts = []; skipped = []
for src in ('L012', 'L013', 'L014', 'L016'):
    for p in sorted(glob.glob('seed/%s/**/cell_*' % src, recursive=True)):
        m = re.search(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt(\.gz)?$', p)
        if not m: skipped.append(p); continue
        key = tuple(map(int, m.groups()[:4]))
        txt = (gzip.open if p.endswith('.gz') else open)(p, 'rt').read()
        lines = txt.splitlines()
        if not any(l.startswith('INFO ') for l in lines): skipped.append(p); continue
        F = frozenset(l.strip() for l in lines if l.startswith('FOUND:'))
        if key in seen:
            if seen[key] != F: conflicts.append((key, src_of[key], p))
            continue
        seen[key] = F; src_of[key] = p
        with open('cells/cell_%d_%d_%d_D%d.txt' % key, 'w') as f:
            f.write(txt if txt.endswith('\n') else txt + '\n')
print('seeded', len(seen), 'keys; conflicts', len(conflicts), conflicts[:5], '; skipped', len(skipped))
for k in sorted(seen): print('SEED', k, len(seen[k]), src_of[k])
