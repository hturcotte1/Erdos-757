import json, re, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
prov = json.load(open(os.path.join(HERE, 'provenance.json')))
def short(ks):
    r = prov.get(ks)
    if r is None: return '?'
    f = r['first']
    if f.endswith('(refereed)'): return 'refereed(' + f.split(' ')[0] + ')'
    if f.startswith('COMPUTED HERE'): return 'here'
    return 'unrefereed:' + f.split(' ')[0]
rows = [l.split('\t') for l in open(os.path.join(HERE, 'cells_table.tsv')).read().splitlines()[1:]]
out = open(os.path.join(HERE, 'components_table.tsv'), 'w'); out.write('cell\tbranch(d,tp,S\')\tdecompositions_total\tdecomposition\tinputs\tcomponents(cell:classes:provenance)\n')
cols = open(os.path.join(HERE, 'cells_table2.tsv'), 'w'); cols.write('cell\tD\tclasses\tinputs\tnodes\tseconds\tbad_tau\thits_in_C\tdecompositions(all branches)\tbranches\n')
seen = set()
for r in rows:
    k = tuple(map(int, re.findall(r'\d+', r[0]))); ks = '%d,%d,%d,%d' % k
    if ks in seen: continue
    seen.add(ks)
    p = os.path.join(HERE, 'out/cells/cell_%d_%d_%d_D%d.txt' % k)
    info = None
    for l in open(p):
        if l.startswith('INFO '): info = json.loads(l[5:])
    brs = info.get('branches', [])
    cols.write('\t'.join(map(str, [r[0], k[3], r[1], r[2], r[3], r[4], r[5], r[6], sum(b['decompositions'] for b in brs), ';'.join("d=%d,tp=%d,S'=%d" % (b['d'], b['tp'], b['Sp']) for b in brs) or 'direct'])) + '\n')
    for b in brs:
        for dec, size in b['dec']:
            if size == 0: continue
            groups = {}
            for c in dec: groups[tuple(c)] = groups.get(tuple(c), 0) + 1
            comp = []
            for c, kk in sorted(groups.items()):
                cks = '%d,%d,%d,%d' % (c[0], c[1], c[2], b['d'])
                if c == (1, 0, 0): comp.append('%dxisolated vertex' % kk); continue
                cn = prov[cks]['classes'] if cks in prov else 0
                comp.append('%dx(%s):%d:%s' % (kk, cks, cn, short(cks)))
            out.write('\t'.join([r[0], "d=%d,tp=%d,S'=%d" % (b['d'], b['tp'], b['Sp']), str(b['decompositions']), str([tuple(c) for c in dec]), str(size), ' + '.join(comp)]) + '\n')
print(len(seen))
