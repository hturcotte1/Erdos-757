"""Streaming DFS-only pattern counts (class O, exactly m edges, alpha<=f(n)); no realization, constant memory.
python3 dfscount.py N m [m...]  ->  results/dfs_n<N>_m<m>.json  (labelled, reflection-symmetric, up to reflection)"""
import sys, os, json, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import counts as c
n = int(sys.argv[1])
for m in map(int, sys.argv[2:]):
    t0 = time.time()
    cmd = ["nice", "-n", "10", c.BIN, "n=%d" % n, "T=%d" % c.F[n], "m_min=%d" % m, "m_exact=%d" % m, "f7=1", "progress=0", "mode=enum"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
    lab = sym = 0; st = {}
    for line in p.stdout:
        if line.startswith("SOL"):
            lab += 1
            es = tuple(sorted(tuple(int(x) for x in t.split(",")) for t in line.split()[2:]))
            if c.refl_of(n, es) == es: sym += 1
        elif line.startswith("DONE"):
            st = dict(kv.split("=") for kv in line.split()[1:])
    p.wait()
    assert int(st["timed_out"]) == 0 and int(st["solutions"]) == lab
    assert (lab + sym) % 2 == 0
    d = {"n": n, "m": m, "labelled": lab, "reflection_symmetric": sym, "up_to_reflection": (lab + sym) // 2,
         "nodes": int(st["nodes"]), "t": round(time.time() - t0, 1)}
    print(json.dumps(d), flush=True)
    json.dump(d, open(os.path.join(c.OUT, "dfs_n%d_m%d.json" % (n, m)), "w"))
