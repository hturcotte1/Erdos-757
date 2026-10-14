"""Independent referee check of the Q8 falsifier (experiments/falsify/q8-omega-inequality).

Pure stdlib. Does NOT import e757 or any falsifier Python code. The only contact with the
falsifier's work is calling its compiled C binary as a black box and comparing its printed
histograms / equality states with this script's own exact brute-force computation.

Definitions (kb/notes/omega_issue_9804.md): A a (4,5)-set, S an induced subset, D subset of S
independent (no 3-AP of S inside D), R = S \ D, K = inclusion-minimal nonempty traces e \ D of
the 3-APs e of S (deduplicated), e_i = number of members of K of size i.
  Q8 : 7 tau(K) <= 3|R| + 2 e_2 + 4 e_1        (slack sQ = rhs - lhs)
  Act: same with |R| replaced by |union K|      (slack sA)
  D4 : 21 tau(K) <= 9|R| + 5 e_2 + 12 e_1      (slack sD)
"""
import itertools, json, os, subprocess, sys, time, collections, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FALS = os.path.join(ROOT, 'experiments', 'falsify', 'q8-omega-inequality')
BIN = os.path.join(FALS, 'q8')

# ---------- my own exact primitives ----------
def is45(A):
    """Every 4 distinct points determine at least 5 distinct absolute differences (exact ints)."""
    A = list(A)
    if len(set(A)) != len(A): return False
    for q in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: return False
    return True

def ap_masks(A):
    """3-term APs of sorted A as bitmasks over sorted indices."""
    A = sorted(A); n = len(A)
    out = []
    for i, j, k in itertools.combinations(range(n), 3):
        if A[i] + A[k] == 2 * A[j]: out.append((1 << i) | (1 << j) | (1 << k))
    return out

_tau_memo = {}
def tau_bruteforce(K):
    """Minimum size of a set hitting every member of K; brute force over subsets of the active
    vertices in increasing size."""
    key = tuple(sorted(K))
    if key in _tau_memo: return _tau_memo[key]
    if not K: _tau_memo[key] = 0; return 0
    act = 0
    for t in K: act |= t
    verts = [v for v in range(act.bit_length()) if act >> v & 1]
    for k in range(0, len(verts) + 1):
        for c in itertools.combinations(verts, k):
            T = 0
            for v in c: T |= 1 << v
            if all(T & t for t in K):
                _tau_memo[key] = k; return k
    raise AssertionError

def evaluate(E, S, D):
    """E: AP masks of A. S: induced subset mask. D: avoided mask (subset of S, independent)."""
    assert D & ~S == 0
    traces = set()
    for e in E:
        if e & S == e:
            t = e & ~D
            assert t != 0, "D not independent"
            traces.add(t)
    K = [t for t in traces if not any(u != t and u & t == u for u in traces)]
    e1 = sum(1 for t in K if bin(t).count('1') == 1)
    e2 = sum(1 for t in K if bin(t).count('1') == 2)
    e3 = len(K) - e1 - e2
    tau = tau_bruteforce(K)
    Rfull = bin(S & ~D).count('1')
    act = 0
    for t in K: act |= t
    Ract = bin(act).count('1')
    sQ = 3 * Rfull + 2 * e2 + 4 * e1 - 7 * tau
    sA = 3 * Ract + 2 * e2 + 4 * e1 - 7 * tau
    sD = 9 * Rfull + 5 * e2 + 12 * e1 - 21 * tau
    return dict(tau=tau, e1=e1, e2=e2, e3=e3, Rfull=Rfull, Ract=Ract, sQ=sQ, sA=sA, sD=sD)

def independent(E, D):
    return not any(e & D == e for e in E)

def states_mode0(E, n):
    """All (S, D): S any subset, D any independent subset of S."""
    full = (1 << n) - 1
    for S in range(full + 1):
        # enumerate D subset of S
        sub = S
        while True:
            if independent(E, sub): yield S, sub
            if sub == 0: break
            sub = (sub - 1) & S

