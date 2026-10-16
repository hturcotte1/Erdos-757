"""Referee L002: run the frozen verifier (read-only use) on the scratch spot-check claim files and store its output here."""
import glob, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.abspath(os.path.join(here, "..", "..", ".."))
files = sorted(glob.glob(os.path.join(here, "spot_claims", "*.json")))
res = subprocess.run([sys.executable, os.path.join(repo, "judge", "judge.py")] + files, capture_output=True, text=True, cwd=repo)
with open(os.path.join(here, "spot_check_output.txt"), "w") as f:
    f.write(res.stdout + res.stderr + "exit=%d\n" % res.returncode)
lines = [l for l in res.stdout.splitlines() if l.startswith("JUDGE:")]
print("claims", len(files), "verdict lines", len(lines), "PASS NO-IMPROVEMENT h=7:",
      sum(1 for l in lines if "PASS NO-IMPROVEMENT" in l and " h=7 " in l), "exit", res.returncode)
