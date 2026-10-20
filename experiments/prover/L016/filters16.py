"""(L016) Audit of a stored cell list: python3 filters16.py LISTFILE n m t D K SEED
(1) Python: every line has exactly m distinct triples on labels 0..n-1, max degree <= D; (2) `bin/filt FOUND n notau` on all lines:
all linear, none contains F7, none violates (P3), all connected on n vertices (survivors = survivors_connected = number of lines);
(2') tau = t exactly for every line: `bin/ext_d n t t+2 1 0` (original Gosper enumeration, MAXP 640) if n <= 22, else
`bin/ext_d_fast n t t+2 1 0` (branching enumeration; C6), whose SUMMARY must show bad_tau = 0 (no cover of size t-1, some cover of
size t) and tg_too_small = number of lines (no extension search); (3) `bin/canon n` maps every line to itself (the list consists of canonical forms) and the
lines are distinct (distinct canonical forms = pairwise non-isomorphic); (4) pyverify (pure Python, L014) on K random lines (seed):
linear, F7-free, (P3), connected, tau = t exactly, max degree <= D."""
import sys, os, re, random, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pyverify as pv
fn = sys.argv[1]; n, m, t, D, K, seed = map(int, sys.argv[2:8])
lines = [l.strip() for l in open(fn) if l.startswith('FOUND:')]
probs = 0
def E_of(l): return [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
for l in lines:
    E = E_of(l); deg = collections.Counter(v for e in E for v in e)
    if len(E) != m or len(set(frozenset(e) for e in E)) != m or any(len(set(e)) != 3 for e in E) or not set(deg) <= set(range(n)) or max(deg.values()) > D:
        probs += 1
r = subprocess.run([os.path.join(HERE, 'bin', 'filt'), 'FOUND', str(n), 'notau'], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True)
summ = r.stdout.strip().splitlines()[-1]; kv = dict(x.split('=', 1) for x in summ.split() if '=' in x)
ok_filt = (int(kv['total']) == len(lines) == int(kv['linear']) == int(kv['survivors']) == int(kv['survivors_connected']) and int(kv['contain_F7']) == 0
           and int(kv['P3_violated']) == 0)
tb = os.path.join(HERE, 'bin', 'ext_d' if n <= 22 else 'ext_d_fast')
tin = '\n'.join('%d ' % m + ' '.join('%d %d %d' % e for e in E_of(l)) for l in lines) + '\n'
ts = subprocess.run([tb, str(n), str(t), str(t + 2), '1', '0'], input=tin, capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]
tkv = dict(x.split('=', 1) for x in ts.split() if '=' in x)
ok_tau = int(tkv['graphs']) == len(lines) and int(tkv['bad_tau']) == 0 and int(tkv['tg_too_small']) == len(lines)
summ = summ + ' | tau oracle %s: %s -> %s' % (os.path.basename(tb), ts, 'tau=t for all' if ok_tau else 'PROBLEM')
ok_filt = ok_filt and ok_tau
c = subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True).stdout.splitlines()
cf = ['FOUND: ' + ' '.join('(%s)' % p.replace('.', ',') for p in x.split()[2:]) for x in c]
fixed = sum(1 for a, b in zip(lines, cf) if a == b); distinct = len(set(lines))
samp = random.Random(seed).sample(range(len(lines)), min(K, len(lines))); pvbad = 0
for i in samp:
    E = E_of(lines[i]); V = list(range(n))
    if not (pv.linear(E) and not pv.has_f7(E) and pv.p3(E) and pv.connected(E, V) and pv.tau(E) == t and pv.maxdeg(E) <= D): pvbad += 1
print('AUDIT %s (%d,%d,%d,%d): lines %d, python-structure problems %d; filt: %s -> %s; canon fixed points %d of %d, distinct lines %d; pyverify sample %d (seed %d), failures %d'
      % (os.path.basename(fn), n, m, t, D, len(lines), probs, summ, 'OK' if ok_filt else 'PROBLEM', fixed, len(lines), distinct, len(samp), seed, pvbad))
print('RESULT audit', 'OK' if (probs == 0 and ok_filt and fixed == len(lines) == distinct and pvbad == 0) else 'PROBLEMS')
