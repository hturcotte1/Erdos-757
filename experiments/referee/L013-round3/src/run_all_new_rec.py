"""Run MY extension program on every branch of every recursion cell of L013 that is not in L012's cells.tar.gz; compare with the prover's
INFO counters (inputs, hits_F7free, hits_in_C per branch; connected_hits per cell); for non-empty cells with <= 1000 classes check that every
prover representative is isomorphic to one of my connected in-C exact-tau hits (invariant buckets + VF2)."""
import tarfile, re, json, glob, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
HERE = '/home/user/Erdos-757/experiments/referee/L013-round3'; P = '/home/user/Erdos-757/experiments/prover/L013/out/cells'
L012 = set()
with tarfile.open('/home/user/Erdos-757/experiments/prover/L012/cells.tar.gz') as tf:
    for mem in tf.getmembers():
        mm = re.match(r'.*cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', mem.name)
        if mm: L012.add(tuple(map(int, mm.groups())))
def parse(f):
    reps = []; info = None
    for l in open(f):
        if l.startswith('FOUND:'): reps.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
        if l.startswith('INFO '): info = json.loads(l[5:])
    return reps, info
def inc(es, n):
    g = nx.Graph()
    for v in range(n): g.add_node(('v', v), side=0)
    for i, e in enumerate(es):
        g.add_node(('e', i), side=1)
        for v in e: g.add_edge(('v', v), ('e', i))
    return g
def inv(es, n):
    deg = [0] * n
    for e in es:
        for v in e: deg[v] += 1
    return (tuple(sorted(deg)), tuple(sorted(tuple(sorted(deg[v] for v in e)) for e in es)))
problems = 0; cells_done = 0
for f in sorted(glob.glob(P + '/cell_*.txt')):
    k = tuple(map(int, re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt', os.path.basename(f)).groups()))
    if k in L012: continue
    reps, info = parse(f)
    if info['route'] != 'recurse': continue
    n, m, t, D = k; cells_done += 1; t0 = time.time(); myconn = 0; hitfiles = []; line = []
    for b in info['branches']:
        d, tp, Sp = b['d'], b['tp'], b['Sp']; tag = '%d_%d_%d_D%d_d%d_tp%d' % (n, m, t, D, d, tp)
        inp = os.path.join(HERE, 'out', 'in_%s.txt' % tag); outp = os.path.join(HERE, 'out', 'x_%s.txt' % tag)
        with open(inp, 'w') as fo: subprocess.run(['python3', os.path.join(HERE, 'src', 'build_inputs.py'), str(n), str(m), str(t), str(D), str(d), str(tp), P], stdout=fo, stderr=subprocess.DEVNULL, check=True)
        ni = sum(1 for _ in open(inp))
        if ni != b['inputs']: problems += 1; print('INPUT COUNT MISMATCH', k, (d, tp), ni, b['inputs'])
        if ni == 0: line.append('d=%d tp=%d inputs=0' % (d, tp)); continue
        with open(inp) as fi, open(outp, 'w') as fo: subprocess.run(['nice', '-n', '10', 'timeout', '3600', os.path.join(HERE, 'bin', 'xext_ref'), str(n - 1), str(tp), str(t), str(d), str(d - 1)], stdin=fi, stdout=fo, check=True)
        summ = open(outp).read().strip().splitlines()[-1]; kv = dict(x.split('=') for x in summ.split()[2:] if '=' in x and x.split('=')[0] not in ('mode',))
        e = b.get('ext', {})
        ok = (int(kv['bad_tau']) == 0 and int(kv['graphs']) == ni and int(kv['hits_F7free']) == e.get('hits_F7free') and int(kv['hits_in_C']) == e.get('hits_in_C') and int(kv['max_min_covers']) == e.get('max_min_covers'))
        if not ok: problems += 1; print('COUNTER MISMATCH', k, (d, tp), summ, e)
        myconn += int(kv['connected_in_C']); hitfiles.append(outp)
        line.append('d=%d tp=%d inputs=%d hits=%s F7free=%s(%s) inC=%s(%s) connected_exact=%s maxcov=%s(%s)' % (d, tp, ni, kv['hits_all'], kv['hits_F7free'], e.get('hits_F7free'), kv['hits_in_C'], e.get('hits_in_C'), kv['connected_in_C'], kv['max_min_covers'], e.get('max_min_covers')))
    if myconn != info['connected_hits']: problems += 1; print('CONNECTED TOTAL MISMATCH', k, myconn, info['connected_hits'])
    isotxt = ''
    if 1 <= len(reps) <= 1000:
        hits = []
        for hf in hitfiles:
            for l in open(hf):
                if l.startswith('HIT conn=1'): hits.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
        buckets = {}
        for h in hits: buckets.setdefault(inv(h, n), []).append(h)
        found = 0
        for r in reps:
            key = inv(r, n); gr = inc(r, n); ok = False
            for h in buckets.get(key, []):
                if GraphMatcher(gr, inc(h, n), node_match=lambda a, b: a['side'] == b['side']).is_isomorphic(): ok = True; break
            found += ok
        isotxt = ' | prover reps found among my connected hits: %d/%d (hits %d)' % (found, len(reps), len(hits))
        if found != len(reps): problems += 1; print('REPRESENTATIVE NOT FOUND', k)
    print('CELL', k, 'classes', len(reps), 'connected_hits mine=%d prover=%d' % (myconn, info['connected_hits']), '; '.join(line), isotxt, '[%.0fs]' % (time.time() - t0), flush=True)
print('DONE new recursion cells:', cells_done, 'problems:', problems)
