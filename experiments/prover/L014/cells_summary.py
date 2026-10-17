"""(L014) python3 cells_summary.py CELLDIR : one line per complete cell file (key, route, classes, seconds; for recursion cells every branch
with d, t', S', decompositions, inputs and the ext_d counters, hits_in_C, connected_hits); totals; every ext_d call's bad_tau."""
import sys, os, re, json
d = sys.argv[1]; rows = []; nbad = 0; ncalls = 0
for fn in sorted(os.listdir(d), key=lambda f: tuple(int(x) for x in re.findall(r'\d+', f))):
    if not re.match(r'cell_\d+_\d+_\d+_D\d+\.txt$', fn): continue
    k = tuple(int(x) for x in re.findall(r'\d+', fn)); reps = 0; info = None
    for l in open(os.path.join(d, fn)):
        if l.startswith('FOUND:'): reps += 1
        elif l.startswith('INFO '): info = json.loads(l[5:])
    if info is None: print('INCOMPLETE', fn); continue
    s = '(%d,%d,%d,%d) %s classes=%d secs=%s' % (k + (info['route'], reps, info.get('secs')))
    if info['route'] == 'direct': s += ' %s labelled=%s in_C_tau=%s' % (info.get('enum'), info.get('labelled'), info.get('in_C_tau_exact'))
    for b in info.get('branches', []):
        e = b.get('ext', {})
        if e: ncalls += 1; nbad += e.get('bad_tau', 0)
        s += ' | d=%d tp=%d S=%d decs=%d inputs=%d' % (b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs'])
        if e: s += ' nodes=%d F7free=%d in_C=%d bad_tau=%d' % (e['nodes'], e['hits_F7free'], e['hits_in_C'], e['bad_tau'])
    if info['route'] == 'recurse': s += ' | connected_hits=%s' % info.get('connected_hits')
    rows.append((k, s))
for k, s in rows: print(s)
print('SUMMARY cells %d (direct %d, recurse %d), classes %d, ext_d branch calls %d, total bad_tau %d' % (
    len(rows), sum(' direct ' in s for _, s in rows), sum(' recurse ' in s for _, s in rows),
    sum(int(re.search(r'classes=(\d+)', s).group(1)) for _, s in rows), ncalls, nbad))