def states_mode1(E, n, kmax):
    """S = full, all independent D with |D| <= kmax."""
    full = (1 << n) - 1
    for k in range(kmax + 1):
        for c in itertools.combinations(range(n), k):
            D = 0
            for v in c: D |= 1 << v
            if independent(E, D): yield full, D

def states_mode3(E, n):
    full = (1 << n) - 1
    for D in range(full + 1):
        if independent(E, D): yield full, D

def my_hist(E, n, states):
    hQ = collections.Counter(); hA = collections.Counter(); hD = collections.Counter()
    eq = set(); cnt = 0
    for S, D in states:
        r = evaluate(E, S, D); cnt += 1
        hQ[r['sQ']] += 1; hA[r['sA']] += 1; hD[r['sD']] += 1
        if r['sQ'] == 0: eq.add((S, D, r['tau'], r['e1'], r['e2'], r['Rfull']))
    return dict(states=cnt, Q=dict(hQ), A=dict(hA), D=dict(hD), eq=eq)

def run_c(E, n, mode, param, printeq=False):
    inp = f"1 {n} {len(E)} {' '.join(map(str, E))} {mode} {param} 0\n"
    env = dict(os.environ)
    if printeq: env['PRINTEQ'] = '1'
    out = subprocess.run([BIN, '0'], input=inp, capture_output=True, text=True, env=env).stdout
    res = dict(eq=set())
    for line in out.splitlines():
        t = line.split()
        if t[0] == 'CASE':
            res.update({k: int(v) for k, v in (kv.split('=') for kv in t[2:])})
        elif t[0] == 'H':
            res[t[2]] = {int(a.split(':')[0]): int(a.split(':')[1]) for a in t[3:]}
        elif t[0] == 'EQ':
            f = dict(x.split('=') for x in t[2:])
            res['eq'].add((int(f['S']), int(f['D']), int(f['tau']), int(f['e1']), int(f['e2']), int(f['Rfull'])))
    return res

