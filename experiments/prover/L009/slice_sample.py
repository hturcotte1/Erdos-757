"""Random-slice validation of a rebuilt class list (heuristic, certificate L009): run enum_conn_slice on random slices (K, SD) of the
DIRECT enumeration of connected linear (N,M,tau>=T0) graphs with max degree <= 3, for a time budget; write all FOUND lines found.
Usage: slice_sample.py N M T0 K SD SECONDS SEED OUT"""
import subprocess, random, sys, time
N, M, T0, K, SD, TL, seed, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], float(sys.argv[6]), int(sys.argv[7]), sys.argv[8]
random.seed(seed); t0 = time.time(); slices = 0; found = 0; calls = 0; done = set()
with open(out, 'w') as f:
    while time.time() - t0 < TL and len(done) < K:
        I = random.randrange(K)
        if I in done: continue
        done.add(I)
        o = subprocess.run(['indep/enum_conn_slice', N, M, T0, '3', '1', str(K), str(I), SD], capture_output=True, text=True).stdout
        for l in o.splitlines():
            if l.startswith('FOUND:'): f.write(l + '\n'); found += 1
            elif l.startswith('enum_conn'): calls += int(l.split('calls=')[1].split()[0])
        slices += 1
print('slices', slices, 'of K =', K, '(fraction %.4f)' % (slices / K), 'found', found, 'calls', calls, 'secs', round(time.time() - t0))
