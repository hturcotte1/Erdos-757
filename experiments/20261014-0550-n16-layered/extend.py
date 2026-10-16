"""Extension step: attach vertex N-1 to every layer-1 hypergraph H' (on N-1 vertices) so that the result H
has exactly M edges, alpha(H) <= T and satisfies all of O' (linear, injective midpoints, F7-free, K30, K31,
cores <= 4 edges).  Justification (lemma, see README): H - (N-1) = H' has m' = M - d edges, and the d edges
(i, j, N-1) have j among the vertices of 1..N-2 that are not midpoints of H' (all of them if M = N-2; all
but one if M = N-3; in general d of them).
Usage: python3 extend.py N T M SHARD NSHARDS   (reads results/n{N-1}_m{m'}_solutions.jsonl for every m' with
1 <= M-m' <= 5; writes results/n{N}_m{M}_ext_shard{SHARD}.json[l] atomically; skips if the JSON exists)
Merge/dedupe/realize: python3 finalize.py N M"""
import sys as _s, os as _o; _s.path.insert(0, _o.path.abspath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "..")))
import itertools, json, os, sys, time
from e757.cpsat_model import (load_cores, satisfies_all, independent_sets, find_f7)
from e757.saturated import alpha_of_edges

N, T, M, SH, NSH = (int(x) for x in sys.argv[1:6])
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.abspath(os.path.join(here, "..", ".."))
res = os.path.join(here, "results")
out_path = os.path.join(res, "n%d_m%d_ext_shard%d.json" % (N, M, SH))
if os.path.exists(out_path):
    print("SKIP", out_path); sys.exit(0)
cores4 = [c for c in load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
          if len(c["edges"]) <= 4]
NP, V = N - 1, N - 1   # H' lives on 0..NP-1; the new vertex is V = N-1 (the maximum)


def extensions(edges, d):
    """All sets of d new edges (i, j, V) giving a valid hypergraph with alpha <= T (before the cheap global checks)."""
    E = [tuple(e) for e in edges]
    mids = {j for _, j, _ in E}
    nonmid = [j for j in range(1, N - 1) if j not in mids]   # candidates for the new midpoints (includes NP-1)
    if d > len(nonmid) or d < 1:
        return []
    pairs_used = set()
    for a, b, c in E:
        pairs_used |= {(a, b), (b, c), (a, c)}
    # independent sets of H' of size T must each contain a pair (i, j) of a new edge
    ind = independent_sets(NP, E, T, limit=10**7) if T <= NP else []
    ind_masks = [sum(1 << v for v in I) for I in ind]
    results = set()

    def cand_pairs(used_v, used_j):
        out = []
        for j in nonmid:
            if j in used_j or j in used_v:
                continue
            for i in range(j):
                if i in used_v or i in used_j or (i, j) in pairs_used:
                    continue
                out.append((i, j))
        return out

    def rec(chosen, used_v, used_j):
        unc = [m for m in ind_masks if not any(((m >> i) & 1) and ((m >> j) & 1) for i, j in chosen)]
        if len(chosen) == d:
            if not unc:
                results.add(frozenset(chosen))
            return
        if unc:
            if len(chosen) == d:
                return
            # branch on the uncovered independent set with the fewest candidate pairs
            cp = cand_pairs(used_v, used_j)
            best, bestc = None, None
            for m in unc:
                c = [(i, j) for i, j in cp if (m >> i) & 1 and (m >> j) & 1]
                if bestc is None or len(c) < len(bestc):
                    best, bestc = m, c
                    if len(c) <= 1:
                        break
            for i, j in bestc:
                rec(chosen + [(i, j)], used_v | {i, j}, used_j | {j})
        else:
            # everything is covered: complete with arbitrary further edges (d - len(chosen) of them)
            cp = cand_pairs(used_v, used_j)
            for i, j in cp:
                rec(chosen + [(i, j)], used_v | {i, j}, used_j | {j})
    rec([], frozenset(), frozenset())
    return [[(i, j, V) for i, j in sorted(r)] for r in results]


def main():
    t0 = time.time()
    n_hp = n_ext = n_ok = 0
    sols = set()
    for mp in range(max(1, M - 5), M):
        f = os.path.join(res, "n%d_m%d_solutions.jsonl" % (NP, mp))
        if not os.path.exists(f):
            print("MISSING stream", f); continue
        d = M - mp
        for ln, line in enumerate(open(f)):
            if ln % NSH != SH:
                continue
            edges = [tuple(e) for e in json.loads(line)]
            n_hp += 1
            for new in extensions(edges, d):
                n_ext += 1
                H = edges + new
                if alpha_of_edges(N, H) > T:
                    continue
                if not satisfies_all(N, H, cores=cores4):
                    continue
                n_ok += 1
                sols.add(tuple(sorted(H)))
    out = {"N": N, "T": T, "M": M, "shard": SH, "nshards": NSH, "n_Hprime": n_hp, "n_candidates": n_ext,
           "n_solutions": len(sols), "wall_s": round(time.time() - t0, 1),
           "solutions": [[list(e) for e in s] for s in sorted(sols)]}
    json.dump(out, open(out_path + ".tmp", "w")); os.replace(out_path + ".tmp", out_path)
    print("DONE shard", SH, {k: v for k, v in out.items() if k != "solutions"})


main()
