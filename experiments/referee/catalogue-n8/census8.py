"""Independent recount of the n=8 census (no e757): all linear, midpoint-injective ordered patterns on
ranks 0..7 (every interior rank is the midpoint of at most one edge; two edges share <= 1 rank),
up to reflection, classified O > E > D > R with the same exact oracle as recompute.py (no realization
point is produced here; R = order-feasible with no forced relation, which is realizable by genericity).
Prints running totals so that a timeout still leaves partial information."""
import itertools, sys, time, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute import eq_rows, nullspace, fm_point, dot, F, reflect

N = int(sys.argv[1]) if len(sys.argv) > 1 else 8


def patterns(n):
    res = []
    def rec(j, edges, used):
        if j == n - 1:
            res.append(tuple(edges)); return
        rec(j + 1, edges, used)
        for i in range(j):
            for k in range(j + 1, n):
                prs = [(i, j), (j, k), (i, k)]
                if any(p in used for p in prs):
                    continue
                rec(j + 1, edges + [(i, j, k)], used | set(prs))
    rec(1, [], frozenset())
    return res


def classify(n, edges):
    rows = eq_rows(n, edges)
    Nb = nullspace(rows, n)
    d = len(Nb)
    ineqs = [[Nb[j][r + 1] - Nb[j][r] for j in range(d)] for r in range(n - 1)]
    if fm_point(ineqs, d) is None:
        return "O"
    listed = {frozenset(e) for e in edges}
    for a, b, c in itertools.combinations(range(n), 3):
        if frozenset((a, b, c)) in listed:
            continue
        if all(Nj[a] + Nj[c] - 2 * Nj[b] == 0 for Nj in Nb):
            return "E"
    for a, b, c, dd in itertools.combinations(range(n), 4):
        if all(Nj[a] + Nj[dd] - Nj[b] - Nj[c] == 0 for Nj in Nb):
            return "D"
    return "R"


def main():
    t0 = time.time()
    pats = patterns(N)
    seen = set()
    todo = []
    for p in pats:
        if not p:
            continue
        c = min(p, reflect(N, p))
        if c not in seen:
            seen.add(c); todo.append(c)
    print(f"n={N}: {len(pats)} raw patterns, {len(todo)} non-empty up to reflection", flush=True)
    cnt = Counter()
    for i, p in enumerate(todo):
        cnt[classify(N, p)] += 1
        if (i + 1) % 5000 == 0:
            print(f"  {i+1}/{len(todo)} {dict(cnt)} {time.time()-t0:.0f}s", flush=True)
    print(f"FINAL n={N}: total {len(todo)} {dict(cnt)}  {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
