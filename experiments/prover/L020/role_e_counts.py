"""Number of role_e configurations (e; a,b) per class (Delta<=3 classes only), and how many distinct centres e."""
import sys, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any
from pattern_e_build import role_e_configs
for p in sys.argv[1:]:
    hist = collections.Counter(); centres = collections.Counter()
    for (n, es) in read_any(p):
        if max(hyp.degrees(n, es)) > 3: continue
        cfg, t = role_e_configs(n, es)
        hist[len(cfg)] += 1; centres[len(set(c[0] for c in cfg))] += 1
    print(p.split('/')[-1], 'configs per class histogram', dict(sorted(hist.items())), 'distinct centres histogram', dict(sorted(centres.items())), flush=True)
