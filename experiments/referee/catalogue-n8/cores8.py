"""Independent recount of the minimal forbidden cores at n=8 (no e757).
A core is a full-support pattern S (every rank 0..7 used) that forces a relation R while no S minus one
edge forces R: R = order-infeasibility, an unlisted AP (a,b,c), or a parallelogram (a,b,c,d).
Deduplicated under reflection (relation reflected too).  Compared with data/forbidden_ordered_n8.json."""
import itertools, sys, os, json, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from census8 import patterns
from recompute import eq_rows, nullspace, fm_point, reflect

N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))


def analyse(n, edges):
    """Returns ('order', None) if order-infeasible, else ('ok', set of forced relations)."""
    rows = eq_rows(n, edges)
    Nb = nullspace(rows, n)
    d = len(Nb)
    ineqs = [[Nb[j][r + 1] - Nb[j][r] for j in range(d)] for r in range(n - 1)]
    if fm_point(ineqs, d) is None:
        return "order", None
    listed = {frozenset(e) for e in edges}
    rels = set()
    for a, b, c in itertools.combinations(range(n), 3):
        if frozenset((a, b, c)) not in listed and all(Nj[a] + Nj[c] - 2 * Nj[b] == 0 for Nj in Nb):
            rels.add(("extra_ap", (a, b, c)))
    for a, b, c, dd in itertools.combinations(range(n), 4):
        if all(Nj[a] + Nj[dd] - Nj[b] - Nj[c] == 0 for Nj in Nb):
            rels.add(("diff", (a, b, c, dd)))
    return "ok", rels


def refl_rel(n, rel):
    if rel[0] == "order":
        return rel
    return (rel[0], tuple(sorted(n - 1 - v for v in rel[1])))


def main():
    t0 = time.time()
    cache = {}
    def an(edges):
        if edges not in cache:
            cache[edges] = analyse(N, edges)
        return cache[edges]
    cores = set()
    for p in patterns(N):
        if not p or {v for e in p for v in e} != set(range(N)):
            continue
        p = tuple(sorted(p))
        kind, rels = an(p)
        subs = [tuple(e for e in p if e != d) for d in p]
        if kind == "order":
            if all(an(s)[0] == "ok" for s in subs):
                a = (p, ("order",)); b = (reflect(N, p), ("order",))
                cores.add(min(a, b))
            continue
        subrels = [an(s) for s in subs]
        for rel in rels:
            if all(sk == "ok" and rel not in sr for sk, sr in subrels):
                a = (p, rel); b = (reflect(N, p), refl_rel(N, rel))
                cores.add(min(a, b))
    kinds = Counter(r[0] for _, r in cores)
    byedges = Counter(len(p) for p, _ in cores)
    print(f"n={N}: {len(cores)} minimal cores (mine), kinds {dict(kinds)}, by #edges {dict(sorted(byedges.items()))}  {time.time()-t0:.0f}s")
    lib = json.load(open(os.path.join(REPO, f"data/forbidden_ordered_n{N}.json")))
    theirs = set()
    for c in lib["cores"]:
        if c["n"] != N:
            continue
        p = tuple(sorted(tuple(e) for e in c["edges"]))
        rel = ("order",) if c["kind"] == "order" else (c["kind"], tuple(c["relation"]))
        theirs.add(min((p, rel), (reflect(N, p), refl_rel(N, rel))))
    print(f"library: {len(theirs)} cores at n={N}; mine - theirs: {len(cores - theirs)}; theirs - mine: {len(theirs - cores)}")
    for x in sorted(cores ^ theirs)[:10]:
        print("  differs:", x, "mine" if x in cores else "theirs")
    print("CORES EQUAL:", cores == theirs)


if __name__ == "__main__":
    main()
