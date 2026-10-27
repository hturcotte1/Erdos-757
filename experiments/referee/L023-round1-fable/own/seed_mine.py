"""Referee L023 round 1 (fable): own seeding of engine/cells.
(1) refereed lists from the extracted tarballs L012/L013/L014/L016 (conflict check across certificates);
(2) the 12 twice-computed degree-3 lists: U1 copy must equal repro3/repro7 copy as a set of FOUND lines; then U1's copy is seeded;
(3) the 5 GAP lists of U1 are copied to own/u1_gap/ (NOT into cells/) with sha256, for later comparison."""
import glob, os, re, gzip, hashlib, shutil, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELLS = os.path.join(R, 'engine', 'cells')
U1 = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
L023 = '/home/user/Erdos-757/experiments/prover/L023'
def found_set(path):
    op = gzip.open if path.endswith('.gz') else open
    txt = op(path, 'rt').read()
    if 'INFO ' not in txt: return None, txt
    return frozenset(l for l in txt.splitlines() if l.startswith('FOUND:')), txt
seen = {}; conflicts = 0; n = 0
for src in ('L012', 'L013', 'L014', 'L016'):
    for p in sorted(glob.glob(os.path.join(R, 'seed', src, '**', 'cell_*.txt*'), recursive=True)):
        m = re.search(r'(cell_\d+_\d+_\d+_D\d+\.txt)(\.gz)?$', p); name = m.group(1)
        F, txt = found_set(p)
        if F is None: print('no INFO, skipped', p); continue
        if name in seen:
            if seen[name][0] != F: conflicts += 1; print('CONFLICT', name, p, seen[name][1])
            continue
        seen[name] = (F, p)
        with open(os.path.join(CELLS, name), 'w') as f: f.write(txt if txt.endswith('\n') else txt + '\n')
        n += 1
print('refereed lists seeded', n, 'conflicts', conflicts)
twice = ['22_14_8_D3','21_11_7_D3','11_5_3_D3','8_4_2_D3','5_3_1_D3','19_13_7_D3','16_12_6_D3','13_11_5_D3','18_10_6_D3','15_9_5_D3','12_8_4_D3','9_7_3_D3']
gap = ['24_20_10_D3','23_17_9_D3','21_19_9_D3','20_16_8_D3','17_15_7_D3']
for k in twice + gap:
    assert not os.path.exists(os.path.join(CELLS, 'cell_%s.txt' % k)), 'unexpectedly refereed: ' + k
ok = 0
for k in twice:
    u1 = os.path.join(U1, 'cell_%s.txt' % k); Fu, txt = found_set(u1)
    reps = [os.path.join(L023, d, 'cells', 'cell_%s.txt' % k) for d in ('repro3', 'repro7')]
    reps = [p for p in reps if os.path.exists(p)]
    assert reps, 'no repro copy for ' + k
    for p in reps:
        Fr, _ = found_set(p)
        assert Fr is not None and Fr == Fu, 'MISMATCH %s vs %s' % (u1, p)
    with open(os.path.join(CELLS, 'cell_%s.txt' % k), 'w') as f: f.write(txt)
    ok += 1; print('twice-computed list %-12s U1 == %s : %d classes, seeded' % (k, ','.join(os.path.basename(os.path.dirname(os.path.dirname(p))) for p in reps), len(Fu)))
os.makedirs(os.path.join(R, 'own', 'u1_gap'), exist_ok=True)
for k in gap:
    u1 = os.path.join(U1, 'cell_%s.txt' % k); Fu, txt = found_set(u1)
    shutil.copy(u1, os.path.join(R, 'own', 'u1_gap', 'cell_%s.txt' % k))
    print('GAP list %-12s U1 classes %7d sha256 %s' % (k, len(Fu), hashlib.sha256(open(u1,'rb').read()).hexdigest()[:16]))
print('cells dir has', len(os.listdir(CELLS)), 'lists')
