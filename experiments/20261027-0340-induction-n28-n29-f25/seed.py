"""Seed out/cells with EVERY existing cell file; verify overlaps agree (as sets of FOUND lines); write provenance.tsv.
Sources in priority order (refereed first).  Re-runnable: picks up files that appeared since (d4 worker)."""
import os, sys, re, glob, gzip, hashlib, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(HERE, '..')
SRC = [
 ('L012 cells.tar.gz (refereed)', glob.glob(HERE+'/seedsrc/L012/**/cell_*', recursive=True)),
 ('L013 cells.tar.gz (refereed)', glob.glob(HERE+'/seedsrc/L013/**/cell_*', recursive=True)),
 ('L014 cells.tar.gz (refereed)', glob.glob(HERE+'/seedsrc/L014/**/cell_*', recursive=True)),
 ('L016 cells_new.tar.gz (refereed)', glob.glob(HERE+'/seedsrc/L016/**/cell_*', recursive=True)),
 ('20261017-2150-i11-n27 (worker, L016 cross-checked)', glob.glob(E+'/20261017-2150-i11-n27/out/cells/cell_*')+glob.glob(E+'/20261017-2150-i11-n27/cell_*.gz')),
 ('20261027-0235-cost-n28-n29 (cost study, unrefereed)', glob.glob(E+'/20261027-0235-cost-n28-n29/out/cells/cell_*')),
 ('20261027-0300-tight-cells-d4 (concurrent worker, unrefereed)', glob.glob(E+'/20261027-0300-tight-cells-d4/out/cells/cell_*')+glob.glob(E+'/20261027-0300-tight-cells-d4/cells_seed/cell_*')),
]
OUT = os.path.join(HERE, 'out', 'cells')
def key_of(p):
    m = re.search(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt(\.gz)?$', p)
    return tuple(map(int, m.groups()[:4])) if m else None
def read(p):
    op = gzip.open if p.endswith('.gz') else open
    found = []; done = False
    with op(p, 'rt') as f:
        for l in f:
            if l.startswith('FOUND:'): found.append(l.rstrip('\n'))
            elif l.startswith('INFO '): done = True
    return found, done
prov = json.load(open(os.path.join(HERE, 'provenance.json'))) if os.path.exists(os.path.join(HERE, 'provenance.json')) else {}
newc = 0; conflicts = []
for p in sorted(glob.glob(OUT + '/cell_*.txt')):
    k = key_of(p); ks = '%d,%d,%d,%d' % k
    if ks not in prov:
        found, done = read(p)
        if done: prov[ks] = dict(classes=len(found), md5=hashlib.md5('\n'.join(sorted(found)).encode()).hexdigest(), first='COMPUTED HERE (this folder)', firstpath=os.path.relpath(p, HERE), agree=[], disagree=[])
for label, files in SRC:
    for p in sorted(files):
        k = key_of(p)
        if k is None: continue
        found, done = read(p)
        if not done: continue
        ks = '%d,%d,%d,%d' % k
        h = hashlib.md5('\n'.join(sorted(found)).encode()).hexdigest()
        if ks not in prov:
            dst = os.path.join(OUT, 'cell_%d_%d_%d_D%d.txt' % k)
            if p.endswith('.gz'):
                with gzip.open(p, 'rb') as a, open(dst + '.tmp', 'wb') as b: shutil.copyfileobj(a, b)
            else: shutil.copyfile(p, dst + '.tmp')
            os.rename(dst + '.tmp', dst)
            prov[ks] = dict(classes=len(found), md5=h, first=label, firstpath=os.path.relpath(p, HERE), agree=[], disagree=[]); newc += 1
        else:
            r = prov[ks]
            if r['md5'] == h and r['classes'] == len(found):
                if label not in r['agree'] and label != r['first']: r['agree'].append(label)
            else:
                r['disagree'].append(label); conflicts.append((ks, label))
json.dump(prov, open(os.path.join(HERE, 'provenance.json'), 'w'), indent=0, sort_keys=True)
with open(os.path.join(HERE, 'provenance.tsv'), 'w') as f:
    f.write('cell(n,m,tau,Delta)\tclasses\tfirst_source\tagreeing_other_sources\tDISAGREE\n')
    for ks in sorted(prov, key=lambda s: tuple(map(int, s.split(',')))):
        r = prov[ks]; f.write('(%s)\t%d\t%s\t%s\t%s\n' % (ks, r['classes'], r['first'], '; '.join(r['agree']), '; '.join(r['disagree'])))
print('cells seeded', len(prov), 'new this run', newc, 'conflicts', conflicts)
