"""(L014) Re-validation of the final extension step of a recursion cell without pruning, with the pure-Python verifier.
python3 ext_validate.py n m t D OUTDIR [TAU_CHECK_LIMIT]
Rebuilds the inputs of every branch of the key (n,m,t,D) from CELLDIR (gen_inputs.py; nothing is computed), runs
`ext_d (n-1) t' t d (d-1) noprune` (no F7 pruning, no (P3) test: every extension with tau >= t), and classifies every printed extension by
pyverify in the order: connected on n vertices, linear, F7-free, (P3), max degree <= D, tau = t (tau checked exactly for every extension
that passes the earlier tests, and for the first TAU_CHECK_LIMIT others: no cover of size t-1).  Prints the counts."""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pyverify as pv
n, m, t, D = map(int, sys.argv[1:5]); out = sys.argv[5]; lim = int(sys.argv[6]) if len(sys.argv) > 6 else 0
os.makedirs(out, exist_ok=True)
inp = os.path.join(out, 'in_%d_%d_%d_%d.txt' % (n, m, t, D)); tg = inp + '.tags'
g = subprocess.run(['python3', os.path.join(HERE, 'gen_inputs.py'), str(n), str(m), str(t), str(D), inp, tg], capture_output=True, text=True, check=True).stdout
print(g.strip().splitlines()[-1])
lines = open(inp).read().splitlines(); tags = open(tg).read().splitlines()
groups = {}
for l, tt in zip(lines, tags):
    d, tp = (int(x) for x in re.match(r'd=(\d+) tp=(\d+)', tt).groups()); groups.setdefault((d, tp), []).append(l)
for (d, tp), ls in sorted(groups.items()):
    r = subprocess.run([os.path.join(HERE, 'bin', 'ext_d'), str(n - 1), str(tp), str(t), str(d), str(d - 1), 'noprune'], input='\n'.join(ls) + '\n', capture_output=True, text=True, check=True)
    cnt = dict(total=0, disconnected=0, nonlinear=0, F7=0, P3=0, degree=0, wrong_tau=0, member=0, tau_checked=0)
    for l in r.stdout.splitlines():
        if not l.startswith('HIT:'): continue
        E = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]; cnt['total'] += 1
        if cnt['tau_checked'] < lim:
            cnt['tau_checked'] += 1; assert not pv.cover_le(E, t - 1), 'extension with tau < t'
        if not pv.connected(E, range(n)): cnt['disconnected'] += 1; continue
        if not pv.linear(E): cnt['nonlinear'] += 1; continue
        if pv.has_f7(E): cnt['F7'] += 1; continue
        if not pv.p3(E, range(n)): cnt['P3'] += 1; continue
        if pv.maxdeg(E) > D: cnt['degree'] += 1; continue
        if pv.cover_le(E, t - 1) or not pv.cover_le(E, t): cnt['wrong_tau'] += 1; continue
        cnt['member'] += 1
    print('(%d,%d,%d,%d) branch d=%d t\'=%d: %d inputs; ext_d noprune %s; pyverify: %s' % (n, m, t, D, d, tp, len(ls), r.stdout.strip().splitlines()[-1], cnt), flush=True)
