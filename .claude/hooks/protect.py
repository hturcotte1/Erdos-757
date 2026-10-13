#!/usr/bin/env python3
"""PreToolUse hook: block edits to the frozen verification infrastructure.

Protected: judge/, GOAL.md, scripts/status.py, scripts/status.sh, .claude/settings.json,
.claude/hooks/, journal/START_TIME_UTC.
Edit/Write/NotebookEdit/MultiEdit on these paths are blocked. Bash commands are blocked when a
write-like command (redirect, sed -i, perl -i, tee, mv, cp into, rm, chmod, truncate, ln, dd,
install, git checkout/restore/rm/mv, or Python open(..., 'w'/'a')) targets one of them.
Reading and running them (cat, python3 judge/judge.py ...) is allowed.
Exit 2 blocks the tool call and shows the message to Claude.
"""
import json
import os
import re
import shlex
import sys

PROTECTED = ["judge/", "GOAL.md", "scripts/status.py", "scripts/status.sh",
             ".claude/settings.json", ".claude/hooks/", "journal/START_TIME_UTC"]
MSG = ("Blocked by .claude/hooks/protect.py: '{}' is frozen verification infrastructure "
       "(see CLAUDE.md, integrity rules). Do not modify it; work elsewhere. If you believe it has a "
       "bug, write the evidence to journal/LOG.md and results/FINAL_REPORT.md for the human.")


def block(what):
    print(MSG.format(what), file=sys.stderr)
    sys.exit(2)


def hit(path_text, root):
    p = path_text.strip().strip("'\"")
    if not p:
        return None
    full = os.path.normpath(p if os.path.isabs(p) else os.path.join(root, p))
    try:
        rel = os.path.relpath(full, root).replace("\\", "/")
    except ValueError:
        return None
    for pat in PROTECTED:
        if pat.endswith("/"):
            if rel == pat[:-1] or rel.startswith(pat):
                return pat
        elif rel == pat:
            return pat
    return None


def check_bash(cmd, root):
    if not any(p.rstrip("/") in cmd for p in PROTECTED):
        return
    prot = "|".join(re.escape(p.rstrip("/")) for p in PROTECTED)
    # redirection into a protected path
    if re.search(r">>?\s*['\"]?[^\s;&|]*(" + prot + r")", cmd):
        block("redirect into protected path")
    # python-style writes
    for line in cmd.splitlines():
        if re.search(prot, line) and re.search(r"open\([^)]*['\"][wax+]", line):
            block("file write in inline code")
        if re.search(prot, line) and re.search(r"write_text|write_bytes|shutil\.(copy|move)|os\.(remove|rename|replace)", line):
            block("file write in inline code")
    # split into simple commands
    for seg in re.split(r"&&|\|\||;|\||\n", cmd):
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            toks = seg.split()
        while toks and (re.match(r"^\w+=", toks[0]) or toks[0] in ("sudo", "env", "command", "nohup", "time")):
            toks = toks[1:]
        if not toks:
            continue
        verb = os.path.basename(toks[0])
        args = toks[1:]
        hits = [a for a in args if hit(a, root)]
        if not hits:
            continue
        if verb in ("sed", "perl") and any(a.startswith("-i") or (a.startswith("-") and "i" in a and verb == "perl") for a in args):
            block(hits[0])
        if verb in ("tee", "mv", "rm", "chmod", "chown", "truncate", "ln", "dd", "install", "unlink", "shred", "touch"):
            block(hits[0])
        if verb == "cp" and hit(args[-1], root):
            block(args[-1])
        if verb == "git" and args and args[0] in ("checkout", "restore", "rm", "mv"):
            block(hits[0])


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    if tool in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
        p = ti.get("file_path") or ti.get("notebook_path") or ""
        h = hit(p, root)
        if h:
            block(h)
    elif tool == "Bash":
        check_bash(ti.get("command", ""), root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
