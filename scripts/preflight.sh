#!/usr/bin/env bash
# One-time environment check. Run it yourself before launching, and the agent runs it in Phase 0.
set -uo pipefail
cd "$(dirname "$0")/.."
fail() { echo "PREFLIGHT FAILED: $*"; exit 1; }

python3 -c 'import sys; assert sys.version_info >= (3, 9), sys.version' || fail "need Python >= 3.9"
echo "python: $(python3 --version)"

pip_install() {
  python3 -m pip install -q "$@" 2>/dev/null || python3 -m pip install -q --user "$@" 2>/dev/null \
    || python3 -m pip install -q --break-system-packages "$@"
}
pip_install -r requirements.txt || fail "could not install requirements.txt"
pip_install -r requirements-optional.txt >/dev/null 2>&1 \
  && echo "optional packages: installed" || echo "optional packages: some failed (fine; install later if needed)"

python3 - <<'PY' || exit 1
import hashlib, pathlib, sys
h = hashlib.sha256(pathlib.Path("judge/judge.py").read_bytes()).hexdigest()
pinned = pathlib.Path("judge/judge.sha256").read_text().split()[0]
if h != pinned:
    print("PREFLIGHT FAILED: judge/judge.py does not match judge/judge.sha256"); sys.exit(1)
print("judge hash: OK")
PY

python3 judge/judge.py tests/fixtures/C000-abase.json | grep -q "PASS NO-IMPROVEMENT" \
  || fail "judge did not reproduce A_base"
echo "judge on A_base: OK"

TO=(); command -v timeout >/dev/null && TO=(timeout 900)
"${TO[@]}" python3 -m pytest -q 2>&1 | tail -3
[ "${PIPESTATUS[0]}" -eq 0 ] || fail "tests failed"

chmod +x .claude/hooks/*.py scripts/*.sh 2>/dev/null
echo '{"tool_name":"Edit","tool_input":{"file_path":"judge/judge.py"}}' \
  | CLAUDE_PROJECT_DIR="$PWD" python3 .claude/hooks/protect.py 2>/dev/null
[ $? -eq 2 ] || fail "protect hook did not block an edit of judge/judge.py"
echo "protect hook: OK"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [ -z "$(git remote)" ]; then echo "WARNING: no git remote (push to a private GitHub repo so progress is visible)"; fi
else
  echo "WARNING: not a git repository (run: git init && git add -A && git commit -m init)"
fi
echo "PREFLIGHT OK"
