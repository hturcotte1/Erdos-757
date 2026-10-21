"""Referee's own recomputation of cell(25,19,10,3), chunk by chunk (25,000 inputs, the worker's chunking), with own decompositions,
own input construction (decomposition order taken as DATA from the INFO line of the stored list; set of decompositions checked against
the own brute force), own extension program rext and nauty labelg.  For every chunk: class set compared with the worker's stored chunk
keys (out/chunks/25_19_10_D3_d3_tp9/cNNNNN.keys.gz, converted to graph6 and labelg).  At the end: union compared with the stored list.
usage: chunks25.py CELLDIR [first_chunk last_chunk]"""
import sys, os, time, json, gzip, subprocess, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = sys.argv[1]
c_lo, c_hi = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 10 ** 9)
WCH = '/home/user/Erdos-757/experiments/20261017-2150-i11-n27/out/chunks/25_19_10_D3_d3_tp9'
n, m, t, D, d, tp = 25, 19, 10, 3, 3, 9
Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
stored, info = rlib.read_cell(rlib.cell_path(CF, n, m, t, D))
br = [b for b in info['branches'] if b['d'] == d and b['tp'] == tp][0]
order = [tuple(tuple(x) for x in dec) for dec, size in br['dec']]
mine_decs = rlib.my_decomps(n - 1, m - d, Sp)
print('S\'=%d own decompositions=%d INFO decompositions=%d equal_as_sets=%s' % (Sp, len(mine_decs), len(order), sorted(tuple(sorted(x)) for x in order) == mine_decs), flush=True)
def gen():
    for dec in order:
        yield from rlib.inputs_for(tuple(sorted(dec)), CF, d, n - 1)
def worker_set(c):
    p = os.path.join(WCH, 'c%05d.keys.gz' % c)
    if not os.path.exists(p): return None
    lines = []
    for l in gzip.open(p, 'rt'):
        parts = l.split()
        if not parts: continue
        es = [tuple(map(int, x.split('.'))) for x in parts[2:]]
        assert len(es) == int(parts[1]) == m
        lines.append(es)
    return rlib.canon_set_of_reps(lines, n)
U = set(); CH = 25000; g = gen(); c = 0; t0 = time.time(); tot_in = 0; nsame = 0; ncmp = 0
while True:
    chunk = list(itertools.islice(g, CH))
    if not chunk: break
    tot_in += len(chunk)
    if c_lo <= c <= c_hi:
        t1 = time.time()
        s, summ, nout = rlib.run_ext(chunk, n - 1, tp, d, d - 1)
        U |= s
        w = worker_set(c); meta = json.load(open(os.path.join(WCH, 'c%05d.meta.json' % c)))
        same = (w == s); ncmp += 1; nsame += same
        print('chunk %2d inputs=%d mine_classes=%d mine_connected_in_C=%d worker_classes=%d worker_nsurv=%d equal=%s (%.1fs) | %s' % (
            c, len(chunk), len(s), nout, len(w) if w is not None else -1, meta['nsurv'], same, time.time() - t1, summ), flush=True)
    c += 1
st = rlib.canon_set_of_reps(stored, n)
print('TOTAL inputs=%d (INFO %d) chunks=%d compared=%d identical=%d' % (tot_in, br['inputs'], c, ncmp, nsame))
if c_lo == 0 and c_hi >= c - 1:
    print('RESULT cell(25,19,10,3): union of own chunks=%d stored=%d equal=%s (%.1fs)' % (len(U), len(st), U == st, time.time() - t0))
else:
    print('PARTIAL union=%d subset_of_stored=%s (%.1fs)' % (len(U), U <= st, time.time() - t0))
with open(os.path.join(rlib.R, 'out', 'mine_25_19_10_3_chunks_%d_%d.g6' % (c_lo, min(c_hi, c - 1))), 'w') as f: f.write('\n'.join(sorted(U)) + '\n')
