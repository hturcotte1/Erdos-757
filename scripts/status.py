#!/usr/bin/env python3
"""
GOAL-STATUS block for the /goal evaluator. PROTECTED FILE: do not edit.

The /goal condition in GOAL.md refers only to the block this script prints. It computes everything
itself from files on disk:
  * judge_integrity: SHA-256 of judge/judge.py equals judge/judge.sha256
  * clock: journal/START_TIME_UTC (created on the first run) and BUDGET_HOURS from GOAL.md
  * clause A (upper bound): a claim in results/claims/ judged live as `PASS NEW-RECORD`, whose most
    recent referee review (results/reviews/<id>__referee__<UTC>.md) starts with `VERDICT: ACCEPT`
  * clause B (lower bound): a proof results/proofs/<id>.md with a line `CLAIM: c* >= r`, r > 9/17,
    whose two most recent referee reviews both start with `VERDICT: ACCEPT` and whose most recent
    scout review starts with `NOVELTY: CLEAR`
  * clause C (budget): elapsed >= BUDGET_HOURS and results/FINAL_REPORT.md exists (>= 500 bytes)
  * GOAL_MET: YES iff (A or B or C) and judge integrity OK and git is clean and pushed
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NINE_17 = Fraction(9, 17)
CACHE = REPO / "results" / ".judge_cache.json"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def utcnow():
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def start_time():
    f = REPO / "journal" / "START_TIME_UTC"
    if not f.exists() or not f.read_text().strip():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(iso(utcnow()) + "\n")
    return datetime.fromisoformat(f.read_text().strip().replace("Z", "+00:00"))


def budget_hours():
    try:
        m = re.search(r"^BUDGET_HOURS:\s*([0-9]+(?:\.[0-9]+)?)", (REPO / "GOAL.md").read_text(), re.M)
        return float(m.group(1)) if m else None
    except OSError:
        return None


def first_line(path):
    for line in Path(path).read_text(errors="replace").splitlines():
        if line.strip():
            return line.strip()
    return ""


def reviews(item_id, kind):
    # file names end in a UTC timestamp, so lexicographic order is chronological
    return sorted((REPO / "results" / "reviews").glob(f"{item_id}__{kind}__*.md"))


def load_judge():
    spec = importlib.util.spec_from_file_location("frozen_judge", REPO / "judge" / "judge.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(*args):
    try:
        r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, timeout=60)
        return r.returncode, r.stdout.strip()
    except Exception as e:  # noqa: BLE001
        return 1, str(e)


def judge_claims(jmod, jhash):
    try:
        cache = json.loads(CACHE.read_text())
    except (OSError, ValueError):
        cache = {}
    results = []
    for p in sorted((REPO / "results" / "claims").glob("*.json")):
        key = sha256(p) + ":" + jhash
        c = cache.get(key)
        if c is None or c.get("tag") == "NEW-RECORD":  # records are always re-judged live
            s = jmod.judge_struct(p)
            c = {"ok": s["ok"], "tag": s["tag"], "id": s["id"], "n": s["n"], "h": s["h"],
                 "ratio": str(s["ratio"]) if s["ratio"] is not None else None}
            cache[key] = c
        results.append(c)
    try:
        CACHE.write_text(json.dumps(cache))
    except OSError:
        pass
    return results


def running_jobs():
    jobs = []
    for pidf in sorted((REPO / "experiments").glob("**/job.pid")):
        try:
            pid = int(pidf.read_text().strip())
            os.kill(pid, 0)
        except (ValueError, OSError):
            continue
        log = pidf.parent / "run.log"
        last = ""
        if log.exists():
            lines = [ln for ln in log.read_text(errors="replace").splitlines() if ln.strip()]
            last = lines[-1][:100] if lines else ""
        jobs.append(f"{pidf.parent.relative_to(REPO)} pid={pid} last: {last}")
    return jobs


def main():
    now = utcnow()
    print("=== GOAL-STATUS (bash scripts/status.sh) ===")
    print(f"time_utc: {iso(now)}")

    # integrity
    jfile, hfile = REPO / "judge" / "judge.py", REPO / "judge" / "judge.sha256"
    jhash = sha256(jfile)
    if not hfile.exists():
        integrity = "MISSING-HASH"
    else:
        integrity = "OK" if hfile.read_text().split()[0] == jhash else "MODIFIED"
    print(f"judge_integrity: {integrity}")

    # clock
    st = start_time()
    elapsed = (now - st).total_seconds() / 3600
    bh = budget_hours()
    exhausted = bh is not None and elapsed >= bh
    print(f"start_utc: {iso(st)}")
    print(f"elapsed_hours: {elapsed:.2f}")
    print(f"budget_hours: {bh if bh is not None else 'unset'}")
    print(f"budget_exhausted: {'YES' if exhausted else 'NO'}")

    # clause A
    claims = judge_claims(load_judge(), jhash) if integrity == "OK" else []
    passed = [c for c in claims if c["ok"]]
    failed = [c for c in claims if not c["ok"]]
    print(f"claims_total: {len(claims)} (pass {len(passed)}, fail {len(failed)})")
    if passed:
        best = min(passed, key=lambda c: Fraction(c["ratio"]))
        print(f"best_judged_ratio: {best['ratio']} ({float(Fraction(best['ratio'])):.6f}) [{best['id']}]")
    records = [c for c in passed if c["tag"] == "NEW-RECORD"]
    a_ok = False
    rec_desc = []
    for c in records:
        revs = reviews(c["id"], "referee")
        verdict = first_line(revs[-1]) if revs else "no referee review yet"
        if verdict == "VERDICT: ACCEPT":
            a_ok = True
        rec_desc.append(f"{c['id']} ratio={c['ratio']} n={c['n']} latest_referee='{verdict}'")
    print(f"new_record_claims: {'; '.join(rec_desc) if rec_desc else 'none'}")
    print(f"upper_bound_success: {'YES' if a_ok else 'NO'}")

    # clause B
    b_ok = False
    proof_desc = []
    for p in sorted((REPO / "results" / "proofs").glob("*.md")):
        if p.name.upper() == "README.MD":
            continue
        m = re.search(r"^CLAIM:\s*c\*?\s*(?:>=|≥)\s*([0-9]+/[0-9]+|[0-9]*\.[0-9]+|[0-9]+)\s*$",
                      p.read_text(errors="replace"), re.M)
        if not m:
            continue
        r = Fraction(m.group(1))
        refs = reviews(p.stem, "referee")
        last_two = [first_line(x) for x in refs[-2:]]
        two_accept = len(last_two) == 2 and all(v == "VERDICT: ACCEPT" for v in last_two)
        scouts = reviews(p.stem, "scout")
        novelty = first_line(scouts[-1]) if scouts else "no scout review yet"
        ok = r > NINE_17 and two_accept and novelty == "NOVELTY: CLEAR"
        b_ok |= ok
        proof_desc.append(f"{p.stem} claims c*>={r} (beats 9/17: {'yes' if r > NINE_17 else 'no'}); "
                          f"last referee verdicts={last_two or 'none'}; scout='{novelty}'")
    print(f"lower_bound_proofs: {'; '.join(proof_desc) if proof_desc else 'none'}")
    print(f"lower_bound_success: {'YES' if b_ok else 'NO'}")

    # clause C
    fr = REPO / "results" / "FINAL_REPORT.md"
    final = fr.exists() and fr.stat().st_size >= 500
    print(f"final_report: {'present' if final else 'absent'}")

    # git
    code, out = git("status", "--porcelain")
    uncommitted = len([ln for ln in out.splitlines() if ln.strip()]) if code == 0 else None
    print(f"git_uncommitted: {uncommitted if uncommitted is not None else 'unknown (not a git repo?)'}")
    code, remotes = git("remote")
    if code == 0 and not remotes.strip():
        unpushed = 0
        print("git_unpushed: 0 (no remote configured)")
    else:
        code, out = git("rev-list", "--count", "@{u}..HEAD")
        unpushed = int(out) if code == 0 and out.isdigit() else None
        print(f"git_unpushed: {unpushed if unpushed is not None else 'no-upstream (run: git push -u origin HEAD)'}")
    git_clean = uncommitted == 0 and unpushed == 0

    jobs = running_jobs()
    print(f"running_jobs: {len(jobs)}" + ("".join(f"\n  - {j}" for j in jobs[:6])))

    log = REPO / "journal" / "LOG.md"
    if log.exists():
        heads = [ln for ln in log.read_text(errors="replace").splitlines() if ln.startswith("## ")]
        print(f"last_log_entry: {heads[-1][3:][:120] if heads else 'none'}")

    clauses = [name for name, ok in (("A", a_ok), ("B", b_ok), ("C", exhausted and final)) if ok]
    met = bool(clauses) and integrity == "OK" and git_clean
    print(f"clauses_satisfied: {','.join(clauses) if clauses else 'none'}; integrity_ok: "
          f"{'YES' if integrity == 'OK' else 'NO'}; git_clean_and_pushed: {'YES' if git_clean else 'NO'}")
    print(f"GOAL_MET: {'YES' if met else 'NO'}")
    print("=== END GOAL-STATUS ===")


if __name__ == "__main__":
    main()
