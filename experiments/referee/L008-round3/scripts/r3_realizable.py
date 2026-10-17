"""Referee L008 round 3: own tests of the passage (4,5)-set -> class O+ and of the lemmas on realizable data.
For each test set A: H(A) = 3-APs in rank order.  Checks on EVERY induced subset S (all 2^n for n <= 16):
  (P1) linear; (P3) e(S') <= |S'|-2 for all S' (via the subset DP); I11 slack 3n+2m-11tau >= 0; and tau <= 6 when |S| = 16.
  (P2) F7-freeness is checked on the full set (hereditary) with the definitional detector of r3_extend.
  h(S) = |S| - tau(S) is checked by brute-force Sidon search on samples.  alpha via DP over bitmasks: alpha[S] = |S| if S has no
  edge, else max_v alpha[S - v]."""
import itertools, random, sys, json, gzip, re
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L008-round3/scripts')
random.seed(3)
def aps(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    out = []
    for i in range(len(A)):
        for j in range(i+1, len(A)):
            k = 2*A[j] - A[i]
            if k in idx and idx[k] > j: out.append((i, j, idx[k]))
    return out
def is45(A): return all(len({abs(a-b) for a, b in itertools.combinations(q, 2)}) >= 5 for q in itertools.combinations(A, 4))
def sidon(S):
    s = [x+y for i, x in enumerate(S) for y in S[i:]]; return len(s) == len(set(s))
def h_bruteforce(A):
    A = sorted(A)
    for k in range(len(A), 0, -1):
        if any(sidon(S) for S in itertools.combinations(A, k)): return k
def alpha_table(n, edges):
    em = [sum(1 << v for v in e) for e in edges]
    N = 1 << n
    hasedge = bytearray(N)
    for m in em:
        # mark all supersets of m
        rest = (N - 1) & ~m
        s = rest
        while True:
            hasedge[s | m] = 1
            if s == 0: break
            s = (s - 1) & rest
    alpha = [0] * N
    pop = [0] * N
    for S in range(1, N):
        pop[S] = pop[S & (S-1)] + 1
        if not hasedge[S]: alpha[S] = pop[S]
        else:
            best = 0; T = S
            while T:
                v = T & -T; T ^= v
                a = alpha[S ^ v]
                if a > best: best = a
            alpha[S] = best
    return alpha, pop, em
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
PERMS = list(itertools.permutations(range(7)))
def contains_f7(edges):
    ms = [sum(1 << v for v in e) for e in edges]
    for five in itertools.combinations(range(len(edges)), 5):
        U = 0
        for i in five: U |= ms[i]
        if bin(U).count('1') != 7: continue
        verts = [v for v in range(64) if U >> v & 1]
        degs = sorted(sum(1 for i in five if ms[i] >> v & 1) for v in verts)
        if degs != [2,2,2,2,2,2,3]: continue
        fs = set(ms[i] for i in five)
        for p in PERMS:
            if all((1 << verts[p[a]]) | (1 << verts[p[b]]) | (1 << verts[p[c]]) in fs for a, b, c in F7): return True
    return False
def check_set(name, A, sample_h=40, full=True):
    A = sorted(A); n = len(A)
    assert len(set(A)) == n and is45(A), name + ' not a (4,5)-set'
    E = aps(A); m = len(E)
    ms = [sum(1 << v for v in e) for e in E]
    lin = all(bin(ms[i] & ms[j]).count('1') <= 1 for i in range(m) for j in range(i+1, m))
    mids = [e[1] for e in E]; inj = len(set(mids)) == m and all(0 < j < n-1 for j in mids)
    f7 = contains_f7(E)
    alpha, pop, em = alpha_table(n, E)
    N = 1 << n
    viol_p3 = viol_i11 = 0; tau16bad = 0; minslack = 99
    for S in range(1, N):
        eS = sum(1 for x in em if x & S == x)
        if pop[S] >= 2 and eS > pop[S] - 2: viol_p3 += 1
        t = pop[S] - alpha[S]
        s = 3*pop[S] + 2*eS - 11*t
        if s < 0: viol_i11 += 1
        if s < minslack and pop[S] >= 3: minslack = s
        if pop[S] == 16 and t > 6: tau16bad += 1
    # h = n - tau on samples
    hbad = 0
    for _ in range(sample_h):
        k = random.randint(4, min(n, 12)); Sidx = sorted(random.sample(range(n), k))
        S = sum(1 << i for i in Sidx)
        if h_bruteforce([A[i] for i in Sidx]) != alpha[S]: hbad += 1
    hfull = alpha[N-1]
    print(f'{name}: n={n} m={m} tau={n-hfull} h=alpha={hfull} linear={lin} midpoints_injective_interior={inj} F7={f7} '
          f'P3_violations={viol_p3} I11_violations={viol_i11} min_slack(|S|>=3)={minslack} tau>6_at_16={tau16bad} h_mismatches={hbad}/{sample_h}')
    return dict(n=n, m=m, h=hfull, lin=lin, inj=inj, f7=f7, p3=viol_p3, i11=viol_i11, bad16=tau16bad, hbad=hbad)
AB = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
C16 = sorted(AB + [-323, 5000])
rec = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
fib = [2,3]
while len(fib) < 16: fib.append(fib[-1] + fib[-2])
res = {}
res['A_base'] = check_set('A_base', AB)
res['C16'] = check_set('C16', C16)
for key in ['12', '12b', '12c', '8', '10', '11']:
    res['rec'+key] = check_set('record_'+key, rec[key]['set'])
res['fib16'] = check_set('Fibonacci F3..F18', fib)
res['fib15'] = check_set('Fibonacci F3..F17', fib[:15])
# generic gluing A_base U (q*B + t) with q avoiding all ratios: random 16-subsets checked
B = rec['12']['set']; q = 7919; t = 10**7
C = sorted(set(AB) | set(q*b + t for b in B))
assert len(C) == 26 and is45(C)
print('gluing n=26: APs', len(aps(C)))
bad = 0
for trial in range(60):
    S = sorted(random.sample(C, 16))
    E = aps(S); alpha, pop, em = alpha_table(16, E); t16 = 16 - alpha[(1<<16)-1]
    s = 48 + 2*len(E) - 11*t16
    if t16 > 6 or s < 0: bad += 1
print('gluing: 60 random 16-subsets, violations of tau<=6 or I11:', bad)
# census n=14 m=12 classes: pattern in O+ with tau=6 ?
cnt = 0; badc = 0
with gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') as f:
    for line in f:
        r = json.loads(line); A = sorted(r['set']); E = aps(A)
        if len(E) != 12: badc += 1; continue
        alpha, pop, em = alpha_table(14, E)
        if 14 - alpha[(1<<14)-1] != 6: badc += 1
        cnt += 1
        if cnt >= 400: break
print(f'census n14 m12: {cnt} classes checked, m=12 and tau=6 failures: {badc}')
json.dump(res, open('/home/user/Erdos-757/experiments/referee/L008-round3/out/realizable_results.json', 'w'), indent=1)
