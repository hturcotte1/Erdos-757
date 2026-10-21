"""Referee regression: prover's ext_d_fast against L012's ext_d (MAXP 256) and the worker's MAXP-640 rebuild, on the referee's own
inputs (real branch inputs built by rlib from the cell lists, and random linear 3-graphs with true/wrong TG, various T, d, EP,
noprune).  Compares exit codes and stdout byte for byte, per group file."""
import sys, os, random, subprocess, time, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
FAST = '/home/user/Erdos-757/experiments/prover/L016/bin/ext_d_fast'
G256 = '/home/user/Erdos-757/experiments/prover/L012/bin/ext_d'
G640 = '/home/user/Erdos-757/experiments/20261017-2150-i11-n27/bin/ext_d'
CF = '/home/user/Erdos-757/experiments/prover/L016/out/cellsF'
OUT = os.path.join(rlib.R, 'out', 'regress'); os.makedirs(OUT, exist_ok=True)
rng = random.Random(20261021 + 2)
def run(binp, args, fn):
    with open(fn) as f:
        r = subprocess.run(['nice', '-n', '10', binp] + [str(a) for a in args], stdin=f, capture_output=True)
    return r.returncode, r.stdout
def npairs(line, NG, EP):
    v = list(map(int, line.split())); m = v[0]; E = [tuple(v[1 + 3 * i:4 + 3 * i]) for i in range(m)]
    deg = [0] * NG; inside = set()
    for e in E:
        for x in e: deg[x] += 1
        for i in range(3):
            for j in range(i + 1, 3): inside.add((min(e[i], e[j]), max(e[i], e[j])))
    return sum(1 for a in range(NG) for b in range(a + 1, NG) if deg[a] <= EP and deg[b] <= EP and (a, b) not in inside)
results = []; ninputs = 0
def group(name, lines, args, use256):
    global ninputs
    fn = os.path.join(OUT, name + '.in'); open(fn, 'w').write('\n'.join(lines) + '\n')
    t0 = time.time()
    rf = run(FAST, args, fn); r6 = run(G640, args, fn)
    same640 = rf == r6
    msg = 'group %-28s inputs=%5d args=%s fast_rc=%d 640_rc=%d identical_fast_vs_640=%s' % (name, len(lines), ' '.join(map(str, args)), rf[0], r6[0], same640)
    if use256:
        r2 = run(G256, args, fn); msg += ' 256_rc=%d identical_fast_vs_256=%s' % (r2[0], rf == r2)
        same = same640 and rf == r2
    else: same = same640
    lastline = rf[1].decode().strip().splitlines()[-1] if rf[1] else ''
    msg += ' bytes=%d hits=%d | %s (%.1fs)' % (len(rf[1]), rf[1].count(b'HIT:'), lastline, time.time() - t0)
    print(msg, flush=True); results.append(same); ninputs += len(lines)
# ---- real inputs of the four heavy cells / top cell (own construction from the stored lists)
def real_inputs(n, m, t, d):
    tp = t - 1; Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp; L = []
    for dec in rlib.my_decomps(n - 1, m - d, Sp):
        try: L += list(rlib.inputs_for(dec, CF, d, n - 1))
        except FileNotFoundError: pass
    return L
for (n, m, t, k) in [(24, 16, 9, 600), (25, 19, 10, 500), (26, 22, 11, 400), (27, 25, 12, 334)]:
    L = real_inputs(n, m, t, 3); smp = rng.sample(L, min(k, len(L)))
    use256 = all(npairs(l, n - 1, 2) < 256 for l in smp)
    if not use256:
        ok = [l for l in smp if npairs(l, n - 1, 2) < 256]; big = [l for l in smp if npairs(l, n - 1, 2) >= 256]
        print('   (%d,%d,%d): %d of %d sampled inputs have >= 256 admissible pairs' % (n, m, t, len(big), len(smp)))
        group('real_%d_%d_%d_P<256' % (n, m, t), ok, [n - 1, t - 1, t, 3, 2], True)
        group('real_%d_%d_%d_P>=256' % (n, m, t), big, [n - 1, t - 1, t, 3, 2], False)
    else:
        group('real_%d_%d_%d' % (n, m, t), smp, [n - 1, t - 1, t, 3, 2], True)
    if n <= 25:
        group('real_%d_%d_%d_noprune' % (n, m, t), smp[:150], [n - 1, t - 1, t, 3, 2, 'noprune'], all(npairs(l, n - 1, 2) < 256 for l in smp[:150]))
# ---- random linear 3-graphs
def rand_graph(NG, m, maxdeg):
    E = []; deg = [0] * NG; tries = 0
    while len(E) < m and tries < 5000:
        tries += 1; e = tuple(sorted(rng.sample(range(NG), 3)))
        if any(deg[x] >= maxdeg for x in e): continue
        if any(len(set(e) & set(f)) > 1 for f in E): continue
        E.append(e)
        for x in e: deg[x] += 1
    rng.shuffle(E)
    return E
def tau_of(lines):
    r = subprocess.run([rlib.REXT, 'filt', '31', '9', 'raw'], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True)
    return [int(l.split()[2]) for l in r.stdout.split('\n') if l.strip()]
for gi in range(16):
    NG = rng.choice([10, 12, 14, 16, 18, 20, 21, 22, 23, 24, 25, 26]); maxdeg = rng.choice([2, 3, 3, 4])
    d = rng.choice([1, 2, 3]); EP = rng.choice([1, 2, 2, 3]); mode = rng.choice(['T=TG+1'] * 5 + ['T=TG', 'T=TG+2'])
    if mode == 'T=TG': NG = rng.choice([8, 10, 12]); d = rng.choice([1, 2])
    graphs = []
    for _ in range(60):
        m = rng.randint(max(1, NG // 3), min(NG - 2, 24)); graphs.append(rand_graph(NG, m, maxdeg))
    lines = ['%d ' % len(E) + ' '.join('%d %d %d' % e for e in E) for E in graphs]
    taus = tau_of(lines)
    # one TG per group (the programs take TG on the command line): use the most common tau; others become bad_tau inputs
    TG = max(set(taus), key=taus.count)
    if TG < 2: TG = 2
    T = TG + 1 if mode == 'T=TG+1' else (TG if mode == 'T=TG' else TG + 2)
    args = [NG, TG, T, d, EP] + (['noprune'] if rng.random() < 0.25 else [])
    use256 = all(npairs(l, NG, EP) < 256 for l in lines)
    print('   random group %d: NG=%d maxdeg=%d taus=%s' % (gi, NG, maxdeg, sorted(set(taus))))
    group('rand_%02d' % gi, lines, args, use256)
print('TOTAL inputs %d groups %d all_identical=%s' % (ninputs, len(results), all(results)))
