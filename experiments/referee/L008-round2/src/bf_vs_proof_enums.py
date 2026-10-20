"""Referee round 2 (L008): the proof's enumerators enum_conn (prover) and conn_dfs3 (falsifier) against my labelled brute force
bf_lab on every connected cell with n <= 9, D in {3, inf}, every m >= 1 and every threshold t = 1..taumax+1: the brute-force
number of labelled connected spanning linear 3-graphs with tau >= t must equal sum over the DISTINCT isomorphism classes in the
enumerator's output of n!/|Aut| (classes and |Aut| from canon_list); every output must be a valid graph of the cell."""
import re, subprocess, sys, collections, math
bf = collections.defaultdict(int)
for fn in sys.argv[1:]:
    for l in open(fn):
        g = re.match(r'CON n=(\d+) D=(\d+) m=(\d+) tau=(\d+) count=(\d+)', l)
        if g: bf[tuple(map(int, g.groups()[:4]))] += int(g.group(5))
cells = mism = 0
for (n, D) in sorted(set((k[0], k[1]) for k in bf)):
    for m in sorted(set(k[2] for k in bf if k[0] == n and k[1] == D)):
        tmax = max(k[3] for k in bf if k[0] == n and k[1] == D and k[2] == m)
        for t in range(1, tmax + 2):
            want = sum(v for k, v in bf.items() if k[0] == n and k[1] == D and k[2] == m and k[3] >= t)
            for prog in (['./rerun/bin/enum_conn', str(n), str(m), str(t), str(D), '1'], ['./rerun/bin/conn_dfs3', str(n), str(m), str(t), str(D), '0', '0']):
                out = subprocess.run(prog, capture_output=True, text=True).stdout
                found = [l for l in out.splitlines() if l.startswith('FOUND')]
                keys = subprocess.run(['./bin/canon_list', 'FOUND', str(n)], input='\n'.join(found) + '\n', capture_output=True, text=True).stdout.split('\n')
                cls = {}
                for kl in keys:
                    if kl.strip(): k, a = kl.split(); cls[k] = int(a)
                got = sum(math.factorial(n) // a for a in cls.values())
                cells += 1
                if got != want: mism += 1; print('MISMATCH', prog[0], n, D, m, t, want, got)
print('cells x programs compared:', cells, 'mismatches:', mism)
