"""An explicit 20-point (4,5)-set with h = 12 (so f(20) <= 12), checked from the definitions.  Construction (the gluing idea of
Ma-Tang Lemma 3.6 with explicit numbers): A_base plus two far 3-term APs {T1, T1+q1, T1+2q1} and {T2, T2+q2, T2+2q2}; the first
(q1, q2) found by a small search that makes the 20-point set a (4,5)-set is used.  h <= 8 + 2 + 2 = 12 is then verified directly."""
import itertools, json, sys
def nd(q): return len({abs(a - b) for a, b in itertools.combinations(q, 2)})
def is45(A): return all(nd(q) >= 5 for q in itertools.combinations(A, 4))
def sidon(S):
    s = [x + y for i, x in enumerate(S) for y in S[i:]]; return len(s) == len(set(s))
AB = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
T1, T2 = 5000, 20000
found = None
for q1 in range(101, 400):
    B = sorted(AB + [T1, T1 + q1, T1 + 2 * q1])
    if not is45(B): continue
    for q2 in range(q1 + 1, 2000):
        C = sorted(B + [T2, T2 + q2, T2 + 2 * q2])
        if is45(C): found = (q1, q2, C); break
    if found: break
q1, q2, C = found
aps = [(a, b, c) for a, b, c in itertools.combinations(C, 3) if a + c == 2 * b]
h12 = any(sidon(S) for S in itertools.combinations(C, 12)); h13 = any(sidon(S) for S in itertools.combinations(C, 13))
print('q1 =', q1, 'q2 =', q2); print('C =', C)
print('(4,5):', is45(C), '(4,845 four-subsets) | APs:', len(aps), '| Sidon 12-subset:', h12, '| Sidon 13-subset:', h13)
sys.path.insert(0, '/home/user/Erdos-757'); from e757.core import alpha, ap_edges
print('e757.core: m =', len(ap_edges(C)), 'h =', alpha(C))
json.dump(dict(set=C, n=20, m=len(aps), h=12 if (h12 and not h13) else None, q1=q1, q2=q2), open('witness_20.json', 'w'))
