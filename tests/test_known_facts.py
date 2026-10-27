"""Pins facts K3, K7, K11, K12, K17-K24 and K29 of kb/known_results.md (K22 only for single-class
chains with a != b and a + b <= 8). K13 and K30-K60 are backed by the tests, experiment folders,
certificates and referee reviews named in their Check column (K44 only by a check on the records
in the main session; K51 and K52 also by the cell regressions tests/test_l007_cells.py and
tests/test_l008_cells.py; of K52-K55 and K58 only the exact values f(16), f(18), f(20), f(22), f(23)
are pinned here, in test_fn_bounds (K58 also by the witness test tests/test_c23_witness.py, which pins
only the upper bound h(C23) = 14); K59 by tests/test_c003_record.py, which pins only the cheap half of
the community 65-point set (it is a (4,5)-set, it equals the exact rebuild, and the stored 37-point
subset is Sidon; the upper bound h <= 37 and the table entry KNOWN_UPPER[65] = 37 are pinned by no
test); K56, K57 and K60 are pinned by no test), and rows whose Check is "source" are pinned by
no test. Also pins the
safety rails
(judge, hook, status script). Run: python3 -m pytest -q"""
import hashlib
import importlib.util
import itertools
import json
import os
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from e757 import chains as C
from e757 import core
from e757 import fn_bounds as B
from e757 import saturated as S

REPO = Path(__file__).resolve().parent.parent
A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
T12A = [0, 178, 198, 218, 227, 235, 272, 276, 287, 317, 356, 436]
T12B = [-336, -168, -44, -24, -4, 0, 39, 44, 49, 80, 102, 160]


