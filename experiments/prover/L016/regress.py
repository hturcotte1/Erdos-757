"""(L016) python3 regress.py INFILE NSAMPLE SEED BIN_A BIN_B ARGS...
Takes a seeded random sample of NSAMPLE input lines of INFILE (all lines if NSAMPLE <= 0 or >= the number of lines; order kept),
runs `BIN_A ARGS < sample` and `BIN_B ARGS < sample` and compares exit codes and stdout byte for byte; also runs every sampled line
separately through both binaries if the sample has at most 50 lines.  Prints one RESULT line."""
import sys, random, subprocess, hashlib, tempfile, os
fn, ns, seed, A, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]; args = sys.argv[6:]
lines = [l for l in open(fn) if l.strip()]
N = len(lines)
if 0 < ns < N:
    idx = sorted(random.Random(seed).sample(range(N), ns)); lines = [lines[i] for i in idx]
data = ''.join(lines).encode()
ra = subprocess.run([A] + args, input=data, capture_output=True); rb = subprocess.run([B] + args, input=data, capture_output=True)
same = ra.returncode == rb.returncode and ra.stdout == rb.stdout
summ = [l for l in ra.stdout.decode().splitlines() if l.startswith('SUMMARY')]
nh = sum(1 for l in ra.stdout.decode().splitlines() if l.startswith('HIT'))
print('RESULT file=%s lines=%d sampled=%d seed=%d args=%s rcA=%d rcB=%d stdout_identical=%s md5=%s hit_lines=%d %s' % (
    os.path.basename(fn), N, len(lines), seed, ' '.join(args), ra.returncode, rb.returncode, same, hashlib.md5(ra.stdout).hexdigest()[:12], nh,
    summ[0] if summ else ''), flush=True)
if not same: print('STDERR_A', ra.stderr[-300:], 'STDERR_B', rb.stderr[-300:]); sys.exit(1)
