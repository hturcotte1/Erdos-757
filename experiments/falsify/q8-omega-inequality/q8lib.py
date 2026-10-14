import subprocess, os, sys
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))
from e757.core import ap_edges, is_45_set

BIN = os.path.join(HERE, 'q8')

def masks_of(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(1 << idx[a]) | (1 << idx[b]) | (1 << idx[c]) for a, b, c in ap_edges(A)]

def run_cases(cases, vcap=1000, printeq=False):
    """cases: list of (id, n, masks, mode, param, seed). Returns dict id -> result."""
    inp = ''.join(f"{i} {n} {len(ms)} {' '.join(map(str, ms))} {mode} {param} {seed}\n" for i, n, ms, mode, param, seed in cases)
    env = dict(os.environ)
    if printeq: env['PRINTEQ'] = '1'
    out = subprocess.run([BIN, str(vcap)], input=inp, capture_output=True, text=True, env=env).stdout
    res = {}; pend_v = {}; pend_e = {}
    for line in out.splitlines():
        t = line.split()
        if t[0] == 'CASE':
            i = int(t[1]); d = dict(kv.split('=') for kv in t[2:]); res[i] = {k: int(v) for k, v in d.items()}
            res[i].update(hist={}, viol=pend_v.pop(i, []), eq=pend_e.pop(i, []))
        elif t[0] == 'H':
            i = int(t[1]); res[i]['hist'][t[2]] = {int(a.split(':')[0]): int(a.split(':')[1]) for a in t[3:]}
        elif t[0] == 'V':
            pend_v.setdefault(int(t[1]), []).append(' '.join(t[2:]))
        elif t[0] == 'EQ':
            pend_e.setdefault(int(t[1]), []).append(' '.join(t[2:]))
    return res

def decode(mask, A):
    A = sorted(A); return [A[i] for i in range(len(A)) if mask >> i & 1]
