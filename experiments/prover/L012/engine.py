"""(L012) Prover's recursive reconstruction engine (independent of the falsifier's engine.py; uses only the prover's programs:
enum_conn (L007), ext_d, filt, canon (nauty 2.8.8), and the decomposition generator of decomp22.py).

cell(n, m, t, D) = list of canonical representatives (one per isomorphism class) of the CONNECTED members X of C with n vertices,
m edges, tau(X) = t exactly and maximum degree <= D.  (C = linear, F7-free, e(S) <= |S|-2.)
 - m <= MD: direct enumeration `enum_conn n m t D` (every connected linear graph with tau >= t and max degree <= D, L007 Lemma D),
   then `filt` (linear, F7-free, (P3), tau == t exactly), then canonical forms.
 - m > MD: X has a vertex w of degree d = max degree, ceil(3m/n) <= d <= D.  X - w lies in C, has n-1 vertices, m-d edges, max degree
   <= d, tau(X - w) = tp in {t-1, t}; its components lie in C, have at most n-1 <= 21 vertices, hence slack >= 0 (I11, L011), with
   slacks adding to S' = 3(n-1)+2(m-d)-11 tp; so its component types form a decomposition of (n-1, m-d) of total slack S'
   (decomp22.gen1, isolated vertices included), each component being isomorphic to a member of cell(n_i, m_i, tau_i, d).  The d edges
   at w have pairwise disjoint pairs, not inside an edge of X - w, with endpoints of degree <= d-1 in X - w.  So X is isomorphic to a
   connected hit of `ext_d (n-1) tp t d (d-1)` on the disjoint unions of class representatives (multisets for repeated types) with
   tau(X) = t; these hits are filtered (C, connected on all n vertices, tau == t) and reduced to canonical forms.
Every cell is written to out/cells/cell_n_m_t_D.txt (canonical FOUND lines) and logged."""
import sys, os, re, math, itertools, subprocess, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp22 import slack_cells
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, 'bin'); OUT = os.path.join(HERE, 'out', 'cells'); os.makedirs(OUT, exist_ok=True)
ENUM = os.path.join(HERE, '..', 'L011', 'indep', 'enum_conn')
MD = 10; NPROC = int(os.environ.get('NPROC', '3'))
MEMO = {}; LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)
    with open(os.path.join(HERE, 'out', 'engine.log'), 'a') as f: f.write(s + '\n')
def parse_edges(l):
    return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def pieces(N, S):
    """component types (n, m, tau) with slack in [0, S]: connected cells (tau >= 1) and, if S >= 3, the isolated vertex."""
    P = [(n, m, t) for (n, m, t, s) in slack_cells(N, S) if t >= 1]
    if S >= 3: P.append((1, 0, 0))
    return P
