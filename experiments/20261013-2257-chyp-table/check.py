"""Re-verify every witness in witnesses.json independently of the solver:
alpha (e757.saturated.alpha_of_edges), linearity (is_linear), midpoint injectivity and range, and
F7-freeness by brute force over all 7-subsets (no use of cpsat_model.find_f7)."""
import itertools, json, os, sys
from e757.saturated import alpha_of_edges, is_linear
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]

def f7_free_bruteforce(edges):
    es = {frozenset(e) for e in edges}
    # F7 copy = injective map of {0..6} to vertices sending the 5 blocks onto edges
    verts = sorted({v for e in edges for v in e})
    for img in itertools.permutations(verts, 7):
        if all(frozenset(img[v] for v in blk) in es for blk in F7):
            return False
    return True

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "witnesses.json")
    W = json.load(open(path))
    bad = 0
    for key, w in sorted(W.items()):
        n, edges = w["n"], [tuple(e) for e in w["edges"]]
        ok = all(0 <= i < j < k < n for i, j, k in edges)
        ok &= len({j for _, j, _ in edges}) == len(edges)
        ok &= is_linear(edges)
        ok &= alpha_of_edges(n, edges) == w["alpha"]
        if w["f7_free"]:
            # brute force over permutations is 7!*C(v,7); fine here since v <= 16 only via pruning:
            ok &= f7_free_bruteforce_fast(edges)
        print(key, "OK" if ok else "FAIL", "n=%d m=%d alpha=%d" % (n, len(edges), w["alpha"]))
        bad += not ok
    sys.exit(1 if bad else 0)

def f7_free_bruteforce_fast(edges):
    """Independent F7 test: backtracking over vertex images (not the structural method of cpsat_model)."""
    es = {frozenset(e) for e in edges}
    verts = sorted({v for e in edges for v in e})
    def rec(img):
        t = len(img)
        for blk in F7:
            if max(blk) < t and frozenset(img[v] for v in blk) not in es:
                return None
        if t == 7:
            return img
        for v in verts:
            if v not in img:
                r = rec(img + [v])
                if r:
                    return r
        return None
    return rec([]) is None

if __name__ == "__main__":
    main()
