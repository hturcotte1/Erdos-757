import itertools

A_base = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]

def is_45_set(A):
    """
    Check (4,5)-set: every 4-subset determines at least 5 distinct absolute differences
    among its 6 pairwise differences.
    Return (ok, witness_quad, diffs) where witness_quad/diffs are provided if fails.
    """
    for quad in itertools.combinations(A, 4):
        diffs = {abs(x - y) for x, y in itertools.combinations(quad, 2)}
        if len(diffs) < 5:
            return False, quad, diffs
    return True, None, None

def is_sidon_subset(S):
    """
    Sidon condition (standard for sets of reals):
    all sums x+y with x<=y are distinct as unordered pairs.
    """
    S = sorted(S)
    seen = {}  # sum -> pair (x,y) with x<=y
    for i, x in enumerate(S):
        for j in range(i, len(S)):
            y = S[j]
            s = x + y
            pair = (x, y)
            if s in seen and seen[s] != pair:
                return False
            seen[s] = pair
    return True

def h_of_set(A):
    """
    Compute h(A): maximum size of a Sidon subset of A.
    Brute force over all subsets: 2^14 = 16384, very fast.
    Return (h, witness_subset).
    """
    n = len(A)
    best = 0
    witness = None
    for mask in range(1 << n):
        bits = mask.bit_count()
        if bits <= best:
            continue
        S = [A[i] for i in range(n) if (mask >> i) & 1]
        if is_sidon_subset(S):
            best = bits
            witness = sorted(S)
    return best, witness

if __name__ == "__main__":
    # 1) output the size
    print("|A_base| =", len(A_base))

    # 2) verify (4,5)-set
    ok, bad_quad, bad_diffs = is_45_set(A_base)
    if ok:
        print("A_base is a (4,5)-set: YES")
    else:
        print("A_base is a (4,5)-set: NO")
        print("Counterexample 4-subset:", bad_quad)
        print("Distinct diffs:", sorted(bad_diffs), "count =", len(bad_diffs))

    # 3) compute and verify h(A_base)=8
    h, witness = h_of_set(A_base)
    print("h(A_base) =", h)
    print("One maximum Sidon subset witness:", witness)
    if h == 8:
        print("h(A_base)=8: VERIFIED")
    else:
        print("h(A_base)=8: FAILED")