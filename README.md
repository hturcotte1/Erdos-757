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
| `tests/` | Regression tests for `e757/`, for the small exact facts of `tests/test_known_facts.py` (A_base, the 12-point sets, F7, Fibonacci, f(n) bounds), for the reproducible parts of the certificates L001-L008 (`tests/test_l007_cells.py` and `tests/test_l008_cells.py` compile the C cell enumerators with gcc and run only the cheap cells, not the slow ones such as the degree-3 (14,11,6) run of L007 or the (15,10,6) cell of L008; for L009-L011 and L014 the tests pin only the fn_bounds entries f(18), f(20), f(22), f(23) and, for L014, the upper-bound witness C23 (tests/test_c23_witness.py: a (4,5)-set with 18 APs and h = 14), not the cell computations; tests/test_c003_record.py pins the (4,5)-set property, the 63 APs and the stored 37-point Sidon witness (so h >= 37) of the 65-point set C003 (K59; an anonymous reader's community construction from Erdős Problem a Day, 19 Oct 2026, verified here, not discovered here), but not the upper bound h <= 37, which rests on the judge and the referees)
 and of K47/K49 (the Check column of `kb/known_results.md` names the test, experiment or published source behind each fact; many facts, e.g. most census totals, rest on experiment folders rather than tests), plus the safety rails (`python3 -m pytest -q`; needs `requirements.txt` and `requirements-optional.txt` (python-sat, ortools); the tests that compile or use C code need gcc (most skip without it; `tests/test_census_counts.py::test_census_counts_agree` and `::test_prefix_split_small` fail without it); a few slow cases run only with `E757_SLOW=1`) |

## Results of the autonomous run (2026-10-13/16) and the 48-hour extension (2026-10-17/18)

Published bounds: $9/17\le c_*\le4/7$. This project found no lower-bound proof (goal clause B not met), and the upper-bound improvement below is not its discovery. **Update 2026-10-20:** a COMMUNITY construction (an anonymous reader's self-similar family, posted on Erdős Problem a Day on 19 Oct 2026; its submitter declares that AI tools found it; the site marks it 'unreviewed by humans'; NOT this project's discovery) was rebuilt, judged and refereed here: its 65-point member has $h=37<4\cdot65/7$ (C003, K59, `JUDGE: PASS NEW-RECORD`, two referee ACCEPTs), so $c_*\le37/65$, and the whole family gives $c_*\le5/9$ by an independent, referee-accepted proof (certificate L015, K60); the lower bound $9/17$ is untouched. `status.sh` therefore reports clause (A) through C003, which this project verified but did not find. Everything below is tagged in `kb/known_results.md` (rows K30-K60).
The extension (K50-K55; certificates L007-L011 for K51-K55; narrative in `results/FINAL_REPORT.md` section 7) closed Q11 (no non-saturated extremal 14-point set, K51) and established $f(16)=10$, $f(18)=11$, $f(20)=12$ and $f(22)=13$ (K52-K55) [verified-here, computer-assisted, three referee ACCEPTs each], so no (4,5)-set with at most 22 points beats $4/7$. K50 [verified-here]: non-saturated extremal 15-point sets exist. The inequality $11\tau\le3n+2m$ behind these results is a [conjecture] in general (`kb/notes/i11_conjecture.md`).
- **Headline results of the 48-hour extension (2026-10-17) [verified-here; computer-assisted certificates, each ACCEPTED by three referees, scout `NOVELTY: CLEAR`]:** $f(16)=10$ (L008, K52; Q1 closed), $f(18)=11$ (L009, K53), $f(20)=12$ (L010, K54) and $f(22)=13$ (L011, K55); together with L007 (K51: every 14-point (4,5)-set with $h=8$ has exactly 12 APs, so, given the L004 census (K45; its completeness was re-checked independently only by sampling plus consistency checks), the 2,910 classes of L004 are all the extremal 14-point sets; Q11 closed) they show that **no (4,5)-set with at most 22 points beats $4/7$**, and, with L012 and L014 (K56 and K58: $f(23)=14$, so no (4,5)-set with at most 24 points beats $4/7$), a set beating $4/7$ would need at least 25 points. The tool is the inequality I11, $11\tau\le3n+2m$ (`kb/notes/i11_conjecture.md`): [conjecture] in general (a proof for all $n$ would give $c_*\ge6/11$), proved here (refereed, computer-assisted) only on the abstract class $C$ of linear $F_7$-free 3-graphs with $e(S)\le|S|-2$ and only for $n\le26$ (L007–L011 for $n\le22$ and L013 for $n\le26$, K51–K55 and K57, each ACCEPTED by three referees), by a window-cell induction. The step to $n=27$ depended on the case that L014 has since settled (Q14, now closed; Remark 5 of L013) and is not claimed here: the unrefereed computation and certificate for it are in progress (`experiments/20261017-2150-i11-n27`). The project's own constructions and lower-bound work leave the published bounds $9/17\le c_*\le4/7$ unchanged. The only (4,5)-sets beating $4/7$ that are known to this project come from the self-similar family of an anonymous reader (Erdős Problem a Day, 19 Oct 2026; a [community] construction, verified here, not discovered here): its first member below $4/7$ has 65 points and $h=37$ (C003, K59; rebuilt exactly, judged PASS NEW-RECORD and ACCEPTED by two referees here), and the whole family gives $c_*\le5/9$ (L015, K60; [verified-here] independent proof, ACCEPTED by three referees). The lower bound $9/17$ is untouched. Where to look: data and falsifier runs `experiments/falsify/i11-inequality` and `experiments/20261017-0300-n16-via-i11` to `experiments/20261017-0825-n21-n22-via-i11`; certificates `results/proofs/L007`-`L012` with reviews in `results/reviews/`; reproduction scripts `experiments/prover/L007`-`L012` (`reproduce.sh`); referee re-derivations `experiments/referee/L007-round1` to `L012-round3`. Certificate L012 (K56, [verified-here], computer-assisted, ACCEPTED by three referees, scout CLEAR; evidence `experiments/20261017-1030-n23-record-cell`): a 23-point (4,5)-set with $h=13$ (the first record cell I11 allows, $(23,21,10)$) would have every AP-degree $\le3$ (the degree-4 case leaves 699 abstract classes in $C$, none exactly realizable); the degree-3 case was closed on 2026-10-20 by certificate L014 (K58, [verified-here], computer-assisted, ACCEPTED by three referees; scout PARTIAL: the lower bound is new, while the upper bound $f(23)\le14$ was already known, by gluing and from the omega #9804 23-point set, and the explicit witness $C_{23}$ with $h=14$ is checked here): no 23-point (4,5)-set has $h=13$, so $f(23)=14$, no (4,5)-set with at most 24 points beats $4/7$, and Q14 is closed (`kb/open_questions.md`, `results/LEDGER.md` row K58). The bullets below describe the state of 2026-10-16 and are superseded by this bullet, by `results/LEDGER.md` and by `kb/00_START_HERE.md` where they conflict (the open status of $f(16)$, Q1, Q11, Q14 and $f(23)$).
- **Headline results of the 2026-10-20 resumption.** (1) [verified-here, computer-assisted; certificate L014, K58, ACCEPTED by three referees; scout PARTIAL: no prior statement of the lower bound was found, the witness was already known by gluing] f(23) = 14: no 23-point (4,5)-set has h = 13, hence no (4,5)-set with at most 24 points beats 4/7 and n = 25 is the first size at which a record is not excluded (`results/proofs/L014-f23-equals-14.md`, `tests/test_c23_witness.py`, `experiments/prover/L014`, `experiments/20261017-1925-q14-decide`; Q14 closed). (2) [community construction, NOT this project's discovery; verified here] An anonymous reader posted a self-similar family on Erdős Problem a Day (submission 7bkzb8 of 17 Oct 2026, write-up of 19 Oct 2026, https://erdosproblemaday.com/day/757-reader-five-ninths-refereed; the site marks it 'unreviewed by humans' and the submitter declares that AI tools found and refereed the bound): with O = {0,49,75,83,98,101,117,119,121,159,269} and phi(x) = 101 + 18x/269, S_K = O u phi(O) u ... u phi^K(O) has 11 + 9K points and largest Sidon subset 7 + 5K, so c* <= 5/9. This project's contribution is verification only: an exact rebuild (`experiments/20261020-1730-reader-5-9`, `data/reader_5_9_family.json`); the frozen judge's verdict `JUDGE: PASS NEW-RECORD` on the 65-point member S_6 (h = 37, 37/65 < 4/7) as claim C003 (`results/claims/C003-reader-5-9-K6.json`, two referee ACCEPTs, scout NOVELTY: KNOWN; K59; `tests/test_c003_record.py`); and certificate L015 (K60; three referees; falsifier HOLDS-ON-DATA, scout PARTIAL), an independent proof that S_K is a (4,5)-set with h(S_K) = 7 + 5K for every K (`results/proofs/L015-reader-family-c-le-5-9.md`, `experiments/prover/L015`, `experiments/falsify/l015-reader-family`). The construction and the claim are the reader's; nothing is claimed about the lower bound 9/17 or about whether 5/9 is the true value of c*, and this project's own constructions and proofs improved neither published bound. `bash scripts/status.sh` re-judges C003 (about 35 to 60 minutes) and reports clause A because of it. Where this bullet conflicts with the paragraph above (no set below 4/7, clause A not met), this bullet governs for the community construction. (3) [in progress, unrefereed] the I11 induction at n = 27 (`experiments/20261017-2150-i11-n27`; certificate L016 in preparation): no outcome is claimed here.
- **Start with** `results/FINAL_REPORT.md` (definitive narrative) and `results/LEDGER.md` (verified results with evidence paths).
- **Certificates (referee ACCEPT):** `results/proofs/L001`-`L015` (L001-L006 are described below; L007-L011, K51-K55 [verified-here]: no non-saturated extremal 14-point set, f(16)=10, f(18)=11, f(20)=12, f(22)=13, hence no (4,5)-set with at most 22 points beats 4/7; L012, K56 [verified-here]: a 23-point record would have a saturated AP pattern (23,21,10) with every AP-degree at most 3; L013, K57 [verified-here]: I11 holds on the abstract class C for all n <= 26; L014, K58 [verified-here]: f(23)=14, hence no (4,5)-set with at most 24 points beats 4/7; L015, K60: for every K >= 0 the self-similar family S_K of an anonymous reader (Erdős Problem a Day, 19 Oct 2026; a [community] construction, verified here, not discovered here) consists of (4,5)-sets with 11+9K points and h = 7+5K, hence c* <= 5/9; the construction is [community] and the independent proof in L015 is [verified-here]; L007-L015 each ACCEPTED by three referee rounds, L015 with round 1 'ACCEPT WITH FIXES' (editorial fixes applied) and rounds 2 and 3 ACCEPT; see `results/LEDGER.md`), with the reviews in `results/reviews/` (L006, K48 [verified-here]: no 14-point (4,5)-set with $h\le8$ contains an extremal 12-point set; the 1,887,566 single (4,5) extensions of the 54,243 classes of L002 have $h=8$ and the 51,264,727 (4,5) T1b two-point extensions have $h=9$; two referee ACCEPTs after one text-only NEEDS-WORK round; scout CLEAR; `experiments/20261016-0330-ext12-all`, `tests/test_ext12_all.py`):
  L001 no 2-point extension of A_base has $h\le9$; L002 exactly 54,243 twelve-point extremal sets;
  L003 saturated extremal counts 1, 4, 66, 1262, 6644, 466961 for $n=6..11$; L004 exactly 2,910 saturated 14-point extremal sets;
  L005 (K46) no 16-point (4,5)-set with $h\le9$ contains a saturated extremal 14-point set (the L001 case analysis applied to all 2,910 classes: all 141,153 single (4,5) extensions, 4,970,208 enumerated (4,5) T1b pairs and 122,220 line hypergraphs give $h=10$; two referee ACCEPTs after one text-only NEEDS-WORK round; scout CLEAR).
- **Exact values:** $f(n)=\lceil n/2\rceil+1$ for $6\le n\le15$ and $n=17$ (K35) [verified-here]; $f(16)=10$ (L008, K52; Q1 closed), $f(18)=11$ (L009, K53), $f(20)=12$ (L010, K54) and $f(22)=13$ (L011, K55) [verified-here, computer-assisted, three referees each]; also $f(24)=14$, $f(26)=15$, $f(28)=16$ [derived-here]. Hence no (4,5)-set with at most 22 points beats $4/7$ (sizes $\le15$, 17, 19, 21 are excluded by Henning–Yeo arithmetic; sizes 16, 18, 20, 22 by the certificates). Still open for $n\le24$: $f(19)\in\{11,12\}$ and $f(21)\in\{12,13\}$ (and for most larger $n$). $f(23)=14$ is also settled (L014, K58; Q14 closed) [verified-here, computer-assisted, three referees]: the degree-3 case of the cell $(23,21,10)$ is empty, and L012 (K56) excludes maximum degree $\ge4$, so no 23-point (4,5)-set has $h=13$. Since $n=24$ is excluded by Henning–Yeo arithmetic, no (4,5)-set with at most 24 points beats $4/7$, and the first open record size is $n=25$.
- **Census data:** `data/census_n14_m12_classes.jsonl.gz` (2,910 sets), `data/census_n14_m12_summary.json`,
    `data/ext12_all_rows.jsonl.gz` (one row per 12-point class, field `class` = index into `realized_n12.json.gz`: the L006 two-point-extension sweep, K48),
    `experiments/20261014-1005-census-dfs/results/realized_n12.json.gz` (54,243 sets); index in `data/README.md`. Non-saturated extremal 15-point sets (K50 [verified-here]): `data/ext15_sets.jsonl.gz` (2,337 sampled sets with $m=11$ (748) or $m=12$ (1,589) APs, each exactly realized with $h=9$; `experiments/20261017-0210-ext15-hunt`). K49 counts (extremal (n-2)-subsets of extremal classes): `experiments/20261016-0840-extremal-subsets/results.json`.
  Forbidden-configuration library: `data/forbidden_ordered_n7.json`, `data/forbidden_ordered_n8.json` (287 minimal cores).
  L005 sweep data: `experiments/20261015-2340-ext14-all/results.json` (one row per class of the 2,910); K47 structure census: `experiments/20261016-0150-structure-2910/results.json`.
- **Lemmas:** monotone midpoints (K30), no medial triangle (K31), degree bound in Gyarfas-Lehel-tight hypergraphs (K44). K47 [verified-here]: in the 2,910 saturated extremal 14-point classes the AP degrees are 2, 3 or 4, there are 137 to 150 maximum Sidon subsets per class, no class contains a 12-point subset with $h=7$, and no vertex lies in every maximum Sidon subset (`tests/test_structure_2910.py`). Extension lemmas in `kb/notes/extension_lemmas.md` [derived-here; falsifier found no counterexample on about 11,000 sets and fixed two gaps in the Lemma Delta consequence paragraph, `experiments/falsify/extension-lemmas`]: Lemma E (one-edge extension raises $h$ by 1, instead of 2, exactly when the vertex lies in every maximum Sidon subset), Lemma U (Henning-Yeo obstruction to such vertices; none occurs in the 2,910 classes), Lemma Delta (in a 16-point record every 15-point subset is extremal and $\deg p\le m-9$), Lemma Delta' (deletion version: if $A$ is extremal with $f(n-2)=f(n)-1$ and $A-p-q$ is extremal, then $\deg p+\deg q-\varepsilon\le m-(17\tau-5n-7)/3$, where $\tau=n-f(n)$ and $\varepsilon=1$ if $p,q$ lie on a common AP, else $0$; this is Henning-Yeo applied to $H-p-q$ [derived-here]; falsifier HOLDS-ON-DATA with 0 violations on all 54,243 twelve-point classes, the 6,644 saturated 10-point, 66 saturated 8-point and 2,910 fourteen-point classes, which tests the arithmetic and hypotheses rather than new combinatorics, `experiments/falsify/deletion-lemma`). K49 [verified-here counts, heuristic trend]: the fraction of saturated extremal classes containing an extremal subset two points smaller is 100% at $n=6..9, 11$, 99.7% at $n=10$ (6,625 of 6,644), 49.5% at $n=12$ (26,852 of 54,243) and 0% at $n=14$ (0 of 2,910, K47); the downward trend at even $n$ rests on three data points [heuristic] (`experiments/20261016-0840-extremal-subsets`, `tests/test_extremal_subsets.py`).
- **Negative results** (status of 2026-10-16; superseded in part on 2026-10-17: f(16)=10 was decided by the I11 induction, certificate L008 / K52, which closes Q1 and the "n=16 undecided / f(16) stays open" statements below; Q11 was closed by L007 / K51 and is no longer "not covered"; D25 and D26 were added, see `kb/dead_ends.md` D15-D26): `kb/dead_ends.md` D15-D24 (n=16 not decided by SAT/CP-SAT/annealing; Q8 false in the abstract class; exact saturated census at n=13 infeasible with the L002/L004 pipeline, D22 / Q12; D23: adding two points to smaller extremal sets gives no larger extremal or record set in the cases covered, since no 14-point (4,5)-set with $h=8$ contains an extremal 12-point set (K48; in particular none of the 2,910 saturated classes, K47) and no saturated extremal 14-point class extends to a 16-point set with $h\le9$ (K46), while the non-saturated $(14,11)$ extremal 14-point sets, Q11, are not covered [verified-here]; D24: CP-SAT (`experiments/20261016-0850-n16-deletion-cpsat`) and CaDiCaL (`experiments/20261016-1240-n16-cnf-witness`) at n=16 with the Henning-Yeo deletion constraints, UNKNOWN / TIMEOUT after 3.5 h for each of $m=13$ and $m=14$, no solution and no refutation, so f(16) stays open, Q1 [heuristic: solver outcomes]).
- **Historical (status at the 2026-10-16 16:12 UTC update; superseded on 2026-10-17: the $(14,11)$ cell was settled by certificate L007, K51, which closes Q11, so "Q11 stays open" below is no longer true; the DFS was stopped after at least 1,081 of 3,437 depth-3 prefixes (last progress line of its git-ignored run.log, which prints every 10 prefixes; 1,087 per-prefix `.done` markers exist on disk in the git-ignored results folder, all with 0 patterns and no timeouts), and no claim rests on it; the budget end and PR plan quoted below are those of the first 72 h, the run was then extended to 2026-10-18 23:06 UTC):** exhaustive DFS for the non-saturated $(14,11)$ case (`experiments/20261014-1005-census-dfs/n14m11dfs`; 4 workers, resumable by prefix; stopped from 08:49 to 12:34 UTC while the CP-SAT run of D24 used the cores). 558 of its 3,437 depth-3 prefixes were finished, every one with 0 patterns. At the measured 22 to 36 prefixes per hour it needs roughly 80 to 130 more hours, but the budget ends at 2026-10-16 23:06 UTC (about 7 h later; PR #1, `claude/intelligent-pasteur-22z06m` -> `main`, is to be merged at about 21:00 UTC, after the final checkpoint), so it will not finish, Q11 stays open, and no claim rests on this partial coverage [heuristic: rate projection]. The saturated $n=13$ census was started and stopped as infeasible (D22, Q12 in `kb/`).
- **Reproduce:** every experiment folder except `experiments/20261015-2310-doc-verify` (verifier notes only: `kb-audit.md`, `readmes.md`) has a `README.md` with the exact command; some bulky outputs and logs are git-ignored (see the reminder in `experiments/README.md`); the certificates `results/proofs/L007`-`L015` (all ACCEPTED) are reproduced by `cd experiments/prover/L0NN && bash reproduce.sh` (run from inside the folder, because the scripts use relative paths; `experiments/prover/` has no README of its own, but `L007/`, `L013/`, `L014/` and `L015/` each have one, and so does the in-progress, unrefereed `L016/`; the L015 script needs only the Python standard library and about 4 CPU-minutes; L015 is this project's independent proof and verification of the self-similar 5/9 family, which is an anonymous reader's construction and claim [community] (Erdős Problem a Day, 19 Oct 2026; verified here, not discovered here), and that family is rebuilt and checked by the commands in section 3 of `experiments/20261020-1730-reader-5-9/README.md` (the frozen judge on its 65-point member, claim C003, took about 35 minutes standalone and about 59 minutes through `scripts/new_claim.py`, measured on a shared 4-core machine, see section 4.2 there); later scripts reuse the outputs of earlier certificates, L011 needs a few CPU-hours, bulky outputs go to git-ignored `out/` or `indep/*.txt` or are stored gzipped, and the L012 script also needs the nauty 2.8.8 sources that sit in the git-ignored `experiments/referee/L010-round1/out/`); most referee rounds carry their own `reproduce*.sh` or a README listing their scripts (`experiments/referee/L0NN-roundK/`; `L007-round1` has neither); tests: `python3 -m pytest -q` (including the cheap cells of L007 and L008 in `tests/test_l007_cells.py` and `tests/test_l008_cells.py`; for L009-L012 the tests pin only the resulting values f(18)=11, f(20)=12, f(22)=13 in `e757.fn_bounds`, not the computations, which only the `reproduce.sh` scripts rerun).
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
  accepted by a referee subagent. (Status 2026-10-20: `status.sh` reports clause A because of claim C003, the 65-point member ($h=37$) of an anonymous reader's self-similar family, posted on Erdős Problem a Day on 19 Oct 2026. That construction is a COMMUNITY result, not a discovery of this project, which only rebuilt, judged and refereed it. The status block records no provenance, so read it together with the K59/C003 and K60/L015 rows of `results/LEDGER.md` and rows K59 and K60 of `kb/known_results.md`.)
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
