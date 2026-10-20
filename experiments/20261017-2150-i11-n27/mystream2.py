"""Chunked, RESUMABLE variant of mystream.recurse (same branches, decompositions, inputs, ext_d call, filt modes, canon; NPROC=1).
Inputs of each branch are processed in contiguous chunks of CHUNK inputs (default 25000); each finished chunk leaves out/chunks/<tag>/cNNNNN.keys.gz (canonical keys
of its connected survivors) and cNNNNN.meta.json (counters).  A rerun skips finished chunks; the final class list is the union of all chunk key files.
Only the chunking/persistence differs from mystream.recurse."""
import os, subprocess, time, gzip, json
import engine
from mystream import direct
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
                CH = int(os.environ.get('CHUNK', '25000')); cdir = os.path.join(engine.OUT, '..', 'chunks', tag); os.makedirs(cdir, exist_ok=True)
                nchunks = (len(inputs) + CH - 1) // CH; tot = {}; nh = 0; filts = []; skipped = False
                for ci in range(nchunks):
                    base = os.path.join(cdir, 'c%05d' % ci)
                    if not os.path.exists(base + '.meta.json') and os.environ.get('WORKER'):
                        # worker mode (added 2026-10-20): claim the chunk with an O_EXCL file, else skip it; the cell is assembled by a later run without WORKER
                        try: os.close(os.open(base + '.claim', os.O_CREAT | os.O_EXCL | os.O_WRONLY))
                        except FileExistsError: skipped = True; continue
                    if not os.path.exists(base + '.meta.json'):
                        t1 = time.time()
                        open(base + '.in', 'w').write('\n'.join(inputs[ci * CH:(ci + 1) * CH]) + '\n')
                        cmd = ('set -o pipefail; %s %d %d %d %d %d < %s.in | tee >(grep "^SUMMARY" > %s.extsum) | (grep "^HIT:" || true) | tee >(wc -l > %s.nhit)'
                               ' | %s HIT %d %s | tee >(tail -n 1 > %s.filtsum) | (grep "^SURVIVOR:.*#conn=1$" || true) | tee >(wc -l > %s.nsurv)'
                               ' | cut -d"#" -f1 | %s %d | sort -u -S 1G | gzip > %s.keys.gz'
                               % (os.path.join(B, 'ext_d'), n - 1, tp, t, d, d - 1, base, base, base, os.path.join(B, 'filt'), n, mode, base, base, os.path.join(B, 'canon'), n, base))
                        p = subprocess.Popen(['bash', '-c', cmd]); 
                        if p.wait() != 0: raise RuntimeError('pipeline failed')
                        time.sleep(1)
                        rd = lambda ext: open(base + ext).read().strip()
                        ext = {}
                        for kv in rd('.extsum').split()[1:]:
                            k, v = kv.split('='); ext[k] = int(v)
                        meta = dict(ext=ext, nhit=int(rd('.nhit').split()[0]), filt=rd('.filtsum'), nsurv=int(rd('.nsurv').split()[0]), secs=round(time.time() - t1, 1), ninputs=len(inputs[ci * CH:(ci + 1) * CH]))
                        for e_ in ('.in', '.extsum', '.nhit', '.filtsum', '.nsurv'): os.remove(base + e_)
                        json.dump(meta, open(base + '.meta.json', 'w'))
                        engine.log('  CHUNK', tag, ci + 1, '/', nchunks, 'secs', meta['secs'], 'hits_in_C', meta['nhit'], 'conn', meta['nsurv'], 'bad_tau', ext.get('bad_tau'))
                        with open(os.path.join(engine.OUT, '..', 'chunk_progress.tsv'), 'a') as cf: cf.write('%s\t%d/%d\t%s\t%d\t%d\t%d\n' % (tag, ci + 1, nchunks, meta['secs'], meta['ninputs'], meta['nhit'], meta['nsurv']))
                    if os.environ.get('WORKER') and os.path.exists(base + '.claim'): os.remove(base + '.claim')
                    meta = json.load(open(base + '.meta.json'))
                    for k, v in meta['ext'].items(): tot[k] = tot.get(k, 0) + v if k != 'max_min_covers' else max(tot.get(k, 0), v)
                    nh += meta['nhit']; filts.append(meta['filt']); nconn += meta['nsurv']; keyfiles.append(base + '.keys.gz')
                if skipped: raise RuntimeError('WORKER_DONE_SKIPPED_CHUNKS')
                if tot.get('bad_tau', 0): raise RuntimeError('bad_tau in %s' % br)
                br['ext'] = tot; br['hits_in_C'] = nh; br['filt'] = filts; br['chunks'] = nchunks
            info['branches'].append(br)
            engine.log('  BRANCH', (n, m, t, D), 'd=%d tp=%d S\'=%d decompositions=%d inputs=%d' % (d, tp, Sp, len(decs), len(inputs)), br.get('ext', ''))
    info['connected_hits'] = nconn
    keys = set()
    for kf in keyfiles:
        keys.update(l for l in gzip.open(kf, 'rt').read().splitlines() if l)
    return [engine.canon_to_edges(k) for k in sorted(keys)], info
