import sys, os, json, gzip, subprocess, math
from collections import defaultdict
sys.path.insert(0, '/home/user/Erdos-757')
HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'tuples')
def mask(e): return sum(1 << v for v in e)

def run_tuples(cases):
    """cases: list of (id, n, edge_masks, mode, param). mode 0: all 3^n (S,D) states; 1: S=V, |D|<=param;
    3: S=V, all independent D.  Returns {id: list of tuple dicts}.  One distinct (tau,R,e2,e1) per entry,
    cnt = number of states giving it, (S,D) = example with minimal |D|."""
    inp = ''.join(f"{i} {n} {len(ms)} {' '.join(map(str, ms))} {mode} {param} 0\n" for i, n, ms, mode, param in cases)
    out = subprocess.run([BIN, '0'], input=inp, capture_output=True, text=True).stdout
    res = defaultdict(list)
    for line in out.splitlines():
        t = line.split()
        if t[0] == 'T':
            i = int(t[1]); v = list(map(int, t[2:]))
            res[i].append(dict(tau=v[0], R=v[1], e2=v[2], e1=v[3], nS=v[4], dsz=v[5], cnt=v[6], S=v[7], D=v[8]))
    return res
