"""Recompute, with own code, n, m, membership in C_3, tau, A, DEF (over all 32 pieces
of L*) and A + DEF for the 18 graphs of experiments/20261027-0730-kt-cells/lists/
cell_27_13_9_D3.txt; also pairwise non-isomorphism and the perfect-matching
structure. Pieces are read from experiments/prover/L021/closure_results.json and
re-verified (n, m, tau, W, s) here."""
import json, re, sys, time
from itertools import combinations
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rlib import (tau, min_transversals, degrees, is_linear, is_connected, p3_ok,
                  p3_ok_hall, has_F7, iso, induced_copies, deficiency, A_of, s_of, masks)

ROOT = "/home/user/Erdos-757/"
t0 = time.time()
pieces = json.load(open(ROOT + "experiments/prover/L021/closure_results.json"))["pieces"]
assert len(pieces) == 32
for p in pieces:
    E = [tuple(e) for e in p["edges"]]
    n = 1 + max(max(e) for e in E)
    t = tau(n, E)
    assert n == p["n"] and len(E) == p["m"] and t == p["tau"], p["name"]
    assert -A_of(n, len(E), t) == p["W"] and p["W"] > 0
    assert is_linear(E) and is_connected(n, E) and max(degrees(n, E)) <= 3
    assert s_of(n, len(E), t) in (0, 1)
print(f"32 pieces re-verified (n, m, tau, W, s in {{0,1}}, linear, connected, Delta<=3) [{time.time()-t0:.1f}s]")

graphs = []
for line in open(ROOT + "experiments/20261027-0730-kt-cells/lists/cell_27_13_9_D3.txt"):
    if line.startswith("FOUND:"):
        E = [tuple(int(x) for x in g.split(",")) for g in re.findall(r"\(([^)]*)\)", line)]
        graphs.append(E)
print("graphs read:", len(graphs))

allok = True
Avals, DEFs, Ps = [], [], []
for gi, E in enumerate(graphs):
    n = 1 + max(max(e) for e in E)
    m = len(E)
    assert len(set(tuple(sorted(e)) for e in E)) == m and all(len(set(e)) == 3 for e in E)
    used = set(v for e in E for v in e)
    conn = is_connected(n, E)
    lin = is_linear(E)
    dmax = max(degrees(n, E))
    p3 = p3_ok(E)
    p3h = p3_ok_hall(n, E)
    f7 = has_F7(E)
    t = tau(n, E)
    # perfect matching: 9 pairwise disjoint edges covering all 27 vertices
    em = masks(E)
    pm = [F for F in combinations(range(m), 9) if bin(sum(em[i] for i in F)).count("1") == 27]
    A = A_of(n, m, t)
    copies = []
    for p in pieces:
        PE = [tuple(e) for e in p["edges"]]
        for U in induced_copies(n, E, PE, p["n"]):
            copies.append((U, p["W"], p["name"]))
    names = sorted(set(c[2] for c in copies))
    D, fam = deficiency(E, [(c[0], c[1]) for c in copies])
    P = A + D
    good = (n == 27 and m == 13 and len(used) == 27 and conn and lin and dmax <= 3 and p3 and p3h
            and not f7 and t == 9 and n == 2 * m + 1 and len(pm) >= 1 and A == -4 and D == 4 and P == 0)
    allok &= good
    Avals.append(A); DEFs.append(D); Ps.append(P)
    print(f"#{gi:2d}: n={n} m={m} conn={conn} lin={lin} Dmax={dmax} P3={p3}/{p3h} F7={f7} tau={t} "
          f"#perfect_matchings={len(pm)} A={A} copies={len(copies)} {names} "
          f"DEF={D} (family size {len(fam)}) A+DEF={P} {'OK' if good else 'FAIL'}")

# pairwise non-isomorphism
noniso = all(not iso(graphs[i], graphs[j]) for i, j in combinations(range(len(graphs)), 2))
print("pairwise non-isomorphic:", noniso)
allok &= noniso and len(graphs) == 18
print(f"A values {sorted(set(Avals))}, DEF values {sorted(set(DEFs))}, A+DEF values {sorted(set(Ps))}")
print("ALL OK" if allok else "SOME FAILURE", f"[{time.time()-t0:.1f}s]")
