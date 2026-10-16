"""README claim: 'The 12 failing orders of the four realizable triangle labelings (4.3-4.6) are all K30
violations (2-edge order cores)'.  Check: for every O order of labelings 4.3-4.6, some PAIR of its
edges is already order-infeasible (exact Fourier-Motzkin, no e757)."""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute import eq_rows, nullspace, fm_point, rank_form, reflect, verdict

TRI_E = [("a", "b", "c"), ("a", "d", "e"), ("b", "d", "f")]


def lab(edges, mids):
    return [tuple([v for v in e if v != m][:1] + [m] + [v for v in e if v != m][1:]) for e, m in zip(edges, mids)]


def infeasible(n, edges):
    Nb = nullspace(eq_rows(n, edges), n)
    return fm_point([[Nj[r + 1] - Nj[r] for Nj in Nb] for r in range(n - 1)], len(Nb)) is None


verts = list("abcdef")
n = 6
total_O = 0
all_k30 = True
for name, mids in (("4.3", "adb"), ("4.4", "adf"), ("4.5", "aed"), ("4.6", "aef")):
    L = lab(TRI_E, mids)
    pats = set()
    for pr in itertools.permutations(range(n)):
        rf = rank_form(dict(zip(verts, pr)), L)
        if rf is not None:
            pats.add(min(rf, reflect(n, rf)))
    nO = 0
    for rf in sorted(pats):
        v, _ = verdict(n, rf)
        if v == "O":
            nO += 1
            pair = any(infeasible(n, list(pr)) for pr in itertools.combinations(rf, 2))
            all_k30 &= pair
            print(f"{name} O-order {list(rf)}: 2-edge infeasible sub-pattern exists: {pair}")
        elif v != "R":
            print(f"{name} unexpected verdict {v} for {rf}")
    total_O += nO
    print(f"{name}: {len(pats)} orders, {nO} O")
print(f"TOTAL failing orders of 4.3-4.6: {total_O} (claimed 12); all K30 (2-edge) : {all_k30}")
