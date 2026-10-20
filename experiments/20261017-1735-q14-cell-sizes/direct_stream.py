"""Streaming variant of engine.direct (same binaries enum_conn -> filt -> canon; only difference: the labelled FOUND lines are piped, not held in Python
memory; the engine's own direct() was OOM-killed at 13.8 GB on cell (14,10,5,3)).  Writes the cell file in the engine format and appends to progress.tsv.
Usage: python3 direct_stream.py n m tau D"""
import os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells'))
os.environ.setdefault('ENGINELOG', os.path.join(HERE, 'out', 'engine.log'))
sys.path.insert(0, HERE)
import engine
n, m, t, D = key = tuple(map(int, sys.argv[1:5])); assert m <= engine.MD
t0 = time.time(); B = engine.B
sf = os.path.join(HERE, 'out', 'stream_%d_%d_%d_D%d' % key)
cmd = ('set -o pipefail; %s %d %d %d %d 1 | tee >(tail -n 1 > %s.last) | grep "^FOUND:" | tee >(wc -l > %s.nfound) | %s FOUND %d tau %d'
       ' | tee >(tail -n 1 > %s.summ) | grep "^SURVIVOR:" | tee >(wc -l > %s.nsurv) | tee >(grep -vc "#conn=1$" > %s.nbadconn)'
       ' | cut -d"#" -f1 | %s %d | sort -u -S 1G > %s.keys'
       % (engine.ENUM, n, m, t, D, sf, sf, os.path.join(B, 'filt'), n, t, sf, sf, sf, os.path.join(B, 'canon'), n, sf))
subprocess.run(['bash', '-c', cmd], check=True)
time.sleep(1)
rd = lambda ext: open(sf + ext).read().strip()
nfound = int(rd('.nfound').split()[0]); last = rd('.last'); summ = rd('.summ'); nsurv = int(rd('.nsurv').split()[0]); assert int(rd('.nbadconn').split()[0]) == 0
keys = [l for l in open(sf + '.keys').read().splitlines() if l]
reps = [engine.canon_to_edges(k) for k in sorted(keys)]
info = dict(route='direct(streamed)', enum=last, labelled=nfound, in_C_tau_exact=nsurv, filt=summ, secs=round(time.time() - t0, 1))
engine.save(key, reps, info); engine.log('CELL', key, 'classes', len(reps), info)
open(os.path.join(HERE, 'progress.tsv'), 'a').write('\t'.join(map(str, ['(%d,%d,%d,%d)' % key, len(reps), info['secs'], info['route'], 0, 0, 0])) + '\n')
print('DONE', key, len(reps), info['secs'], 'labelled', nfound, 'survivors', nsurv)
