# Referee round 2: brute-force validation of fr (random 3-graphs on <= 10 vertices, many with F7 planted).
import itertools, random, subprocess
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def linear(E): return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2)) and len(set(map(frozenset, E))) == len(E)
def has_f7(n, E):
    S = set(map(frozenset, E))
    for vs in itertools.permutations(range(n), 7):
        if all(frozenset(vs[i] for i in e) in S for e in F7): return True
    return False
def p3(n, E):
    for k in range(2, n + 1):
        for Sv in itertools.combinations(range(n), k):
            s = set(Sv)
            if sum(1 for e in E if set(e) <= s) > k - 2: return False
    return True
def tau(n, E):
    for k in range(n + 1):
        for Sv in itertools.combinations(range(n), k):
            if all(set(Sv) & set(e) for e in E): return k
random.seed(11); tests = []
while len(tests) < 400:
    n = random.randint(7, 9); m = random.randint(3, n - 1)
    E = []
    if random.random() < 0.4:
        perm = random.sample(range(n), 7); E = [tuple(sorted(perm[i] for i in e)) for e in F7]
        if random.random() < 0.5: E.pop(random.randrange(5))
    tries = 0
    while len(E) < m and tries < 200:
        tries += 1; e = tuple(sorted(random.sample(range(n), 3)))
        if random.random() < 0.9 and not linear(E + [e]): continue
        if e not in E: E.append(e)
    tests.append((n, E))
bad = 0; stats = dict(nonlin=0, f7=0, p3=0, surv=0)
for n, E in tests:
    line = 'X: ' + ' '.join('(%d,%d,%d)' % e for e in E) + '\n'
    out = subprocess.run(['./out/fr', str(n), 'print'], input=line, capture_output=True, text=True).stdout
    summ = dict(kv.split('=') for kv in out.splitlines()[-1].split()[1:6])
    if not linear(E): exp = 'nonlinear'
    elif has_f7(n, E): exp = 'F7'
    elif not p3(n, E): exp = 'P3violated'
    else: exp = 'survivors'
    got = [k for k in ('nonlinear', 'F7', 'P3violated', 'survivors') if summ[k] == '1']
    if got != [exp]: bad += 1; print('MISMATCH', n, E, exp, got)
    if exp == 'survivors':
        t = int(out.splitlines()[0].split()[1].split('=')[1])
        if t != tau(n, E): bad += 1; print('TAU MISMATCH', n, E)
    stats[{'nonlinear': 'nonlin', 'F7': 'f7', 'P3violated': 'p3', 'survivors': 'surv'}[exp]] += 1
print('tests %d %s mismatches %d' % (len(tests), stats, bad))
