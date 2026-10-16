"""Resumable case-split decision for n=16, T=9 (F7-free, monotone K30, medial K31, forbidden cores).

Sub-instances: m in {13,14} x vertex-1 case k in {0 (vertex 1 is no midpoint), 2..15 (edge (0,1,k))}.
Each is one CP-SAT enumeration (workers=1): UNSAT (COMPLETE, 0 solutions), SAT (all solutions are
enumerated with blocking clauses, each goes through realize_exact; realizable ones through
scripts/new_claim.py at once) or TIMEOUT.  A TIMEOUT case is split further by the edge of vertex 2
(options (i,2,k) with i in {0,1}, or none).  The reflection lex constraint is DROPPED inside cases
(the case split on vertex 1 is not reflection invariant; dropping it is trivially sound).
Each task writes results/case_m{M}_k{K}[_v2_{tag}].json when finished; a task whose JSON exists is
skipped, so relaunching resumes.  Usage: python3 driver.py [PARALLEL=4] [TIME=3000]
"""
import gzip, json, os, subprocess, sys, time
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RES = os.path.join(HERE, "results")
N, T = 16, 9


def fixings(task):
    """task = (M, K, V2) with V2 None or ('none',) or (i, k2); returns (name, setup function)."""
    M, K, V2 = task
    name = "case_m%d_k%d" % (M, K)
    if V2 is not None:
        name += "_v2_" + ("none" if V2 == "none" else "%d_%d" % V2)

    def setup(mod):
        e = mod.e
        if K == 0:
            mod.model.Add(sum(e[(0, 1, k)] for k in range(2, N)) == 0)
        else:
            mod.model.Add(e[(0, 1, K)] == 1)
        if V2 is not None:
            lits = [e[(i, 2, k)] for i in (0, 1) for k in range(3, N)]
            if V2 == "none":
                mod.model.Add(sum(lits) == 0)
            else:
                mod.model.Add(e[(V2[0], 2, V2[1])] == 1)
    return name, setup


def run_task(task, tl):
    from e757.cpsat_model import enumerate_solutions, load_cores
    from e757.realizability import realize_exact
    M, K, V2 = task
    name, setup = fixings(task)
    out_path = os.path.join(RES, name + ".json")
    if os.path.exists(out_path):
        return name, json.load(open(out_path))["status"]
    cores = load_cores(REPO + "/data/forbidden_ordered_n7.json", REPO + "/data/forbidden_ordered_n8.json")
    found = []
    sol_file = os.path.join(RES, name + "_solutions.jsonl")
    fh = open(sol_file, "w")
    realizable = []

    def cb(edges, a):
        fh.write(json.dumps({"edges": edges, "alpha": a}) + "\n"); fh.flush()
        r = realize_exact(N, [tuple(e) for e in edges])
        if r[0]:
            realizable.append({"edges": edges, "set": r[1]})
            rr = subprocess.run([sys.executable, REPO + "/scripts/new_claim.py", "--slug", "n16-" + name,
                                 "--set", ",".join(map(str, r[1]))], capture_output=True, text=True, cwd=REPO)
            realizable[-1]["new_claim"] = rr.stdout[-1500:]
        else:
            found.append(r[1])

    t0 = time.time()
    count, _, status = enumerate_solutions(N, T, M, callback=cb, limit=200000, time_limit=tl, workers=1,
                                           symmetry=False, setup=setup, monotone=True, medial=True,
                                           cores=cores, core_lit_budget=2_500_000)
    fh.close()
    info = enumerate_solutions.last
    st = {"COMPLETE": ("UNSAT" if count == 0 else "SAT_ENUMERATED")}.get(status, status)
    out = {"n": N, "T": T, "m_exact": M, "k": K, "v2": V2, "status": st, "enum_status": status,
           "n_solutions": count, "n_realizable": len(realizable), "realizable": realizable,
           "failure_reasons": {r: found.count(r) for r in set(found)},
           "constraints": info["constraints"], "wall_s": round(time.time() - t0, 1), "workers": 1,
           "time_limit": tl}
    if count:
        with open(sol_file, "rb") as f, gzip.open(sol_file + ".gz", "wb") as g:
            g.write(f.read())
    os.remove(sol_file)
    tmp = out_path + ".tmp"
    json.dump(out, open(tmp, "w")); os.replace(tmp, out_path)  # atomic: JSON exists only when complete
    return name, st


def main():
    par = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 3000
    os.makedirs(RES, exist_ok=True)
    tasks = [(M, K, None) for M in (13, 14) for K in [0] + list(range(2, N))]
    with ProcessPoolExecutor(par) as ex:
        while tasks:
            res = list(ex.map(run_task, tasks, [tl] * len(tasks)))
            print(time.strftime("%H:%M:%S"), res, flush=True)
            nxt = []
            for task, (name, st) in zip(tasks, res):
                if st == "TIMEOUT" and task[2] is None:  # split by vertex 2
                    M, K, _ = task
                    nxt += [(M, K, "none")] + [(M, K, (i, k)) for i in (0, 1) for k in range(3, N)]
            tasks = nxt
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
