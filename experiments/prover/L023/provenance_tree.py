"""(L023) Join the dry-run tree of engine.cell(25,23,11,4) with the provenance table of the induction run
experiments/20261027-0340-induction-n28-n29-f25 (provenance.json, written by its seed.py).
For every non-trivial key of the tree: classes in the stored list, route, first source, agreeing sources,
SHA-256 of the stored cell file (out/cells/cell_n_m_t_D<D>.txt).  Prints the unrefereed keys separately.
usage: python3 provenance_tree.py tree_25_23_11_4.txt"""
import sys, json, re, hashlib, os
RUN = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25'
prov = json.load(open(RUN + '/provenance.json'))
keys = []
for l in open(sys.argv[1]):
    m = re.match(r'CELL \((\d+), (\d+), (\d+), (\d+)\) (\w+)', l)
    if m: keys.append((tuple(map(int, m.groups()[:4])), m.group(5)))
REF = ('L012', 'L013', 'L014', 'L016')
nref = nun = 0; unref = []
rows = []
for k, route in keys:
    ks = '%d,%d,%d,%d' % k
    p = prov.get(ks)
    fn = RUN + '/out/cells/cell_%d_%d_%d_D%d.txt' % k
    sha = hashlib.sha256(open(fn, 'rb').read()).hexdigest() if os.path.exists(fn) else 'MISSING'
    nfound = sum(1 for l in open(fn) if l.startswith('FOUND:')) if os.path.exists(fn) else -1
    if p is None:
        rows.append((k, route, nfound, 'NO PROVENANCE', '', sha)); unref.append(k); nun += 1; continue
    srcs = [p['first']] + p['agree']
    refd = any(s.startswith(REF) and 'refereed' in s for s in srcs)
    assert p['classes'] == nfound, (k, p['classes'], nfound)
    assert not p['disagree'], (k, p['disagree'])
    rows.append((k, route, nfound, p['first'], '; '.join(p['agree']), sha))
    if refd: nref += 1
    else: nun += 1; unref.append(k)
for r in rows:
    print('KEY %s route=%s classes=%d first=%s | agree=%s | sha256=%s' % r)
print('SUMMARY keys %d refereed(some source L012/L013/L014/L016) %d unrefereed-only %d' % (len(rows), nref, nun))
for k in unref:
    r = [x for x in rows if x[0] == k][0]
    print('UNREFEREED %s route=%s classes=%d first=%s | agree=%s | sha256=%s' % r)
