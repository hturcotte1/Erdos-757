"""Referee L013 r1: an independent bottom-up cell engine (does NOT read the prover's files or programs).
cell(n,m,t,D) = class representatives of connected members of C with (n,m,t) and max degree <= D.
 - leaves (m <= 10): unmodified genbg with the tau-only PRUNE1 hook (bin/genbg_tprune) + own filter bin/hfilt (genbg outputs one
   graph per isomorphism class, so the survivors are the class list);
 - m >= 11: vertex-deletion at a vertex of maximum degree d (ceil(3m/n) <= d <= D), tau(X-w) = tp in {t-1, t} with
   S' = 3(n-1)+2(m-d)-11tp >= 0 (I11 below n, the induction hypothesis), decompositions by src/decomp_ref.py, component lists by
   recursion with bound d, inputs = disjoint unions (multisets), extensions by bin/myext4 (all d-sets of disjoint admissible pairs
   with tau(X) >= t, i.e. = t; connected, in C, Delta <= D), reduction to classes by networkx VF2 (src/iso_compare.py).
Lists are cached in out/myeng/ (and lists already produced by genbg in out/gmine/ are reused)."""
import sys, os, re, math, itertools, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from decomp_ref import decomps
from iso_compare import inc, key, iso
OUT = os.path.join(ROOT, 'out', 'myeng'); os.makedirs(OUT, exist_ok=True)
GM = os.path.join(ROOT, 'out', 'gmine')
LOG = open(os.path.join(ROOT, 'logs', 'myengine.log'), 'a')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
def parse(fn):
    L = []; done = False
    for l in open(fn):
        if l.startswith('FOUND') or l.startswith('HIT'): L.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)])
        if l.startswith('SUMMARY'): done = True
    return L if done else None
MEMO = {}
def save(k, reps, note):
    with open(os.path.join(OUT, 'cell_%d_%d_%d_D%d.txt' % k), 'w') as f:
        for es in reps: f.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
        f.write('SUMMARY %s\n' % note)
def reduce_classes(nv, L):
    buckets = {}; reps = []
    for es in L:
        G = inc(nv, es); h = key(G)
        if any(iso(G, H) for H in buckets.get(h, [])): continue
        buckets.setdefault(h, []).append(G); reps.append(es)
    return reps
def cell(n, m, t, D):
    k = (n, m, t, D)
    if k in MEMO: return MEMO[k]
    if (n, m, t) == (1, 0, 0): MEMO[k] = [[]]; return MEMO[k]
    if m < 1 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 3 * m > D * n:
        MEMO[k] = []; return []
    for d in (OUT, GM):
        fn = os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % k)
        if os.path.exists(fn):
            r = parse(fn)
            if r is not None: MEMO[k] = r; return r
    t0 = time.time()
    if m <= 10:
        cmd = 'PRUNE_T=%d %s/bin/genbg_tprune -q -c -Z1 -d1:3 -D%d:3 %d %d %d:%d | %s/bin/hfilt %d %d %d %d print' % (t, ROOT, D, n, m, 3 * m, 3 * m, ROOT, n, m, t, D)
        out = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True).stdout
        reps = [[tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in out.splitlines() if l.startswith('FOUND')]
        note = 'leaf genbg_tprune+hfilt ' + out.strip().splitlines()[-1]
    else:
        hits = []; notes = []
        for d in range(max(1, math.ceil(3 * m / n)), D + 1):
            for tp in (t - 1, t):
                Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
                if Sp < 0 or tp < 0: continue
                lines = []
                for dec in decomps(n - 1, m - d, Sp):
                    groups = {}
                    for c in dec: groups[c] = groups.get(c, 0) + 1
                    gl = [(typ, cell(typ[0], typ[1], typ[2], d), kk) for typ, kk in sorted(groups.items())]
                    for combo in itertools.product(*[list(itertools.combinations_with_replacement(range(len(L)), kk)) for (typ, L, kk) in gl]):
                        es = []; off = 0
                        for (typ, L, kk), idxs in zip(gl, combo):
                            for i in idxs: es += [tuple(v + off for v in e) for e in L[i]]; off += typ[0]
                        lines.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
                if not lines: notes.append('d=%d tp=%d S=%d inputs=0' % (d, tp, Sp)); continue
                r = subprocess.run([os.path.join(ROOT, 'bin', 'myext4'), str(n - 1), str(t), str(d), str(D), 'e'], input='\n'.join(lines) + '\n', capture_output=True, text=True)
                if r.returncode != 0: raise RuntimeError('myext4 failed %s %s' % (k, r.stderr[-500:]))
                summ = r.stdout.strip().splitlines()[-1]
                if 'bad_tau_G=0' not in summ: raise RuntimeError('bad tau in %s: %s' % (k, summ))
                hits += [[tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in r.stdout.splitlines() if l.startswith('HIT')]
                notes.append('d=%d tp=%d S=%d inputs=%d %s' % (d, tp, Sp, len(lines), summ.replace('SUMMARY ', '')))
        reps = reduce_classes(n, hits)
        note = 'recursion connected_hits=%d | ' % len(hits) + ' | '.join(notes)
    save(k, reps, note + ' secs=%.1f' % (time.time() - t0)); MEMO[k] = reps
    log('CELL', k, 'classes', len(reps), 'secs %.1f' % (time.time() - t0), note[:300])
    return reps
if __name__ == '__main__':
    a = list(map(int, sys.argv[1:]))
    for i in range(0, len(a), 4):
        k = tuple(a[i:i + 4]); r = cell(*k); log('RESULT', k, len(r))