def decompositions(N, M, S):
    P = pieces(N, S); sl = {p: 3 * p[0] + 2 * p[1] - 11 * p[2] for p in P}; sols = []
    def rec(i, n, m, s, ch):
        if n == N and m == M and s == S: sols.append(tuple(ch)); return
        if i == len(P): return
        p = P[i]; k = 0
        while n + k * p[0] <= N and m + k * p[1] <= M and s + k * sl[p] <= S:
            rec(i + 1, n + k * p[0], m + k * p[1], s + k * sl[p], ch + [p] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sols
def run(cmd, inp=None):
    r = subprocess.run(cmd, input=inp, capture_output=True, text=True, shell=isinstance(cmd, str))
    if r.returncode != 0: raise RuntimeError('command failed: %s\n%s' % (cmd, r.stderr[-2000:]))
    return r.stdout
def canon_lines(lines, nv):
    """canonical form strings (one per input line) via bin/canon."""
    if not lines: return []
    out = run([os.path.join(B, 'canon'), str(nv)], '\n'.join(lines) + '\n').splitlines()
    assert len(out) == len(lines), (len(out), len(lines))
    return out
def canon_to_edges(c):
    parts = c.split()[2:]
    return [tuple(map(int, p.split('.'))) for p in parts]
def dedupe(graph_lines, nv):
    """graph_lines: 'TAG: (a,b,c) ...' lines; returns canonical representatives (edge lists), one per isomorphism class."""
    keys = canon_lines(graph_lines, nv); seen = {}
    for k in keys:
        if k not in seen: seen[k] = canon_to_edges(k)
    return [seen[k] for k in sorted(seen)]
def save(key, reps, info):
    n, m, t, D = key
    with open(os.path.join(OUT, 'cell_%d_%d_%d_D%d.txt' % key), 'w') as f:
        for es in reps: f.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
        f.write('INFO ' + json.dumps(info) + '\n')
def load(key):
    p = os.path.join(OUT, 'cell_%d_%d_%d_D%d.txt' % key)
    if not os.path.exists(p): return None
    reps = []; done = False
    for l in open(p):
        if l.startswith('FOUND:'): reps.append(parse_edges(l))
        if l.startswith('INFO '): done = True
    return reps if done else None
def cell(n, m, t, D):
    key = (n, m, t, D)
    if key in MEMO: return MEMO[key]
    if (n, m) == (1, 0): MEMO[key] = [[]]; return MEMO[key]
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1:
        MEMO[key] = []; return []
    r = load(key)
    if r is not None: MEMO[key] = r; log('CELL', key, 'classes', len(r), '(loaded)'); return r
    t0 = time.time()
    if m <= MD: reps, info = direct(n, m, t, D)
    else: reps, info = recurse(n, m, t, D)
    info['secs'] = round(time.time() - t0, 1)
    save(key, reps, info); MEMO[key] = reps
    log('CELL', key, 'classes', len(reps), info)
    return reps
def direct(n, m, t, D):
    out = run('%s %d %d %d %d 1' % (ENUM, n, m, t, D))
    found = [l for l in out.splitlines() if l.startswith('FOUND:')]; last = out.strip().splitlines()[-1]
    f = run([os.path.join(B, 'filt'), 'FOUND', str(n), 'tau', str(t)], '\n'.join(found) + '\n')
    surv = [l.split(' #conn')[0] for l in f.splitlines() if l.startswith('SURVIVOR:')]
    summ = f.strip().splitlines()[-1]
    assert all(l.endswith('#conn=1') for l in f.splitlines() if l.startswith('SURVIVOR:'))
    reps = dedupe(surv, n)
    return reps, dict(route='direct', enum=last, labelled=len(found), in_C_tau_exact=len(surv), filt=summ)
def ext_parallel(inputs, NG, TG, T, d, EP, tag):
    """run ext_d on the input lines (split into NPROC chunks); returns the HIT lines and the summed counters."""
    inp = os.path.join(HERE, 'out', 'tmp_in_%s' % tag)
    chunks = [inputs[i::NPROC] for i in range(NPROC)] if len(inputs) >= 50 * NPROC else [inputs]
    procs = []
    for i, ch in enumerate(chunks):
        if not ch: continue
        fn = '%s_%d.txt' % (inp, i); open(fn, 'w').write('\n'.join(ch) + '\n')
        procs.append((fn, subprocess.Popen('%s %d %d %d %d %d < %s > %s.out' % (os.path.join(B, 'ext_d'), NG, TG, T, d, EP, fn, fn), shell=True)))
    hits = []; tot = {}
    for fn, p in procs:
        if p.wait() != 0: raise RuntimeError('ext_d failed ' + fn)
        for l in open(fn + '.out'):
            if l.startswith('HIT:'): hits.append(l.rstrip('\n'))
            elif l.startswith('SUMMARY'):
                for kv in l.split()[1:]:
                    k, v = kv.split('='); tot[k] = tot.get(k, 0) + int(v) if k != 'max_min_covers' else max(tot.get(k, 0), int(v))
        os.remove(fn); os.remove(fn + '.out')
    return hits, tot
def recurse(n, m, t, D):
    info = dict(route='recurse', branches=[]); allhits = []
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = decompositions(n - 1, m - d, Sp)
            inputs = []; dec_info = []
            for dec in decs:
                groups = {}
                for c in dec: groups[c] = groups.get(c, 0) + 1
                gl = []
                for typ, k in sorted(groups.items()):
                    cls = cell(typ[0], typ[1], typ[2], d)
                    gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), k))))
                size = 1
                for g in gl: size *= len(g[2])
                dec_info.append([list(dec), size])
                for combo in itertools.product(*[g[2] for g in gl]):
                    es = []; off = 0
                    for (typ, cls, _), idxs in zip(gl, combo):
                        for i in idxs:
                            es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                    assert off == n - 1
                    inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
            br = dict(d=d, tp=tp, Sp=Sp, decompositions=len(decs), inputs=len(inputs), dec=dec_info)
            if inputs:
                hits, tot = ext_parallel(inputs, n - 1, tp, t, d, d - 1, '%d_%d_%d_D%d_d%d_tp%d' % (n, m, t, D, d, tp))
                br['ext'] = tot
                if tot.get('bad_tau', 0): raise RuntimeError('bad_tau in %s' % br)
                allhits += [(tp, h) for h in hits]; br['hits_in_C'] = len(hits)
            info['branches'].append(br)
            log('  BRANCH', (n, m, t, D), 'd=%d tp=%d S\'=%d decompositions=%d inputs=%d' % (d, tp, Sp, len(decs), len(inputs)), br.get('ext', ''))
    # filter: in C (re-checked by filt), connected on all n vertices, and tau == t exactly.  For tp = t-1 the ext_d test gives
    # tau >= t and tau <= tau(G)+1 = t, so tau == t holds and is not recomputed ('notau'); for tp = t it is computed exactly.
    keep = []; info['filt'] = []
    for tpv, mode in ((t - 1, ['notau']), (t, ['tau', str(t)])):
        hl = [h for (tq, h) in allhits if tq == tpv]
        if not hl: continue
        f = run([os.path.join(B, 'filt'), 'HIT', str(n)] + mode, '\n'.join(hl) + '\n')
        keep += [l.split(' #conn')[0] for l in f.splitlines() if l.startswith('SURVIVOR:') and l.endswith('#conn=1')]
        info['filt'].append(f.strip().splitlines()[-1])
    info['connected_hits'] = len(keep)
    reps = dedupe(keep, n)
    return reps, info
if __name__ == '__main__':
    n, m, t, D = map(int, sys.argv[1:5])
    r = cell(n, m, t, D); print('RESULT', (n, m, t, D), len(r))
