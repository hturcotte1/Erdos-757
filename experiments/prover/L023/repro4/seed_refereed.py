"""(L023) Seed repro4/cells with the refereed lists only (L012, L013, L014 cells.tar.gz + cell_15_13_6_D3.txt.gz, L016 cells_new.tar.gz);
where several certificates hold the same key, the FOUND sets must be identical (checked)."""
import glob, os, re, shutil, gzip
OUT = 'cells'; os.makedirs(OUT, exist_ok=True)
seen = {}; conflicts = 0; n = 0
for src in ('L012', 'L013', 'L014', 'L016'):
    for p in sorted(glob.glob('seed/%s/**/cell_*.txt*' % src, recursive=True)):
        m = re.search(r'(cell_\d+_\d+_\d+_D\d+\.txt)(\.gz)?$', p); name = m.group(1)
        op = gzip.open if p.endswith('.gz') else open
        txt = op(p, 'rt').read()
        if 'INFO ' not in txt: continue
        F = sorted(l for l in txt.splitlines() if l.startswith('FOUND:'))
        if name in seen:
            if seen[name] != F: conflicts += 1; print('CONFLICT', name, p)
            continue
        seen[name] = F; open(os.path.join(OUT, name), 'w').write(txt if txt.endswith('\n') else txt + '\n'); n += 1
print('seeded', n, 'distinct refereed lists; conflicts', conflicts)
