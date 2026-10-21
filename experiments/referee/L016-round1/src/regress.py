#!/usr/bin/env python3
"""Referee L016 round 1 (own code): byte-level regression of ext_d_fast against the Gosper builds of ext_d.
Builds compared (all run on identical stdin with identical arguments; stdout bytes and exit codes compared):
  FAST = prover L016 bin/ext_d_fast, G640W = worker's MAXP-640 rebuild, G640P = prover's bin/ext_d (MAXP 640),
  G256 = L012's original ext_d (MAXP 256; expected to stop with exit code 4 when an input has more than 256 pairs).
Inputs: (a) random lines of given input files (one batch per parameter set); (b) random linear 3-graphs (own generator),
each run separately with random parameters (NG, TG in {tau-1, tau, tau+1}, T in {TG, TG+1, TG+2}, d, EP, prune/noprune)."""
import random, subprocess, sys, json, os

FAST = '/home/user/Erdos-757/experiments/prover/L016/bin/ext_d_fast'
G640W = '/home/user/Erdos-757/experiments/20261017-2150-i11-n27/bin/ext_d'
G640P = '/home/user/Erdos-757/experiments/prover/L016/bin/ext_d'
G256 = '/home/user/Erdos-757/experiments/prover/L012/bin/ext_d'
MYTAU = '/home/user/Erdos-757/experiments/referee/L016-round1/bin/mytau'
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 20261021)
mode = sys.argv[1]

def run(binary, args, inp):
    p = subprocess.run([binary] + [str(a) for a in args], input=inp.encode(), capture_output=True, timeout=3600)
    return p.returncode, p.stdout

def compare(args, inp, builds):
    res = {name: run(b, args, inp) for name, b in builds}
    ref = res[builds[0][0]]
    same = {name: (r == ref) for name, r in res.items()}
    return ref, res, same

def rand_linear(n, mt):
    edges = []; pairs = set(); tries = 0
    while len(edges) < mt and tries < 5000:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        ps = {(e[0], e[1]), (e[0], e[2]), (e[1], e[2])}
        if ps & pairs:
            continue
        pairs |= ps; edges.append(e)
    rng.shuffle(edges)
    return edges

if mode == 'file':
    # regress.py file seed infile k NG TG T d EP [noprune]
    infile, k = sys.argv[3], int(sys.argv[4]); args = sys.argv[5:]
    lines = open(infile).read().splitlines()
    sample = rng.sample(lines, min(k, len(lines)))
    inp = '\n'.join(sample) + '\n'
    builds = [('FAST', FAST), ('G640W', G640W), ('G640P', G640P)]
    ref, res, same = compare(args, inp, builds)
    hits = ref[1].count(b'HIT:')
    summ = [l for l in ref[1].decode().splitlines() if l.startswith('SUMMARY')]
    r256 = run(G256, args, inp)
    print('FILE %s inputs=%d args=%s rc=%d HITlines=%d identical(FAST,G640W,G640P)=%s | G256 rc=%d identical=%s | %s' % (
        os.path.basename(infile), len(sample), ' '.join(args), ref[0], hits, all(same.values()), r256[0], r256 == ref, summ[-1] if summ else ''))
elif mode == 'random':
    # regress.py random seed count
    count = int(sys.argv[3]); nsame = 0; ndiff = 0; n256_4 = 0; n256_same = 0; stats = {}
    for it in range(count):
        while True:   # random linear 3-graph without isolated vertices, m between ceil(NG/2) and NG-2
            NG = rng.choice([8, 10, 12, 14, 16, 18, 20, 22, 23, 24, 24, 25, 25, 25])
            mt = rng.randint((NG + 1) // 2, NG - 2)
            G = rand_linear(NG, mt)
            if len({v for e in G for v in e}) == NG:
                break
        line = '%d %s\n' % (len(G), ' '.join('%d %d %d' % e for e in G))
        tau = int(subprocess.run([MYTAU], input=line.encode(), capture_output=True).stdout.split()[0])
        TG = tau if rng.random() < 0.8 else max(2, tau + rng.choice([-1, 1]))
        TG = max(TG, 2)
        T = TG + rng.choice([1, 1, 1, 0, 2])
        d = rng.choice([1, 2, 2, 3, 3, 3])
        EP = rng.choice([1, 2, 2, 3])
        args = [NG, TG, T, d, EP]
        if T == TG and d > 1:
            d = 1; args[3] = 1          # TG >= T: every d-set is a hit; keep the output small
        if rng.random() < 0.3:
            args.append('noprune')
        ref, res, same = compare(args, line, [('FAST', FAST), ('G640W', G640W), ('G640P', G640P)])
        r256 = run(G256, args, line)
        if all(same.values()):
            nsame += 1
        else:
            ndiff += 1; print('DIFF', args, line.strip(), {k: (v[0], len(v[1])) for k, v in res.items()})
        if r256[0] == 4:
            n256_4 += 1
        elif r256 == ref:
            n256_same += 1
        else:
            print('G256 DIFF (rc %d)' % r256[0], args, line.strip())
        if (it + 1) % 50 == 0:
            print('progress', it + 1, nsame, ndiff, flush=True)
        key = 'NG%d' % NG
        stats[key] = stats.get(key, 0) + 1
        stats['hits'] = stats.get('hits', 0) + ref[1].count(b'HIT:')
        stats['rc%d' % ref[0]] = stats.get('rc%d' % ref[0], 0) + 1
        s = [l for l in ref[1].decode().splitlines() if l.startswith('SUMMARY')]
        if s and 'bad_tau=1' in s[-1]:
            stats['bad_tau'] = stats.get('bad_tau', 0) + 1
        if s and 'tg_too_small=1' in s[-1]:
            stats['tg_too_small'] = stats.get('tg_too_small', 0) + 1
    print('RANDOM count=%d identical(FAST,G640W,G640P)=%d different=%d | G256: exit4(MAXP)=%d identical=%d | %s' % (
        count, nsame, ndiff, n256_4, n256_same, json.dumps(stats, sort_keys=True)))
