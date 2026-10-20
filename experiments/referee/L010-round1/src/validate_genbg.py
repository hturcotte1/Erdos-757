"""Referee L010 r1: validate genbg_ref (orderly generation + referee hooks) against the labelled brute force bf.c.
For each n, D: for every m, bf gives the number of labelled connected spanning linear 3-graphs on [n] with max degree <= D
and transversal number tau; genbg gives one representative per isomorphism class; nauty gives |Aut|; the labelled count of
a class is n!/|Aut|.  Also checks the tau-pruned genbg (TAU0 = t) returns exactly the classes with tau >= t."""
import subprocess, sys, math, collections, os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin')
def run(cmd, env=None, inp=None):
    return subprocess.run(cmd, capture_output=True, text=True, env=env, input=inp).stdout
bad = 0; cells = 0
for n, D in [(int(a), int(b)) for a, b in (x.split(':') for x in sys.argv[1:])]:
    bf = collections.Counter()
    for l in run([B + '/bf', str(n), str(D)]).split('\n'):
        if l.strip():
            _, _, m, t, c = map(int, l.split()); bf[(m, t)] = c
    ms = sorted({m for m, t in bf} | set(range(1, n + 1)))
    for m in ms:
        env = dict(os.environ, TAU0='0')
        out = run([B + '/genbg_ref64', '-q', '-c', '-Z1', '-d1:3', '-D%d:3' % D, str(n), str(m), '%d:%d' % (3 * m, 3 * m)], env)
        lines = [l for l in out.split('\n') if l.startswith('FOUND')]
        can = run([B + '/canon', 'x', str(n)], inp='\n'.join(lines) + '\n').split('\n')
        gb = collections.Counter(); keys = set()
        for l, c in zip(lines, can):
            t = int(l.split('tau=')[1]); key, aut = c.split()
            assert key not in keys; keys.add(key)
            gb[(m, t)] += math.factorial(n) // int(aut)
        tvals = sorted({t for (mm, t) in bf if mm == m} | {t for (mm, t) in gb if mm == m})
        for t in tvals:
            cells += 1
            if bf[(m, t)] != gb[(m, t)]:
                bad += 1; print('MISMATCH', n, D, m, t, bf[(m, t)], gb[(m, t)])
        # pruned runs: TAU0 = t must give exactly the classes with tau >= t
        for t0 in range(0, (max(tvals) + 2) if tvals else 1):
            env = dict(os.environ, TAU0=str(t0))
            out = run([B + '/genbg_ref64', '-q', '-c', '-Z1', '-d1:3', '-D%d:3' % D, str(n), str(m), '%d:%d' % (3 * m, 3 * m)], env)
            k = sum(1 for l in out.split('\n') if l.startswith('FOUND'))
            want = sum(1 for l in lines if int(l.split('tau=')[1]) >= t0)
            cells += 1
            if k != want: bad += 1; print('PRUNE MISMATCH', n, D, m, t0, k, want)
    print('n=%d D=%d: labelled total %d over %d (m,tau) cells' % (n, D, sum(bf.values()), len(bf)), flush=True)
print('compared', cells, 'mismatches', bad)