def compare(name, E, n, mode, param, states):
    t0 = time.time()
    mine = my_hist(E, n, states)
    c = run_c(E, n, mode, param, printeq=True)
    ok = (mine['states'] == c['states'] and mine['Q'] == c['Q'] and mine['A'] == c['A'] and mine['D'] == c['D']
          and mine['eq'] == c['eq'])
    out = dict(case=name, mode=mode, param=param, states=mine['states'], c_states=c['states'],
               histQ_match=mine['Q'] == c['Q'], histA_match=mine['A'] == c['A'], histD_match=mine['D'] == c['D'],
               eq_states_match=mine['eq'] == c['eq'], n_eq=len(mine['eq']),
               minQ=min(mine['Q']), minA=min(mine['A']), minD=min(mine['D']),
               violQ_c=c['violQ'], violD4_c=c['violD4'], violD4_mine=sum(v for s, v in mine['D'].items() if s < 0),
               all_match=ok, secs=round(time.time() - t0, 1))
    print(json.dumps(out), flush=True)
    return out

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'fg'
    recs = json.load(open(os.path.join(ROOT, 'data', 'small_records.json')))['sets']
    results = {'compare': [], 'sets45': [], 'notes': []}
    if which == 'fg':
        # 0. the sanity case from scratch
        A12b = recs['12b']['set']; E = ap_masks(A12b); n = 12
        assert is45(A12b)
        D = 1 << sorted(A12b).index(287)
        r = evaluate(E, (1 << n) - 1, D)
        results['sanity_12b_D287'] = dict(r, D4_lhs=21 * r['tau'], D4_rhs=9 * r['Rfull'] + 5 * r['e2'] + 12 * r['e1'],
                                          Q8_lhs=7 * r['tau'], Q8_rhs=3 * r['Rfull'] + 2 * r['e2'] + 4 * r['e1'], n_aps=len(E))
        print('sanity 12b D={287}:', results['sanity_12b_D287'], flush=True)
        # D=empty on A_base and single-point D on the 12-pt sets
        Ab = recs['14']['set']; Eb = ap_masks(Ab); assert is45(Ab)
        r = evaluate(Eb, (1 << 14) - 1, 0); results['Abase_Dempty'] = r; print('A_base D=empty', r)
        # 1. exhaustive histogram + equality-state comparisons against the C binary
        for key in ['8', '10', '11']:
            A = recs[key]['set']; E = ap_masks(A); n = len(A); assert is45(A)
            results['compare'].append(compare(f'record{key}_mode0_all3^n', E, n, 0, 0, states_mode0(E, n)))
        for key in ['14', '12', '12b', '12c']:
            A = recs[key]['set']; E = ap_masks(A); n = len(A); assert is45(A)
            results['compare'].append(compare(f'record{key}_mode3_Sfull_allD', E, n, 3, 0, states_mode3(E, n)))
            results['compare'].append(compare(f'record{key}_mode1_Dle3', E, n, 1, 3, states_mode1(E, n, 3)))
        # random pool sets: mode 1 |D|<=2 (n=14,16) and mode 3 (n=12)
        rs = json.load(open(os.path.join(FALS, 'random_sets.json'))); ad = json.load(open(os.path.join(FALS, 'adv_sets.json')))
        rng = random.Random(2026)
        for src, pool in (('random', rs), ('adv', ad)):
            for nk in ('12', '14', '16'):
                for idx in rng.sample(range(len(pool[nk])), 2):
                    A = pool[nk][idx]; E = ap_masks(A); n = len(A)
                    if n == 12: results['compare'].append(compare(f'{src}{nk}#{idx}_mode3', E, n, 3, 0, states_mode3(E, n)))
                    else: results['compare'].append(compare(f'{src}{nk}#{idx}_mode1_Dle2', E, n, 1, 2, states_mode1(E, n, 2)))
        # 2. exact (4,5) re-check of 20 pool sets (10 random, 10 adversarial) + saturation count
        for src, pool in (('random', rs), ('adv', ad)):
            for nk in ('12', '14', '16'):
                for idx in rng.sample(range(len(pool[nk])), 4 if nk != '16' else 2):
                    A = pool[nk][idx]; t0 = time.time()
                    ok = is45(A); m = len(ap_masks(A))
                    results['sets45'].append(dict(src=src, n=int(nk), idx=idx, is45=ok, n_aps=m, saturated=(m == len(A) - 2), distinct=len(set(A)) == len(A)))
        print('sets45:', sum(1 for s in results['sets45'] if s['is45']), '/', len(results['sets45']), 'are (4,5)-sets;',
              sum(1 for s in results['sets45'] if s['saturated']), 'saturated', flush=True)
        # 3. the 5 stored 3-piece amalgams from step3b: exact (4,5) check
        s3 = json.load(open(os.path.join(FALS, 'step3b_results.json')))
        results['amalgams45'] = [dict(names=m[0], n=len(m[1]), is45=is45(m[1]), n_aps=len(ap_masks(m[1]))) for m in s3['meta']]
        print('amalgams:', results['amalgams45'], flush=True)
        json.dump(results, open(os.path.join(HERE, 'indep_check_fg.json'), 'w'), indent=1, default=list)
    elif which == 'bg12b':
        A = recs['12b']['set']; E = ap_masks(A); n = 12
        r = compare('record12b_mode0_all3^12', E, n, 0, 0, states_mode0(E, n))
        json.dump(r, open(os.path.join(HERE, 'indep_check_bg12b.json'), 'w'), indent=1)
    elif which == 'bg14':
        A = recs['14']['set']; E = ap_masks(A); n = 14
        r = compare('record14_mode1_Dle5', E, n, 1, 5, states_mode1(E, n, 5))
        json.dump(r, open(os.path.join(HERE, 'indep_check_bg14.json'), 'w'), indent=1)
