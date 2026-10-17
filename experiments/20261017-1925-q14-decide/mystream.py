"""Drop-in replacement for engine.direct (monkeypatched in run_one.py for n >= 13): same binaries enum_conn -> filt -> canon, but the labelled FOUND/SURVIVOR
lines are streamed through a shell pipeline (sort -u of canonical forms) instead of being held in Python memory (engine.direct was OOM-killed at 13.8 GB on (14,10,5,3))."""
import os, subprocess, time
import engine
def direct(n, m, t, D):
    key = (n, m, t, D); B = engine.B
    sf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'stream_%d_%d_%d_D%d' % key)
    cmd = ('set -o pipefail; %s %d %d %d %d 1 | tee >(tail -n 1 > %s.last) | grep "^FOUND:" | tee >(wc -l > %s.nfound) | %s FOUND %d tau %d'
           ' | tee >(tail -n 1 > %s.summ) | grep "^SURVIVOR:" | tee >(wc -l > %s.nsurv) | tee >(grep -vc "#conn=1$" > %s.nbadconn)'
           ' | cut -d"#" -f1 | %s %d | sort -u -S 1G > %s.keys'
           % (engine.ENUM, n, m, t, D, sf, sf, os.path.join(B, 'filt'), n, t, sf, sf, sf, os.path.join(B, 'canon'), n, sf))
    subprocess.run(['bash', '-c', cmd], check=True); time.sleep(1)
    rd = lambda ext: open(sf + ext).read().strip()
    nfound = int(rd('.nfound').split()[0]); nsurv = int(rd('.nsurv').split()[0]); assert int(rd('.nbadconn').split()[0]) == 0
    keys = [l for l in open(sf + '.keys').read().splitlines() if l]
    reps = [engine.canon_to_edges(k) for k in sorted(keys)]
    return reps, dict(route='direct(streamed)', enum=rd('.last'), labelled=nfound, in_C_tau_exact=nsurv, filt=rd('.summ'))

import math, itertools
def recurse(n, m, t, D):
    """Memory/disk-streaming twin of engine.recurse (same branches, decompositions, inputs, ext_d call, filt modes; the HIT lines are piped
    ext_d -> filt -> canon -> sort -u instead of being held in Python lists / .out files).  NPROC is ignored (one ext_d process)."""
    info = dict(route='recurse(streamed)', branches=[]); keyfiles = []; nconn = 0; B = engine.B
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = engine.decompositions(n - 1, m - d, Sp); inputs = []; dec_info = []
            for dec in decs:
                groups = {}
                for c in dec: groups[c] = groups.get(c, 0) + 1
                gl = []
                for typ, k in sorted(groups.items()):
                    cls = engine.cell(typ[0], typ[1], typ[2], d)
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
                tag = '%d_%d_%d_D%d_d%d_tp%d' % (n, m, t, D, d, tp); mode = 'notau' if tp == t - 1 else 'tau %d' % t
                NP = int(os.environ.get('NPROC', '1')) if len(inputs) >= 50 * int(os.environ.get('NPROC', '1')) else 1
                bases = []; procs = []
                for ci in range(NP):
                    base = os.path.join(engine.OUT, 'tmp_%s_c%d' % (tag, ci)); bases.append(base)
                    open(base + '.in', 'w').write('\n'.join(inputs[ci::NP]) + '\n')
                    cmd = ('set -o pipefail; %s %d %d %d %d %d < %s.in | tee >(grep "^SUMMARY" > %s.extsum) | grep "^HIT:" | tee >(wc -l > %s.nhit)'
                           ' | %s HIT %d %s | tee >(tail -n 1 > %s.filtsum) | grep "^SURVIVOR:.*#conn=1$" | tee >(wc -l > %s.nsurv)'
                           ' | cut -d"#" -f1 | %s %d | sort -u -S 1G > %s.keys'
                           % (os.path.join(B, 'ext_d'), n - 1, tp, t, d, d - 1, base, base, base, os.path.join(B, 'filt'), n, mode, base, base, os.path.join(B, 'canon'), n, base))
                    procs.append(subprocess.Popen(['bash', '-c', cmd]))
                for p in procs:
                    if p.wait() != 0: raise RuntimeError('pipeline failed')
                time.sleep(1)
                tot = {}; nh = 0; filts = []
                for base in bases:
                    rd = lambda ext: open(base + ext).read().strip()
                    for kv in rd('.extsum').split()[1:]:
                        k, v = kv.split('='); tot[k] = tot.get(k, 0) + int(v) if k != 'max_min_covers' else max(tot.get(k, 0), int(v))
                    nh += int(rd('.nhit').split()[0]); filts.append(rd('.filtsum')); nconn += int(rd('.nsurv').split()[0])
                    keyfiles.append(base + '.keys')
                    for ext in ('.in', '.extsum', '.nhit', '.filtsum', '.nsurv'): os.remove(base + ext)
                if tot.get('bad_tau', 0): raise RuntimeError('bad_tau in %s' % br)
                br['ext'] = tot; br['hits_in_C'] = nh; br['filt'] = filts
            info['branches'].append(br)
            engine.log('  BRANCH', (n, m, t, D), 'd=%d tp=%d S\'=%d decompositions=%d inputs=%d' % (d, tp, Sp, len(decs), len(inputs)), br.get('ext', ''))
    info['connected_hits'] = nconn
    keys = set()
    for kf in keyfiles:
        keys.update(l for l in open(kf).read().splitlines() if l); os.remove(kf)
    return [engine.canon_to_edges(k) for k in sorted(keys)], info
