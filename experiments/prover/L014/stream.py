"""(L014) Streamed twins of engine.direct and engine.recurse (experiments/prover/L014/engine.py = L012's engine.py, unchanged).

Why: engine.direct / engine.recurse hold every labelled graph / every HIT line in Python lists; on the cells of this certificate
(e.g. 57.9M labelled graphs of (14,10,5,3), 1e7 HIT lines of (15,13,6,3)) that exceeds the 15 GB of the machine.

What is the same (line by line as in engine.py):
  * engine.cell (memo, load/save of out/cells files, the trivial-cell guards, the choice direct if m <= MD else recurse) is not touched;
  * direct: `enum_conn n m t D 1`, then `filt FOUND n tau t`, keep the SURVIVOR lines (all must be connected), canonical forms by
    `canon n`, one representative per distinct canonical form, representatives = parsed canonical forms sorted by the form string;
  * recurse: the same branches (d from max(1,ceil(3m/n)) to D, t' in (t-1, t), S' = 3(n-1)+2(m-d)-11t' >= 0, t' >= 0), the same
    decompositions engine.decompositions(n-1, m-d, S'), the same component cells engine.cell(n_i, m_i, tau_i, d), the same input
    lines in the same order (multisets by itertools.combinations_with_replacement, product in sorted-type order, consecutive vertex
    blocks), the same chunking (inputs[i::NPROC] if len >= 50*NPROC, else one chunk), the same call `ext_d (n-1) t' t d (d-1)`,
    the same counters (summed; max for max_min_covers), RuntimeError on bad_tau != 0, the same filter call (`filt HIT n notau` for
    t' = t-1, `filt HIT n tau t` for t' = t), keep SURVIVOR lines flagged #conn=1, canonical forms, one per distinct form.
What differs: the lines flow through a shell pipeline (bash, set -o pipefail; every exit code checked) and the distinct canonical
forms are collected by an awk hash of the distinct lines and `LC_ALL=C sort -u` instead of Python lists:
  ext_d ... < chunk.in | awk(HIT lines to stdout, other lines to chunk.extsum) | filt HIT n MODE | awk(SURVIVOR lines to stdout,
  other lines to chunk.filtsum) | awk(keep lines ending '#conn=1') | cut -d'#' -f1 | canon n | awk(first occurrence of each line) | LC_ALL=C sort -u > chunk.keys
filt and ext_d treat every input line independently, so splitting into chunks/branches before filt does not change the survivors;
the union of the chunk key sets is the engine's set of distinct canonical forms.  cut leaves a trailing blank where the engine strips
' #conn...' (l.split(' #conn')[0]); canon reads only the '(a,b,c)' groups, so its output is the same.
The counters that engine.recurse computes in Python (number of HIT lines = hits_in_C, connected survivors = connected_hits) are read
from filt's SUMMARY line (total=, survivors_connected=)."""
import os, sys, math, itertools, subprocess, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
WORK = os.environ.get('WORKDIR', os.path.join(engine.HERE, 'out', 'work')); os.makedirs(WORK, exist_ok=True)
SORTMEM = os.environ.get('SORTMEM', '600M')
def sh(cmd):
    r = subprocess.run(['bash', '-c', 'set -o pipefail; ' + cmd])
    if r.returncode != 0: raise RuntimeError('pipeline failed (rc=%d): %s' % (r.returncode, cmd))
def rd(fn): return open(fn).read().strip()
def summary_kv(line):
    out = {}
    for kv in line.split():
        if '=' in kv:
            k, v = kv.split('=', 1); out[k] = v
    return out
def keys_to_reps(keyfiles):
    keys = set()
    for kf in keyfiles:
        with open(kf) as f:
            for l in f:
                l = l.rstrip('\n')
                if l: keys.add(l)
    return [engine.canon_to_edges(k) for k in sorted(keys)]
def direct(n, m, t, D):
    key = (n, m, t, D); base = os.path.join(WORK, 'direct_%d_%d_%d_D%d' % key)
    B = engine.B
    cmd = ("%s %d %d %d %d 1 | awk '/^FOUND:/{print; next} {print > \"%s.enumsum\"}' | %s FOUND %d tau %d"
           " | awk '/^SURVIVOR:/{print; next} {print > \"%s.filtsum\"}' | cut -d'#' -f1 | %s %d 2>> %s.canonlog"
           " | awk '!s[$0]++' | LC_ALL=C sort -u -S %s -T %s > %s.keys"
           % (engine.ENUM, n, m, t, D, base, os.path.join(B, 'filt'), n, t, base, os.path.join(B, 'canon'), n, base, SORTMEM, WORK, base))
    sh(cmd)
    last = rd(base + '.enumsum').splitlines()[-1]; summ = rd(base + '.filtsum').splitlines()[-1]
    kv = summary_kv(summ)
    assert kv['survivors'] == kv['survivors_connected'], ('direct: disconnected survivor', key, summ)   # engine.direct's assert
    reps = keys_to_reps([base + '.keys'])
    for ext in ('.enumsum', '.filtsum', '.keys', '.canonlog'):
        if os.path.exists(base + ext): os.remove(base + ext)
    return reps, dict(route='direct', driver='stream', enum=last, labelled=int(kv['total']), in_C_tau_exact=int(kv['survivors']), filt=summ)