def load_judge():
    spec = importlib.util.spec_from_file_location("frozen_judge", REPO / "judge" / "judge.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def affinely_equal(A, B_):
    A, B_ = sorted(A), sorted(B_)
    if len(A) != len(B_):
        return False
    for AA in (A, sorted(-x for x in A)):
        q = Fraction(B_[-1] - B_[0], AA[-1] - AA[0])
        t = B_[0] - q * AA[0]
        if sorted(q * x + t for x in AA) == [Fraction(b) for b in B_]:
            return True
    return False


# ---------------------------------------------------------------- integrity
def test_judge_hash_pinned():
    h = hashlib.sha256((REPO / "judge" / "judge.py").read_bytes()).hexdigest()
    assert (REPO / "judge" / "judge.sha256").read_text().split()[0] == h


# ---------------------------------------------------------------- K11, K17
def test_abase():
    assert core.is_45_set(A_BASE)
    E = core.ap_edges(A_BASE)
    assert len(E) == 12 == len(A_BASE) - 2
    assert core.alpha(A_BASE, E) == 8
    assert sum(1 for s in itertools.combinations(A_BASE, 8) if core.is_sidon(s)) == 143
    assert not any(core.is_sidon(s) for s in itertools.combinations(A_BASE, 9))
    assert sorted(core.degrees(A_BASE, E).values(), reverse=True) == [4] + [3] * 6 + [2] * 7
    adj = {v: set() for v in A_BASE}
    for e in E:
        for x, y in itertools.combinations(e, 2):
            adj[x].add(y)
            adj[y].add(x)
    for cut in A_BASE:  # no cut vertex in the primal graph
        rest = [v for v in A_BASE if v != cut]
        seen, stack = {rest[0]}, [rest[0]]
        while stack:
            for w in adj[stack.pop()]:
                if w != cut and w not in seen:
                    seen.add(w)
                    stack.append(w)
        assert len(seen) == len(rest)


# ---------------------------------------------------------------- K12, K19
def test_twelve_point_sets():
    for T in (T12A, T12B):
        assert core.is_45_set(T)
        E = core.ap_edges(T)
        assert len(E) == 10
        assert core.alpha(T, E) == 7
    assert not affinely_equal(T12A, T12B)


# ---------------------------------------------------------------- K18
def test_rigidity_and_rebuild():
    for T in (A_BASE, T12A, T12B):
        rep = core.ap_rank_report(T)
        assert rep["solution_dim"] == 2 and rep["m"] == rep["n"] - 2
    idx = {x: i for i, x in enumerate(A_BASE)}
    labeled = [(idx[a], idx[b], idx[c]) for a, b, c in core.ap_edges(A_BASE)]
    ok, vals = core.realize(labeled, 14)
    assert ok and affinely_equal(A_BASE, vals)
    lo, hi, mid = S.map_of_set(A_BASE)
    v = S.solve_midpoint_map(14, lo, hi, mid)
    assert [x * 1056 for x in v] == [Fraction(x) for x in A_BASE]
    assert S.check_values(v, S.edges_of_map(mid)) == (True, "ok")
    assert S.alpha_of_edges(14, S.edges_of_map(mid)) == 8


# ---------------------------------------------------------------- K7, K20
def test_f7_not_realizable():
    F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    reasons = {}
    for lab in itertools.product(range(3), repeat=5):
        edges = []
        for e, k in zip(F7, lab):
            mid = e[k]
            ends = [x for x in e if x != mid]
            edges.append((ends[0], mid, ends[1]))
        ok, r = core.realize(edges, 7, tries=5)
        key = "REALIZED" if ok else r
        reasons[key] = reasons.get(key, 0) + 1
    assert "REALIZED" not in reasons
    assert reasons == {"two points forced equal": 204, "extra AP forced": 24,
                       "(4,5) condition violated": 15}


# ---------------------------------------------------------------- K3, K21
def test_fibonacci_caveat():
    assert not core.is_45_set([1, 2, 3, 5])
    assert core.is_45_set([1, 2, 3, 6]) and not core.is_sidon([1, 2, 3, 6])
    fib = [1, 2]
    while len(fib) < 40:
        fib.append(fib[-1] + fib[-2])
    for n, h in ((10, 7), (20, 13), (30, 19)):
        Bset = fib[1:1 + n]
        assert core.is_45_set(Bset)
        assert core.alpha(Bset) == h


# ---------------------------------------------------------------- K22
def test_chain_densities():
    assert C.chain_density([(2, 1)]) == Fraction(3, 5)
    for a in range(1, 8):
        for b in range(1, 8):
            if a != b and a + b <= 8:
                assert C.chain_density([(a, b)]) >= Fraction(3, 5), (a, b)


# ---------------------------------------------------------------- K23, K24
def test_hy_feasibility():
    excluded = [n for n in range(4, 31) if not B.beat_feasibility(n)[0]]
    assert excluded == list(range(4, 16)) + [17, 19, 21, 24, 26, 28]
    assert B.beat_feasibility(16) == (True, 9, 7, 13)


def test_fn_bounds():
    b = B.fn_bounds(40)
    exact = {n: lu[0] for n, lu in b.items() if lu[0] == lu[1]}
    want = {1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8,
            14: 8, 15: 9, 16: 10, 17: 10, 18: 11, 20: 12, 21: 12, 22: 13, 23: 14, 24: 14, 26: 15, 27: 16, 28: 16}
    assert exact == want
    assert b[16] == (10, 10) and b[18] == (11, 11) and b[20] == (12, 12) and b[21] == (12, 12) and b[22] == (13, 13) and b[23] == (14, 14) and b[27] == (16, 16)  # L008-L011, L014, L016
    for n, (lo, hi) in b.items():
        assert lo <= hi


def test_small_records():
    data = json.loads((REPO / "data" / "small_records.json").read_text())["sets"]
    J = load_judge()
    for key, d in data.items():
        A = d["set"]
        assert core.is_45_set(A), key
        assert core.alpha(A) == d["h"] == B.fn_bounds(20)[len(A)][0], key
    assert data["8"]["h"] == 5 and data["10"]["h"] == 6


def test_ordered_search_small():
    from e757.ordered_search import search
    hits = search(8, 5, max_none=6, limit=1)
    assert hits and hits[0]["h"] == 5 and core.is_45_set(hits[0]["set"])


# ---------------------------------------------------------------- judge behaviour
def _claim(tmp, cid, s, **kw):
    p = tmp / f"{cid}.json"
    p.write_text(json.dumps({"id": cid, "type": "construction", "set": s, **kw}))
    return p


def test_judge_behaviour(tmp_path):
    J = load_judge()
    s = J.judge_struct(REPO / "tests" / "fixtures" / "C000-abase.json")
    assert s["ok"] and s["tag"] == "NO-IMPROVEMENT" and s["h"] == 8
    assert not J.judge_struct(_claim(tmp_path, "x1", [1, 2, 3, 5, 8]))["ok"]
    assert not J.judge_struct(_claim(tmp_path, "x2", A_BASE, claimed_h=7))["ok"]
    p = tmp_path / "x3.json"
    p.write_text(json.dumps({"id": "other", "type": "construction", "set": A_BASE}))
    assert not J.judge_struct(p)["ok"]  # id must equal the file name
    glued = A_BASE + [x * 1009 + 10 ** 7 for x in A_BASE]  # generic scale: still (4,5)
    g = J.judge_struct(_claim(tmp_path, "x4", glued))
    assert g["ok"] and g["h"] == 16 and g["tag"] == "NO-IMPROVEMENT"
    bad = A_BASE + [x * 7 + 10 ** 6 for x in A_BASE]  # a "nice" scale creates a parallelogram
    assert not J.judge_struct(_claim(tmp_path, "x5", bad))["ok"]
    r = J.judge_struct(_claim(tmp_path, "x6", ["0", "1/2", "3/2", "7/2"]))
    assert r["ok"]  # exact rationals are accepted


# ---------------------------------------------------------------- hooks
def _hook(payload):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(REPO))
    r = subprocess.run([sys.executable, str(REPO / ".claude" / "hooks" / "protect.py")],
                       input=json.dumps(payload), capture_output=True, text=True, env=env)
    return r.returncode


