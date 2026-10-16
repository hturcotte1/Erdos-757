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
| `.claude/` | Hooks (protect frozen files, re-inject state after compaction), subagents (worker, summarizer, prover, referee, scout, falsifier), skills (verify-claim, e757-checkpoint), permissions |
| `journal/` | STATE (current), LOG (append-only), START_TIME_UTC (the clock) |
| `results/` | claims/, proofs/, reviews/, LEDGER.md, FINAL_REPORT.md |
| `data/` | Census and record data (the 2,910 saturated 14-point classes, small records, forbidden-core libraries); index in `data/README.md` |
| `experiments/` | One folder per experiment, each with a README; index in `experiments/README.md`, sub-indexes for `falsify/` and `referee/` |
| `tests/` | Pins every verified fact and the safety rails (`python3 -m pytest -q`) |

## Results of the autonomous run (2026-10-13/16)

Published bounds are unchanged: $9/17\le c_*\le4/7$. No set below 4/7 and no lower-bound proof were found
(goal clauses A and B not met). Everything below is tagged in `kb/known_results.md` (rows K30-K47).
- **Start with** `results/FINAL_REPORT.md` (definitive narrative) and `results/LEDGER.md` (verified results with evidence paths).
- **Certificates (referee ACCEPT):** `results/proofs/L001`-`L005`, with the reviews in `results/reviews/`:
  L001 no 2-point extension of A_base has $h\le9$; L002 exactly 54,243 twelve-point extremal sets;
  L003 saturated extremal counts 1, 4, 66, 1262, 6644, 466961 for $n=6..11$; L004 exactly 2,910 saturated 14-point extremal sets;
  L005 (K46) no 16-point (4,5)-set with $h\le9$ contains a saturated extremal 14-point set (the L001 case analysis applied to all 2,910 classes: all 141,153 single (4,5) extensions, 4,970,208 enumerated (4,5) T1b pairs and 122,220 line hypergraphs give $h=10$; two referee ACCEPTs after one text-only NEEDS-WORK round; scout CLEAR).
- **Exact values:** $f(n)=\lceil n/2\rceil+1$ for $6\le n\le15$ and $n=17$ (K35). The first open case is $f(16)\in\{9,10\}$ (Q1 in `kb/open_questions.md`).
- **Census data:** `data/census_n14_m12_classes.jsonl.gz` (2,910 sets), `data/census_n14_m12_summary.json`,
  `experiments/20261014-1005-census-dfs/results/realized_n12.json.gz` (54,243 sets); index in `data/README.md`.
  Forbidden-configuration library: `data/forbidden_ordered_n7.json`, `data/forbidden_ordered_n8.json` (287 minimal cores).
  L005 sweep data: `experiments/20261015-2340-ext14-all/results.json` (one row per class of the 2,910); K47 structure census: `experiments/20261016-0150-structure-2910/results.json`.
- **Lemmas:** monotone midpoints (K30), no medial triangle (K31), degree bound in Gyarfas-Lehel-tight hypergraphs (K44). K47 [verified-here]: in the 2,910 saturated extremal 14-point classes the AP degrees are 2, 3 or 4, there are 137 to 150 maximum Sidon subsets per class, no class contains a 12-point subset with $h=7$, and no vertex lies in every maximum Sidon subset (`tests/test_structure_2910.py`). Extension lemmas in `kb/notes/extension_lemmas.md` [derived-here; falsifier found no counterexample on about 11,000 sets and fixed two gaps in the Lemma Delta consequence paragraph, `experiments/falsify/extension-lemmas`]: Lemma E (one-edge extension raises $h$ by 1, instead of 2, exactly when the vertex lies in every maximum Sidon subset), Lemma U (Henning-Yeo obstruction to such vertices; none occurs in the 2,910 classes), Lemma Delta (in a 16-point record every 15-point subset is extremal and $\deg p\le m-9$).
- **Negative results:** `kb/dead_ends.md` D15-D22 (n=16 undecided by SAT/CP-SAT/annealing; Q8 false in the abstract class; exact saturated census at n=13 infeasible with the L002/L004 pipeline, D22 / Q12).
- **Still running at the last update (2026-10-16, about 02:55 UTC):** exhaustive DFS for the non-saturated $(14,11)$ case (`experiments/20261014-1005-census-dfs/n14m11dfs`; 4 workers, resumable by prefix). 169 of its 3,437 depth-3 prefixes were finished, every one with 0 patterns. At the measured 30 to 36 prefixes per hour it needs roughly 90 to 110 more hours, but the budget ends at 2026-10-16 23:06 UTC (about 20 h later), so it will not finish, Q11 stays open, and no claim rests on this partial coverage [heuristic: rate projection]. The saturated $n=13$ census was started and stopped as infeasible (D22, Q12 in `kb/`).
- **Reproduce:** every experiment folder has a `README.md` with the exact command; tests: `python3 -m pytest -q`.
- **Audit of this documentation:** `experiments/20261015-2310-kb-audit/README.md`.

## Quick start (Claude Code on the web)

1. Open claude.ai/code, start a session on `hturcotte1/Erdos-757`, and choose Fable at max effort.
2. Give the environment network access so it can install packages and read papers.
3. Type `/goal `, paste the box from `GOAL.md`, and send. The first turns run preflight and start Phase 1.
4. Watch progress in the commit history, `journal/STATE.md` and `results/LEDGER.md`.

### How usage is conserved
Fable is the orchestrator: it plans, does the key mathematical reasoning, and judges results.
Execution is delegated:

| Work | Subagent | Model |
|---|---|---|
| Code, experiments | `worker` | Sonnet |
| Reading logs and files | `summarizer` | Haiku |
| Literature | `scout` | Sonnet |
| Counterexample hunting | `falsifier` | Sonnet |
| Writing out proofs | `prover` | Opus |
| Verification | `referee` | Opus, or Fable for the final check |

Searches run as CPU jobs, which cost no tokens. The rules are in the "orchestrator" section of
CLAUDE.md.

If usage is still too high, pick a lower effort for Fable in the session (high instead of max)
or lower `BUDGET_HOURS` in `GOAL.md`.

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
