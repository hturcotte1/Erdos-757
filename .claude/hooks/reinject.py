#!/usr/bin/env python3
"""SessionStart hook (matcher: compact). Stdout is added to Claude's context after compaction."""
import os
from pathlib import Path

root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
print("=== RE-INJECTED AFTER COMPACTION (from .claude/hooks/reinject.py) ===")
print("Rules recap: every turn does real work with tool calls and ends with `bash scripts/status.sh`; "
      "never edit judge/, GOAL.md or scripts/status.*; constructions count only via judge/judge.py; "
      "proofs need 2 referee ACCEPTs + scout NOVELTY: CLEAR (verify-claim skill); checkpoint every 2-3 h; "
      "grep kb/dead_ends.md before starting a direction.")
state = root / "journal" / "STATE.md"
if state.exists():
    print("\n--- journal/STATE.md ---")
    print(state.read_text(errors="replace")[:6000])
log = root / "journal" / "LOG.md"
if log.exists():
    lines = log.read_text(errors="replace").splitlines()
    print("\n--- last lines of journal/LOG.md ---")
    print("\n".join(lines[-40:]))
print("=== END RE-INJECTED CONTEXT ===")
