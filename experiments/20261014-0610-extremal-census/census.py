"""Census of extremal abstract solutions (class O': linear, midpoint-injective, F7-free, K30, K31, cores<=4 edges)
with exactly M edges and alpha <= T on N vertices, and of their realizations.
Stage 1 (enumerate): e757.cpsat_model.enumerate_native (all solutions, eager alpha/F7 clauses; the lazy
  enumerate_solutions loop re-solves from scratch per solution and is ~100x slower).  Instead of the lex
  symmetry constraint (which adds auxiliary variables and would multiply solutions) every solution is reduced
  afterwards to the canonical representative min(edges, reflected edges) (sorted tuples); the abstract count
  reported is the number of canonical classes.  Resumable: a finished (N, M) stream is skipped.
Stage 2 (process): realize_exact on every canonical solution; realizable ones -> integer sets, verified with
  e757.core.alpha / is_45_set; affine normalization (translate min to 0, divide by gcd, lexicographically smaller
  of the set and its reflection).  Patterns whose AP-equation system has rank N-2 are rigid (unique up to affine
  maps); flexible patterns give a continuum, one generic representative is stored.
Usage: python3 census.py N T M TIME_LIMIT_S"""
import sys as _s, os as _o; _s.path.insert(0, _o.path.abspath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "..")))
import json, math, os, sys, time
from e757.cpsat_model import enumerate_native, load_cores
from e757.core import alpha, is_45_set, ap_edges
from e757.realizability import realize_exact, _rref, _x_rows
from e757.saturated import map_of_set, edges_of_map

N, T, M, TL = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.abspath(os.path.join(here, "..", ".."))
res = os.path.join(here, "results"); os.makedirs(res, exist_ok=True)
base = os.path.join(res, "n%d_m%d" % (N, M))
prog = base + "_progress.json"
fin = base + "_census.json"
if os.path.exists(fin):
    print("SKIP finished", fin); sys.exit(0)
if not (os.path.exists(prog) and json.load(open(prog))["status"] == "EXHAUSTED"):
    cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")
    cnt, st = enumerate_native(N, T, M, base + "_solutions.jsonl", time_limit=TL, progress_path=prog,
                               cores=cores, core_max_edges=4)
    print("ENUM", N, T, M, st, cnt, flush=True)
else:
    print("enumeration already exhausted", flush=True)
status = json.load(open(prog))["status"]


def canon(edges):
    t = tuple(sorted(tuple(e) for e in edges))
    r = tuple(sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in t))
    return min(t, r)


def normalize(vals):
    v = sorted(vals); lo = v[0]; v = [x - lo for x in v]
    g = 0
    for x in v: g = math.gcd(g, x)
    v = [x // g for x in v]
    r = sorted(v[-1] - x for x in v)
    return tuple(min(v, r))


canon_set = set()
raw = 0
for line in open(base + "_solutions.jsonl"):
    raw += 1
    canon_set.add(canon(json.loads(line)))
sols = sorted(canon_set)
realizable, reasons, classes = [], {}, {}
rigid = 0
for t in sols:
    r = realize_exact(N, list(t))
    if not r[0]:
        reasons[r[1]] = reasons.get(r[1], 0) + 1
        continue
    vals = sorted(r[1])
    E = ap_edges(vals)
    h = alpha(vals, E)
    ok45 = is_45_set(vals)
    R, piv = _rref(_x_rows(N, list(t)), N)
    is_rigid = (N - len(piv)) == 2
    rigid += is_rigid
    realizable.append({"edges": [list(e) for e in t], "set": vals, "h": h, "is_45": ok45, "rigid": is_rigid})
    classes.setdefault(normalize(vals), []).append(len(realizable) - 1)
# known sets
known = {}
data = json.load(open(repo + "/data/small_records.json"))["sets"]
from e757 import core as _core
cands = {("record_" + k): v["set"] for k, v in data.items() if len(v["set"]) == N}
cands.update({"core.KNOWN: " + k: v for k, v in _core.KNOWN.items() if len(v) == N})
for name, A in cands.items():
    lo, hi, mid = map_of_set(A)
    pat = canon(edges_of_map(mid))
    known[name] = {"pattern_in_abstract_solutions": pat in canon_set,
                   "normalized_set_in_realized_classes": normalize(A) in classes, "h": alpha(sorted(A))}
out = {"N": N, "T": T, "M": M, "enumeration_status": status, "raw_solutions": raw,
       "abstract_classes_up_to_reflection": len(sols), "n_realizable": len(realizable),
       "n_rigid_realizable": rigid, "n_affine_classes_of_stored_sets": len(classes),
       "unrealizable_reasons": reasons,
       "all_h_equal_T": all(r["h"] == T for r in realizable), "all_45": all(r["is_45"] for r in realizable),
       "record_beating": [r for r in realizable if 7 * r["h"] < 4 * N], "known_sets": known}
json.dump(realizable, open(os.path.join(here, "results_sets_n%d.json" % N), "w"))
if status == "EXHAUSTED":
    json.dump(out, open(fin, "w"))
else:   # partial: do not mark as finished (so a relaunch continues/enumerates again)
    json.dump(out, open(base + "_partial_census.json", "w"))
print(json.dumps(out)[:3000])
