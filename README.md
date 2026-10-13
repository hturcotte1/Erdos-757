# Erdős #757: autonomous research repo

This repo lets a Claude Code session (Fable, max effort) work on Erdős Problem #757 under `/goal`
for days. Its success can only be declared through checks it cannot fake: a frozen judge for
constructions, independent referee subagents for proofs, and a status script that computes the
goal verdict.

**Problem.** Every 4 points of a finite set $A\subset\mathbb R$ determine at least 5 distinct
distances. How large a Sidon subset must $A$ contain? The published bounds are
$9/17\le c_*\le4/7$ (Ma–Tang 2026). Full context is in `kb/00_START_HERE.md`.

## Layout

| Path | What |
|---|---|
| `CLAUDE.md` | The agent's operating rules (auto-loaded every session) |
| `GOAL.md` | `BUDGET_HOURS` and the exact `/goal` condition to paste |
| `kb/` | Knowledge base: START_HERE, research plan, known results, dead ends, open questions, ideas, the two literature reviews, bibliography, papers/ |
| `e757/` | Exact-arithmetic toolkit (AP hypergraphs, realizability, midpoint maps, f(n) bounds, chains) |
| `judge/` | Frozen independent verifier, with its SHA-256 pinned |
| `scripts/` | `status.sh` (goal verdict), `preflight.sh`, `new_claim.py`, `start_job.sh`, `jobs.sh` |
| `.claude/` | Hooks (protect frozen files, re-inject state after compaction), subagents (referee, scout, falsifier), skills (verify-claim, checkpoint), permissions |
| `journal/` | STATE (current), LOG (append-only), START_TIME_UTC (the clock) |
| `results/` | claims/, proofs/, reviews/, LEDGER.md, FINAL_REPORT.md |
| `tests/` | Pins every verified fact and the safety rails (`python3 -m pytest -q`) |

## Quick start (Claude Code on the web)

1. Open claude.ai/code, start a session on `hturcotte1/Erdos-757`, and choose Fable at max effort.
2. Give the environment network access so it can install packages and read papers.
3. Type `/goal `, paste the box from `GOAL.md`, and send. The first turns run preflight and start Phase 1.
4. Watch progress in the commit history, `journal/STATE.md` and `results/LEDGER.md`.

The terminal instructions below are for running it locally instead.

## Setup (once, about 15 minutes)

1. Unzip, then `cd erdos757`.
2. Create a **private** GitHub repo and push:
   `gh repo create erdos757 --private --source=. --push`. Or create it on github.com, then run
   `git remote add origin <url> && git push -u origin main`.
3. Add the papers listed in `kb/literature/papers/README.md`, then commit and push. The most
   valuable one is Henning–Yeo 2021, which contains the 9/17 inequality.
4. Optional: `python3 -m venv .venv && source .venv/bin/activate`.
5. Run `bash scripts/preflight.sh` and check that it ends with `PREFLIGHT OK`.
6. Update Claude Code (`claude update`), signed in on a plan with Fable access.

## Dry run (30 minutes; do this first)

```bash
git checkout -b dry-run
sed -i.bak 's/^BUDGET_HOURS: .*/BUDGET_HOURS: 0.5/' GOAL.md && rm GOAL.md.bak
git commit -am "dry run: 0.5h budget"
claude --model fable --effort max --permission-mode auto
```

Type `/goal `, paste the box from `GOAL.md`, and watch. Check that it:
- runs preflight and reads kb/;
- starts Phase 1 and commits/pushes;
- ends turns with `bash scripts/status.sh`;
- is not stuck on permission prompts (see `/permissions` → Recently denied).

Afterwards: `git checkout main && git branch -D dry-run && git push origin --delete dry-run`.

## Real run

```bash
tmux new -s e757                  # keeps the session alive if the terminal closes
cd erdos757 && source .venv/bin/activate   # if you made a venv
caffeinate -dims &                # macOS: keep the machine awake
                                  # Linux: systemd-inhibit --what=idle:sleep sleep infinity &
claude --model fable --effort max --permission-mode auto
```

Then type `/goal `, paste the box from `GOAL.md`, and press Enter. Detach with `Ctrl-b d` and
reattach later with `tmux attach -t e757`.

- **Use interactive mode, not `claude -p`.** The interactive session waits for usage limits to
  reset and then continues on its own, and it checks in on long background jobs.
- **Claude Code on the web also works.** Open this repo in a cloud session, pick Fable, and type
  the same `/goal`. Its environment needs network access for package installs and web research.

## Monitoring

- **From anywhere:** the GitHub commit history, `journal/STATE.md`, `journal/LOG.md` and
  `results/LEDGER.md`. CI re-runs the tests and the judge on every push (Actions tab).
- **In the session:** `/goal` shows the turns, time, tokens and the evaluator's latest reason.
  `bash scripts/status.sh` and `bash scripts/jobs.sh` also work.

## Stopping, resuming, budget

- `/goal clear` stops the loop; `Esc` interrupts a turn.
- `claude --continue` resumes the session, and the goal is restored.
- `BUDGET_HOURS` in GOAL.md is the hard stop (default 72). Lower it to spend less.
- Elapsed time counts from `journal/START_TIME_UTC`; delete that file to restart the clock.
- Fable at max effort for days uses a lot of plan usage. When a limit is hit, the session waits
  and continues automatically.

## What counts as success

`scripts/status.sh` prints `GOAL_MET: YES` only if the judge is unmodified, git is clean and
pushed, and one of these holds:
- **(A) New upper bound:** a (4,5)-set with ratio below 4/7, passed by `judge/judge.py` and
  accepted by a referee subagent.
- **(B) New lower bound:** a proof of $c_*\ge r>9/17$ with two independent referee ACCEPTs and a
  scout `NOVELTY: CLEAR`.
- **(C) Budget reached:** the time budget is used up and `results/FINAL_REPORT.md` is written.

Partial results (exact values of $f(n)$, refuted lemmas, censuses) go in the ledger along the way.
Before announcing anything, check it yourself: re-run `python3 judge/judge.py` on the claim, read
the referee reviews in `results/reviews/`, and ideally get a human expert to look.

## If something goes wrong

| Problem | What to do |
|---|---|
| Session idles or stops with the goal still set | Send `continue` (or any message) |
| Goal cleared after an unrecoverable error | Fix the cause (credits, login), `claude --continue`, paste `/goal ...` again |
| Repeated auto-mode denials | `/permissions` → Recently denied; allow the action or add a rule |
| You suspect a judge bug | Only you may edit `judge/`. Fix it, then re-pin the hash: `python3 -c "import hashlib;print(hashlib.sha256(open('judge/judge.py','rb').read()).hexdigest()+'  judge/judge.py')" > judge/judge.sha256` |
