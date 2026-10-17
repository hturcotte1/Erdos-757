"""Referee (L013 round 2) independent bottom-up engine.
cell(n,m,t,D) = canonical representatives (labelg on incidence graphs, partition points|edges) of the connected X in C with n vertices,
m edges, tau = t, maxdeg <= D.
 - m <= MD (10): base lists = the prover's DIRECT lists (enum_conn, L007 Lemma D, accepted), every representative re-verified by refx
   (linear, connected, F7-free, (P3), tau == t, maxdeg <= D) and re-canonicalised by labelg; Delta<=2 base cells are independently
   complete by dual_d2.py; some Delta<=3 base cells are independently checked by genbgL (genbg_cells.sh).
 - m > MD: own recursion: max-degree vertex w, d in [ceil(3m/n), D], tp in {t-1, t} with S' >= 0, own decompositions (decomp_ref),
   inputs = disjoint unions of MY lists (multisets), own extension program (refx ext, MIS-containment search), GOOD = connected,
   in C, tau == t exactly, maxdeg <= d; then labelg reduction.
Guards (necessary for a connected member of C with m >= 1): n <= 2m+1, m <= n-2, 1 <= t <= m, 17t <= 5n+3m (K8), D >= 1."""
import sys, os, re, math, itertools, subprocess, json, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from decomp_ref import decomps
BIN = os.path.join(HERE, 'bin'); OUT = os.path.join(HERE, 'out', 'mycells'); os.makedirs(OUT, exist_ok=True)
PROVER = os.path.join(HERE, 'out', 'prover_cells', 'cells')
MD = 10; NPROC = int(os.environ.get('NPROC', '2'))
MEMO = {}
LOGF = open(os.path.join(HERE, 'out', 'myengine.log'), 'a')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
def g6(n, m, es):
    N = n + m; adj = set()
    for j, e in enumerate(es):
        for v in e: adj.add((v, n + j))
    bits = []
    for j in range(1, N):
        for i in range(j):
            bits.append(1 if (i, j) in adj or (j, i) in adj else 0)
    while len(bits) % 6: bits.append(0)
    s = chr(63 + N) if N <= 62 else None
    assert s is not None
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]: v = 2 * v + b
        s += chr(63 + v)
    return s
def from_g6(s, n, m):
    N = ord(s[0]) - 63; assert N == n + m
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        for k in range(5, -1, -1): bits.append((v >> k) & 1)
    nb = {i: [] for i in range(N)}; k = 0
    for j in range(1, N):
        for i in range(j):
            if bits[k]: nb[i].append(j); nb[j].append(i)
            k += 1
    es = []
    for j in range(n, N):
        assert all(v < n for v in nb[j]) and len(nb[j]) == 3
        es.append(tuple(sorted(nb[j])))
    for i in range(n): assert all(v >= n for v in nb[i])
    return sorted(es)
def canon(n, m, list_of_es):
    if not list_of_es: return []
    inp = ''.join(g6(n, m, es) + '\n' for es in list_of_es)
    r = subprocess.run([os.path.join(BIN, 'labelg'), '-q', '-f' + 'a' * n + 'b' * m], input=inp, capture_output=True, text=True)
    out = r.stdout.split()
    assert len(out) == len(list_of_es), (len(out), len(list_of_es), r.stderr[-500:])
    return out
def check(n, list_of_es):
    if not list_of_es: return []
    inp = ''.join('X: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n' for es in list_of_es)
    out = subprocess.run([os.path.join(BIN, 'refx'), 'check', str(n)], input=inp, capture_output=True, text=True).stdout.splitlines()
    res = [{k: int(v) for k, v in (kv.split('=') for kv in l.split()[1:])} for l in out]
    assert len(res) == len(list_of_es)
    return res
