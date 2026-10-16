"""Summarise results/case_*.json into a table (printed and appended to README.md between markers)."""
import glob, json, os
here = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(here + "/results/case_*.json")):
    r = json.load(open(f))
    rows.append((r["m_exact"], r["k"], r["v2"], r["status"], r["n_solutions"], r["n_realizable"], r["wall_s"]))
rows.sort(key=lambda x: (x[0], x[1], str(x[2])))
tot = 30
lines = ["| m | k (edge (0,1,k); 0 = none) | vertex-2 split | status | #solutions | #realizable | wall s |", "|---|---|---|---|---|---|---|"]
lines += ["| %d | %d | %s | %s | %d | %d | %.0f |" % (m, k, v2 or "-", st, ns, nr, w) for m, k, v2, st, ns, nr, w in rows]
done_top = sum(1 for r in rows if r[2] is None)
summary = "Top-level cases finished: %d / %d.  UNSAT: %d, SAT: %d, TIMEOUT (split further): %d.  Realizable sets found: %d." % (
    done_top, tot, sum(r[3] == "UNSAT" for r in rows), sum(r[3].startswith("SAT") for r in rows),
    sum(r[3] == "TIMEOUT" for r in rows), sum(r[5] for r in rows))
text = summary + "\n\n" + "\n".join(lines) + "\n"
print(text)
p = os.path.join(here, "README.md")
s = open(p).read() if os.path.exists(p) else ""
a, b = "<!-- RESULTS START -->", "<!-- RESULTS END -->"
if a in s:
    s = s[:s.index(a)] + a + "\n" + text + b + s[s.index(b) + len(b):]
else:
    s += "\n" + a + "\n" + text + b + "\n"
open(p, "w").write(s)