def test_protect_hook():
    E = lambda p: {"tool_name": "Edit", "tool_input": {"file_path": p}}  # noqa: E731
    Bsh = lambda c: {"tool_name": "Bash", "tool_input": {"command": c}}  # noqa: E731
    assert _hook(E("judge/judge.py")) == 2
    assert _hook(E(str(REPO / "GOAL.md"))) == 2
    assert _hook(E("scripts/status.py")) == 2
    assert _hook(E("e757/core.py")) == 0
    assert _hook(E("journal/STATE.md")) == 0
    assert _hook(Bsh("python3 judge/judge.py results/claims/a.json > experiments/x/out.txt")) == 0
    assert _hook(Bsh("cat GOAL.md && bash scripts/status.sh")) == 0
    assert _hook(Bsh("cp judge/judge.py /tmp/j.py")) == 0
    assert _hook(Bsh("sed -i 's/4, 7/1, 2/' judge/judge.py")) == 2
    assert _hook(Bsh("echo 'BUDGET_HOURS: 999' > GOAL.md")) == 2
    assert _hook(Bsh("cp /tmp/x.py judge/judge.py")) == 2
    assert _hook(Bsh("rm journal/START_TIME_UTC")) == 2
    assert _hook(Bsh("python3 - <<'EOF'\nopen('scripts/status.py','w').write('x')\nEOF")) == 2
    assert _hook(Bsh("git checkout -- judge/judge.py")) == 2


# ---------------------------------------------------------------- status + new_claim (in a copy)
def test_status_and_new_claim_in_copy(tmp_path):
    dst = tmp_path / "repo"
    shutil.copytree(REPO, dst, ignore=shutil.ignore_patterns(".git", "START_TIME_UTC", ".judge_cache.json",
                                                             "__pycache__", "C[0-9]*-*.json", "out", "logs*", "bin", "chunks*", "nauty_build", "prover_copy", "*.tar.gz"))
    (dst / "tests" / "fixtures").mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, "scripts/new_claim.py", "--slug", "abase",
                        "--set", ",".join(map(str, A_BASE)), "--notes", "test"],
                       cwd=dst, capture_output=True, text=True)
    assert r.returncode == 0 and "PASS NO-IMPROVEMENT" in r.stdout, r.stdout + r.stderr
    out = subprocess.run([sys.executable, "scripts/status.py"], cwd=dst, capture_output=True,
                         text=True).stdout
    assert "judge_integrity: OK" in out
    assert "claims_total: 1 (pass 1, fail 0)" in out
    assert "upper_bound_success: NO" in out and "lower_bound_success: NO" in out
    assert "GOAL_MET: NO" in out
    assert (dst / "journal" / "START_TIME_UTC").exists()
    assert not (REPO / "results" / "claims" / "C001-abase.json").exists()
