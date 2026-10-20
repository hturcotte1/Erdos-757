"""Referee L014 round 2: own bottom-up engine (shares no code with the prover's engine.py / stream.py / binaries).
mycell(n,m,t,D) = one representative per isomorphism class of the CONNECTED members of C (linear, F7-free, (P3)) with n vertices,
m edges, tau = t, max degree <= D.
 * trivial: (1,0) -> isolated vertex; empty if m = 0 (n > 1), t < 1, t > m, n > 2m+1, m > n-2 or D < 1 (no Henning-Yeo guard);
 * m <= MDIR: unmodified nauty genbg (own build) on incidence graphs: -c (connected) -Z1 (two edges share <= 1 vertex)
   -d1:3 -D<D>:3 (vertex degrees 1..D, edge degree 3), 3m bipartite edges; then bin/gfilt (own classifier) keeps the members with
   tau == t; genbg outputs one graph per colour-preserving isomorphism class, so this list is complete and irredundant;
 * m > MDIR: X has a vertex w of degree d = Delta(X) >= ceil(3m/n); X - w has n-1 vertices, m-d edges, tau' in {t-1,t},
   components = connected members of C with <= n-1 <= 22 vertices (I11 slack >= 0 by L011) or isolated vertices;
   decompositions by arith_decomp.decomps_bf (no K8); inputs = multisets of representatives of mycell(n_i,m_i,tau_i,d);
   bin/myext enumerates every extension by w with d pairwise disjoint pairs (not inside an edge, endpoints of degree <= d-1),
   tau(H) >= t, and prints the connected members of C (own classifier); keep tau == t; reduce by labelg canonical forms.
usage: python3 myengine.py n m t D [MDIR]"""
import sys, os, itertools, subprocess, time, json
from math import ceil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arith_decomp import decomps_bf
from canon_cmp import canon
NB = os.path.join(HERE, 'out', 'nbin'); MYB = os.path.join(HERE, 'bin')
OUT = os.environ.get('MYCELLS', os.path.join(HERE, 'out', 'mycells')); os.makedirs(OUT, exist_ok=True)
MDIR = int(os.environ.get('MDIR', '11'))
LOG = os.path.join(HERE, 'out', 'myengine.log')
MEMO = {}
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True)
    with open(LOG, 'a') as f: f.write(s + '\n')
def fname(key): return os.path.join(OUT, 'cell_%d_%d_%d_D%d.txt' % key)
def save(key, reps, info):
    with open(fname(key), 'w') as f:
        for es in reps: f.write('%d %d ' % (key[0], len(es)) + ' '.join('%d %d %d' % e for e in es) + '\n')
        f.write('#DONE ' + json.dumps(info) + '\n')
def load(key):
    if not os.path.exists(fname(key)): return None
    reps = []; done = False
    for l in open(fname(key)):
        if l.startswith('#DONE'): done = True; continue
        a = list(map(int, l.split())); reps.append([tuple(a[2 + 3*i: 5 + 3*i]) for i in range(a[1])])
    return reps if done else None
def parse_lines(txt, n, m):
    out = []
    for l in txt.splitlines():
        if l.startswith('MEMBER'):
            head, body = l.split(':', 1); fl = dict(kv.split('=') for kv in head.split()[1:])
            a = list(map(int, body.split())); out.append((int(fl['tau']), [tuple(a[2 + 3*i: 5 + 3*i]) for i in range(a[1])]))
        elif l[:1].isdigit():
            a = list(map(int, l.split())); out.append((None, [tuple(a[2 + 3*i: 5 + 3*i]) for i in range(a[1])]))
    for t, es in out: assert len(es) == m
    return out
def direct(n, m, t, D):
    gb = 'genbg' if (n + m <= 32 and n <= 24) else 'genbgL'
    cmd = "%s/%s -q -c -Z1 -d1:3 -D%d:3 %d %d %d:%d | %s/gfilt2 %d %d 1 1" % (NB, gb, D, n, m, 3*m, 3*m, MYB, n, t)
    r = subprocess.run(['bash', '-c', 'set -o pipefail; ' + cmd], capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError('direct failed %s: %s' % (cmd, r.stderr[-500:]))
    reps = [es for _, es in parse_lines(r.stdout, n, m)]
    return reps, dict(route='genbg', gfilt=r.stderr.strip().splitlines()[-1])
def recurse(n, m, t, D):
    info = dict(route='recursion', branches=[]); members = []
    for d in range(max(1, ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = decomps_bf(n - 1, m - d, Sp, False)
            lines = []; dinfo = []
            for dec in decs:
                groups = {}
                for c in dec: groups[c] = groups.get(c, 0) + 1
                gl = []
                for typ in sorted(groups):
                    cls = mycell(typ[0], typ[1], typ[2], d)
                    gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), groups[typ]))))
                cnt = 0
                for combo in itertools.product(*[g[2] for g in gl]):
                    es = []; off = 0
                    for (typ, cls, _), idxs in zip(gl, combo):
                        for i in idxs: es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                    assert off == n - 1 and len(es) == m - d
                    lines.append('%d %d ' % (n - 1, len(es)) + ' '.join('%d %d %d' % e for e in es)); cnt += 1
                dinfo.append([list(dec), cnt])
            br = dict(d=d, tp=tp, Sp=Sp, decompositions=len(decs), inputs=len(lines), dec=dinfo)
            if lines:
                r = subprocess.run([os.path.join(MYB, 'myext'), str(tp), str(t), str(d), str(d - 1), '2', '1'], input='\n'.join(lines) + '\n',
                                   capture_output=True, text=True)
                if r.returncode != 0: raise RuntimeError('myext failed')
                summ = [l for l in r.stdout.splitlines() if l.startswith('SUMMARY')]; assert len(summ) == 1
                if 'bad_tau=0' not in summ[0] or 'bad_deg=0' not in summ[0] or 'bad_input=0' not in summ[0]: raise RuntimeError('bad input ' + summ[0])
                got = parse_lines(r.stdout, n, m)
                keep = [es for tau, es in got if tau == t]
                br['myext'] = summ[0]; br['members_tau_eq_t'] = len(keep); members += keep
            info['branches'].append(br)
            log('  BRANCH', (n, m, t, D), 'd=%d tp=%d Sp=%d decs=%d inputs=%d' % (d, tp, Sp, len(decs), len(lines)), br.get('myext', ''))
    if not members: return [], info
    cf = canon(n, m, members); seen = {}
    for c, es in zip(cf, members):
        if c not in seen: seen[c] = es
    info['connected_members'] = len(members)
    return [seen[c] for c in sorted(seen)], info
def mycell(n, m, t, D):
    key = (n, m, t, D)
    if key in MEMO: return MEMO[key]
    if (n, m) == (1, 0): MEMO[key] = [[]] if t == 0 else []; return MEMO[key]
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or D < 1 or 3 * m > D * n: MEMO[key] = []; return []   # 3m > Dn: degree sum
    r = load(key)
    if r is not None: MEMO[key] = r; return r
    t0 = time.time()
    reps, info = (direct if m <= MDIR else recurse)(n, m, t, D)
    info['secs'] = round(time.time() - t0, 1)
    save(key, reps, info); MEMO[key] = reps
    log('MYCELL', key, 'classes', len(reps), json.dumps(info)[:600])
    return reps
if __name__ == '__main__':
    n, m, t, D = map(int, sys.argv[1:5])
    r = mycell(n, m, t, D); print('RESULT', (n, m, t, D), len(r))
