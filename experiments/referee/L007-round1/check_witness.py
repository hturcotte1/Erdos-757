"""Referee check of Step 7 witnesses from the definitions (plain Python, no e757/judge)."""
import itertools
def is45(A):
    for q in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: return False
    return True
def aps(A):
    S = set(A); return [(a, (a + c) // 2, c) for a, c in itertools.combinations(sorted(A), 2) if (a + c) % 2 == 0 and (a + c) // 2 in S]
def is_sidon(B):
    sums = set()
    for i, x in enumerate(B):
        for y in B[i:]:
            s = x + y
            if s in sums: return False
            sums.add(s)
    return True
def h(A):
    A = sorted(A)
    for k in range(len(A), 0, -1):
        if any(is_sidon(list(B)) for B in itertools.combinations(A, k)): return k
W = [0,323,523,566,569,572,595,609,621,646,723,851,919,1379]
fib = [2,3]
while len(fib) < 14: fib.append(fib[-1] + fib[-2])
for name, A in [('W', W), ('Fib F3..F16', fib)]:
    print(name, A, 'n', len(A), 'distinct', len(set(A)) == len(A), '(4,5):', is45(A), 'APs:', len(aps(A)), 'h:', h(A))
print('W APs:', aps(W))
Ab = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
Wp = sorted([x for x in Ab if x != 136] + [-323])
print('W-323 == (A_base minus 136) + {-323}:', sorted(x - 323 for x in W) == Wp)