def recurse(n, m, t, D):
    info = dict(route='recurse', driver='stream', branches=[]); keyfiles = []; nconn = 0; B = engine.B; NPROC = engine.NPROC
    filts = []
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = engine.decompositions(n - 1, m - d, Sp)
            plan = []; dec_info = []; total = 0
            for dec in decs:
                groups = {}
                for c in dec: groups[c] = groups.get(c, 0) + 1
                gl = []
                for typ, k in sorted(groups.items()):
                    cls = engine.cell(typ[0], typ[1], typ[2], d)
                    gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), k))))
                size = 1
                for g in gl: size *= len(g[2])
                dec_info.append([list(dec), size]); plan.append(gl); total += size
            br = dict(d=d, tp=tp, Sp=Sp, decompositions=len(decs), inputs=total, dec=dec_info)
            if total:
                tag = '%d_%d_%d_D%d_d%d_tp%d' % (n, m, t, D, d, tp)
                NP = NPROC if total >= 50 * NPROC else 1
                bases = [os.path.join(WORK, 'rec_%s_c%d' % (tag, i)) for i in range(NP)]
                fhs = [open(b + '.in', 'w') for b in bases]; idx = 0
                for gl in plan:
                    for combo in itertools.product(*[g[2] for g in gl]):
                        es = []; off = 0
                        for (typ, cls, _), idxs in zip(gl, combo):
                            for i in idxs:
                                es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                        assert off == n - 1
                        fhs[idx % NP].write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); idx += 1
                for fh in fhs: fh.close()
                assert idx == total
                mode = 'notau' if tp == t - 1 else 'tau %d' % t
                procs = []
                for b in bases:
                    cmd = ("%s %d %d %d %d %d < %s.in 2>> %s.err | awk '/^HIT:/{print; next} {print > \"%s.extsum\"}'"
                           " | %s HIT %d %s | awk '/^SURVIVOR:/{print; next} {print > \"%s.filtsum\"}' | awk '/#conn=1$/'"
                           " | cut -d'#' -f1 | %s %d 2>> %s.err | awk '!s[$0]++' | LC_ALL=C sort -u -S %s -T %s > %s.keys"
                           % (os.path.join(B, 'ext_d'), n - 1, tp, t, d, d - 1, b, b, b, os.path.join(B, 'filt'), n, mode, b,
                              os.path.join(B, 'canon'), n, b, SORTMEM, WORK, b))
                    procs.append((b, subprocess.Popen(['bash', '-c', 'set -o pipefail; ' + cmd])))
                for b, p in procs:
                    if p.wait() != 0: raise RuntimeError('pipeline failed %s: %s' % (b, open(b + '.err').read()[-2000:]))
                tot = {}; nh = 0; fl = []
                for b in bases:
                    es = [l for l in rd(b + '.extsum').splitlines() if l.startswith('SUMMARY')]
                    assert len(es) == 1, (b, es)
                    for kv in es[0].split()[1:]:
                        k, v = kv.split('='); tot[k] = tot.get(k, 0) + int(v) if k != 'max_min_covers' else max(tot.get(k, 0), int(v))
                    fs = rd(b + '.filtsum').splitlines()[-1]; fkv = summary_kv(fs)
                    nh += int(fkv['total']); nconn += int(fkv['survivors_connected']); fl.append(fs)
                    keyfiles.append(b + '.keys')
                    for ext in ('.in', '.extsum', '.filtsum', '.err'): os.remove(b + ext)
                if tot.get('bad_tau', 0): raise RuntimeError('bad_tau in %s' % br)
                assert tot.get('graphs') == total and tot.get('searched', 0) + tot.get('tg_too_small', 0) + tot.get('bad_tau', 0) == total
                assert nh == tot.get('hits_in_C', 0), ('HIT lines vs ext_d counter', nh, tot)
                br['ext'] = tot; br['hits_in_C'] = nh; br['filt_chunks'] = fl; filts += fl
            info['branches'].append(br)
            engine.log('  BRANCH', (n, m, t, D), 'd=%d tp=%d S\'=%d decompositions=%d inputs=%d' % (d, tp, Sp, len(decs), total), br.get('ext', ''))
    info['connected_hits'] = nconn
    reps = keys_to_reps(keyfiles)
    for kf in keyfiles: os.remove(kf)
    return reps, info
def install():
    engine.direct = direct; engine.recurse = recurse
