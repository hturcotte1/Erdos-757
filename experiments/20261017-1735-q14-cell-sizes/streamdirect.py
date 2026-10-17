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