def parse_edges(l): return [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def save(key, cforms, info):
    with open(os.path.join(OUT, 'mycell_%d_%d_%d_D%d.txt' % key), 'w') as f:
        for c in cforms: f.write('C ' + c + '\n')
        f.write('INFO ' + json.dumps(info) + '\n')
def load(key):
    p = os.path.join(OUT, 'mycell_%d_%d_%d_D%d.txt' % key)
    if not os.path.exists(p): return None
    cf = []; done = False
    for l in open(p):
        if l.startswith('C '): cf.append(l.split()[1])
        if l.startswith('INFO '): done = True
    return cf if done else None
def reps_of(key):
    n, m, t, D = key
    return [from_g6(c, n, m) for c in cell(*key)]
def cell(n, m, t, D):
    key = (n, m, t, D)
    if key in MEMO: return MEMO[key]
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1:
        MEMO[key] = []; return []
    r = load(key)
    if r is not None: MEMO[key] = r; return r
    t0 = time.time()
    if m <= MD:
        p = os.path.join(PROVER, 'cell_%d_%d_%d_D%d.txt' % key)
        if not os.path.exists(p): raise RuntimeError('base cell missing in prover dir: %s' % (key,))
        reps = [parse_edges(l) for l in open(p) if l.startswith('FOUND:')]
        for c in check(n, reps):
            assert c['m'] == m and c['linear'] == 1 and c['connected'] == 1 and c['F7'] == 0 and c['P3'] == 1 and c['tau'] == t and c['maxdeg'] <= D, (key, c)
        cf = sorted(set(canon(n, m, reps)))
        assert len(cf) == len(reps), ('prover base list has isomorphic duplicates', key)
        info = dict(route='base(prover direct list, re-verified)', classes=len(cf))
    else:
        info = dict(route='recursion', branches=[]); good = []
        for d in range(max(1, -(-3 * m // n)), D + 1):
            for tp in (t - 1, t):
                Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
                if Sp < 0 or tp < 0: continue
                inputs = []; decinfo = []
                for dec in decomps(n - 1, m - d, Sp):
                    c = Counter(dec); groups = []
                    for typ in sorted(c):
                        L = [[]] if typ == (1, 0, 0) else reps_of(typ + (d,))
                        groups.append((typ, L, c[typ]))
                    choices = [list(itertools.combinations_with_replacement(range(len(L)), k)) for (typ, L, k) in groups]
                    k0 = 0
                    for combo in itertools.product(*choices):
                        es = []; off = 0
                        for (typ, L, k), idxs in zip(groups, combo):
                            for i in idxs:
                                es += [tuple(v + off for v in e) for e in L[i]]; off += typ[0]
                        assert off == n - 1
                        inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es)); k0 += 1
                    decinfo.append((list(dec), k0))
                br = dict(d=d, tp=tp, Sp=Sp, decompositions=len(decinfo), inputs=len(inputs))
                if inputs:
                    chunks = [inputs[i::NPROC] for i in range(NPROC)] if len(inputs) >= 20 * NPROC else [inputs]
                    procs = []
                    for i, ch in enumerate(chunks):
                        fn = os.path.join(OUT, 'tmp_%d_%d_%d_%d_%d_%d_%d.txt' % (key + (d, tp, i)))
                        open(fn, 'w').write('\n'.join(ch) + '\n')
                        procs.append((fn, subprocess.Popen('nice -n 10 %s ext %d %d %d %d %d < %s > %s.out' % (os.path.join(BIN, 'refx'), n - 1, tp, t, d, d - 1, fn, fn), shell=True)))
                    summ = Counter()
                    for fn, pr in procs:
                        if pr.wait() != 0: raise RuntimeError('refx failed ' + fn)
                        for l in open(fn + '.out'):
                            if l.startswith('GOOD:'): good.append(parse_edges(l))
                            elif l.startswith('SUMMARY'):
                                for kv in l.split()[2:]:
                                    k_, v_ = kv.split('=')
                                    if k_ in ('inputs', 'badtau', 'hits', 'taufail', 'f7free', 'inC', 'connected', 'GOOD'): summ[k_] += int(v_)
                        os.remove(fn); os.remove(fn + '.out')
                    if summ['badtau'] or summ['taufail']: raise RuntimeError('badtau/taufail %s %s' % (key, dict(summ)))
                    assert summ['inputs'] == len(inputs)
                    br['ext'] = dict(summ)
                info['branches'].append(br)
        cf = sorted(set(canon(n, m, good))) if good else []
        info['good_labelled'] = len(good); info['classes'] = len(cf)
    info['secs'] = round(time.time() - t0, 1)
    save(key, cf, info); MEMO[key] = cf
    log('CELL', key, len(cf), json.dumps(info)[:400])
    return cf
if __name__ == '__main__':
    a = list(map(int, sys.argv[1:]))
    for i in range(0, len(a), 4):
        key = tuple(a[i:i + 4]); r = cell(*key); log('TOP', key, len(r))
